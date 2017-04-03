from django.core.mail import send_mail

# def send_email():
#     #for decision in Decision.objects.all():
#     #  if decision.active == True:
#     #    message = "Dear Sir,\n\nThe following crisis has occured: " + \
#     #                decision.type_of_crisis.__unicode__() + "\n\nThe details are as follows: " +  \
#     #          decision.description + "\n\nDate and Time: " + str(decision.date_time) \
#     #          + "\n\nBest,\nAllStarCMS"
#     #    send_to_president(message)
#     # get all active decisions
#     active_decisions = Decision.objects.filter(active=True)
#     if len(active_decisions) != 0:
#         active_decisions_msg = ""
#         for active_decision in active_decisions:
#             active_decisions_msg += active_decision.type_of_crisis.__unicode__() + "\n" + \
#                                     active_decision.description + "\n" + \
#                                     str(active_decision.date_time) + "\n\n"
#         msg = "Dear Sir,\n\nThe following crisis are ongoing:\n\n" + \
#               active_decisions_msg + \
#               "Best,\nAllStarCMS"
#         send_to_president(msg)

def send_to_president(message):
    """
    Send custom message to PMO in case of any issue

    :param message: Custom message to be sent to the PMO
    :return: None
    """
    send_mail("Periodic Report"
              , message
              , 'wuevnas@gmail.com',
              ['wuevans@hotmail.com'],
              fail_silently=False)
