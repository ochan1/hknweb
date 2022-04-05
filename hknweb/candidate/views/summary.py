from django.shortcuts import render
from django.contrib.auth.models import User

from hknweb.utils import login_and_permission
from hknweb.candidate.utils_candportal import CandidatePortalData
from hknweb.candidate.constants import EVENT_NAMES
from hknweb.models import Profile

from multiprocessing import Pool

def process_cand_data(cand):
    data = CandidatePortalData(cand).get_user_cand_data()

    status = [
        data["candidate_forms"]["all_done"],
        data["due_payments"]["all_done"],
        data["committee_project"]["all_done"],
        data["bitbyte"]["status"],
        all(interactiv["status"] for key, interactiv in data["interactivities"].items()),
        *(e["status"] for e in data["events"]),
    ]
    status.append(all(status))

    row = {
        "name": f"{cand.first_name} {cand.last_name} ({cand.username})",
        "status": status,
        "link": f"/cand/portal/{cand.username}",
    }
    return row

@login_and_permission("candidate.change_offchallenge")
def summary(request):
    cands = User.objects.filter(groups__name="candidate")
    headers, rows = [], []

    if len(cands) > 0:
        data = CandidatePortalData(cands[0]).get_user_cand_data()

        headers = [
            "Name",
            "Forms",
            "Payments",
            "Project",
            "BitByte",
            "Hangouts and Challenges",
        ]
        for event in data["events"]:
            event_title = event["title"]
            if len(event_title) > 15:
                event_title = event_title.split()[0]
            headers.append(event_title)
        headers.append("Overall")

    pool = Pool()
    results = []

    for cand in cands:
        p = pool.apply_async(process_cand_data, args=(cand,))
        results.append(p)
    
    rows = [p.get() for p in results]

    pool.close()

    context = {
        "headers": headers,
        "rows": rows,
    }
    return render(request, "candidate/summary.html", context=context)
