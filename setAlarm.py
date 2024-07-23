# import datetime
# import winsound
# import fieldName = models.TimeField(auto_now=False, auto_now_add=False)


# def set_alarm(hour, minute):
#     current_time = datetime.datetime.now()
#     alarm_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
#     time_difference = alarm_time - current_time
#     time_to_wait = time_difference.total_seconds()

#     if time_to_wait < 0:
#         print("Invalid alarm time. Please choose a future time.")
#         return

#     print(f"Alarm set for {alarm_time.strftime('%H:%M')}.")

#     # Wait for the specified time
#     time.sleep(time_to_wait)

#     # Play alarm sound
#     frequency = 2500  # Set frequency (2500 Hz)
#     duration = 2000  # Set duration (2 seconds)
#     winsound.Beep(frequency, duration)

# # Example usage: set alarm for 8:30 AM
# set_alarm(8, 30)