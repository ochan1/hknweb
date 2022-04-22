from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase

from hknweb.events.models import EventType, Event
from hknweb.events.tests.models.utils import ModelFactory
from hknweb.events.tests.views.event_transactions.utils import setUp


class MergeEventsViewTestsBase(CandidateViewTestsBase):
    def test_merge_event_scenario_one(self):
        event_type_list = ["Community", "Indrel"]
        for e_type in event_type_list:
            ModelFactory.create_event_type(type=e_type)

        for event_type in EventType.objects.all():
            for i in range(3):
                ModelFactory.create_event(f"{event_type.type} {i}", event_type, self.officer)


        pass
