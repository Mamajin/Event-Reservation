from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas import *


class TicketStrategy(ABC):
    
    @staticmethod
    def get_strategy(strategy_name):
        strategies = {
            # 'get_user_ticket': TicketGetUserTicket(),
            # 'get_ticket_detail': TicketGetTicketDetail(),
            # 'register_ticket': TicketRegisterStrategy(),
            # 'cancel_ticket': TicketDeleteStrategy(),
            # 'sent_reminder': TicketSendReminderStrategy(),
        }
        return strategies.get(strategy_name)
    
    @abstractmethod
    def execute(self, *arg, **kwargs):
        pass
    

