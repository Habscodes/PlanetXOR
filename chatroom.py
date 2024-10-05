# from pywebio import *
# from pywebio.output import *
# from pywebio.input import *

# import asyncio
# from pywebio.session import defer_call, info as session_info, run_async
# import datetime

# MAX_MESSAGES_CNT = 500  # Reduced message history count for better performance

# chat_msgs = []  # (name, msg)
# online_users = set()
# climate_experts = {"StormRider", "SunnySkies"}  # You can add expert usernames here


# async def refresh_msg(my_name, msg_box):
#     """Send new messages to the current session"""
#     global chat_msgs
#     last_idx = len(chat_msgs)
#     while True:
#         await asyncio.sleep(0.5)
#         for m in chat_msgs[last_idx:]:
#             if m[0] != my_name:  # Only refresh messages not sent by the current user
#                 msg_box.append(put_markdown(f'`{m[2]} {m[0]}`: {m[1]}', sanitize=True))

#         # Remove expired messages
#         if len(chat_msgs) > MAX_MESSAGES_CNT:
#             chat_msgs = chat_msgs[len(chat_msgs) // 2:]

#         last_idx = len(chat_msgs)


# async def main():
#     """Custom Chatroom for CliMATE Project | Weather and Climate Discussions"""
#     global chat_msgs

#     put_markdown("## Welcome to CliMATE Chat\n"
#                  "Let's discuss weather and climate-related topics around the globe.",
#                  lstrip=True)

#     msg_box = output()
#     put_scrollable(msg_box, height=300, keep_bottom=True)

#     # Custom nickname prompt
#     nickname = await input("Choose a weather-related nickname (e.g., StormRider, SunnySkies)", required=True,
#                            validate=lambda n: 'This name is already in use or invalid'
#                            if n in online_users or n == '📢' else None)

#     online_users.add(nickname)
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     chat_msgs.append(('📢', f'`{nickname}` joins the room. {len(online_users)} users currently online', timestamp))
#     msg_box.append(put_markdown(f'`📢 {timestamp}`: `{nickname}` joins the room. {len(online_users)} users online.',
#                                 sanitize=True))

#     @defer_call
#     def on_close():
#         online_users.remove(nickname)
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         chat_msgs.append(('📢', f'`{nickname}` leaves the room. {len(online_users)} users currently online', timestamp))

#     refresh_task = run_async(refresh_msg(nickname, msg_box))

#     while True:
#         # Input group for sending messages or sharing weather info
#         data = await input_group('Send message or share weather info', [
#             input(name='msg', help_text='Message content supports inline Markdown syntax'),
#             actions(name='cmd', buttons=['Send', 'Share Weather Info', {'label': 'Exit', 'type': 'cancel'}])
#         ], validate=lambda d: ('msg', 'Message content cannot be empty') if d['cmd'] == 'Send' and not d['msg'] else None)

#         if data is None:  # Exit chat
#             break

#         # Handle Multiline Input
#         if data['cmd'] == 'Share Weather Info':
#             city = await input("Enter city for weather info")
#             weather_data = fetch_weather(city)  # Assume you have a function `fetch_weather` to get weather data
#             msg_box.append(put_markdown(f'`{nickname}`: Shared weather info for {city}: {weather_data}'))
#         else:
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             if nickname in climate_experts:
#                 msg_box.append(put_markdown(f'`{timestamp} [Expert] {nickname}`: {data["msg"]}', sanitize=True))
#             else:
#                 msg_box.append(put_markdown(f'`{timestamp} {nickname}`: {data["msg"]}', sanitize=True))
#             chat_msgs.append((nickname, data['msg'], timestamp))

#     refresh_task.close()
#     toast("You have left the chat room")


# # Sample weather fetching function (you'll need to integrate with your existing weather app)
# def fetch_weather(city):
#     # Simulating weather data fetching
#     return f"Temperature: 25°C, Humidity: 60%, Condition: Sunny in {city}"




from pywebio import *
from pywebio.output import *
from pywebio.input import *
import asyncio
from pywebio.session import defer_call, run_async
import datetime
import requests
import os

MAX_MESSAGES_CNT = 500  # Reduced message history count for better performance

chat_msgs = []  # (name, msg)
online_users = set()
climate_experts = {"StormRider", "SunnySkies"}  # You can add expert usernames here

# Replace with your OpenWeather API key
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Make sure to set this in your environment

async def refresh_msg(my_name, msg_box):
    """Send new messages to the current session"""
    global chat_msgs
    last_idx = len(chat_msgs)
    while True:
        await asyncio.sleep(0.5)
        for m in chat_msgs[last_idx:]:
            if m[0] != my_name:  # Only refresh messages not sent by the current user
                msg_box.append(put_markdown(f'`{m[2]} {m[0]}`: {m[1]}', sanitize=True))

        # Remove expired messages
        if len(chat_msgs) > MAX_MESSAGES_CNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)

async def main():
    """Custom Chatroom for PlanetXOR Project | Weather and Climate Discussions"""
    global chat_msgs

    put_markdown("## Welcome to CliMATE Chat\n"
                 "Let's discuss weather and climate-related topics around the globe.",
                 lstrip=True)

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    # Custom nickname prompt
    nickname = await input("Choose a weather-related nickname (e.g., StormRider, SunnySkies)", required=True,
                           validate=lambda n: 'This name is already in use or invalid'
                           if n in online_users or n == '📢' else None)

    online_users.add(nickname)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_msgs.append(('📢', f'`{nickname}` joins the room. {len(online_users)} users currently online', timestamp))
    msg_box.append(put_markdown(f'`📢 {timestamp}`: `{nickname}` joins the room. {len(online_users)} users online.',
                                sanitize=True))

    @defer_call
    def on_close():
        online_users.remove(nickname)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_msgs.append(('📢', f'`{nickname}` leaves the room. {len(online_users)} users currently online', timestamp))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        # Input group for sending messages or sharing weather info
        data = await input_group('Send message or share weather info', [
            input(name='msg', help_text='Message content supports inline Markdown syntax'),
            actions(name='cmd', buttons=['Send', 'Share Weather Info', {'label': 'Exit', 'type': 'cancel'}])
        ], validate=lambda d: ('msg', 'Message content cannot be empty') if d['cmd'] == 'Send' and not d['msg'] else None)

        if data is None:  # Exit chat
            break

        # Handle Weather Info Sharing
        if data['cmd'] == 'Share Weather Info':
            city = await input("Enter city for weather info:", required=True)
            weather_data = fetch_weather(city)
            msg_box.append(put_markdown(f'`{nickname}`: Shared weather info for **{city}**: {weather_data}'))
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if nickname in climate_experts:
                msg_box.append(put_markdown(f'`{timestamp} [Expert] {nickname}`: {data["msg"]}', sanitize=True))
            else:
                msg_box.append(put_markdown(f'`{timestamp} {nickname}`: {data["msg"]}', sanitize=True))
            chat_msgs.append((nickname, data['msg'], timestamp))

    refresh_task.close()
    toast("You have left the chat room")

# Weather fetching function
def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        return f"Temperature: {temp}°C, Humidity: {humidity}%, Condition: {description.capitalize()}"
    else:
        return f"Error: {data.get('message', 'Unable to fetch weather data')}"

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)
