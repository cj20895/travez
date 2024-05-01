from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully created for {username}! Login In Now')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'stackusers/register.html', {'form': form})

@login_required
def profile(request):
        return render(request, 'stackusers/profile.html')
        
@login_required
def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Acount Updated Successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'stackusers/profile_update.html', context)

from django.shortcuts import render, redirect
from .models import Person
from .forms import RideForm, NewRideForm
import os
# from langchain_openai import OpenAI
# from langchain_openai import ChatOpenAI  # Import ChatOpenAI
# from dotenv import load_dotenv
# from langchain_core.messages import HumanMessage, SystemMessage

# from transformers import pipeline
from .models import Person
from django.shortcuts import render
from django.conf import settings  # Assuming your API key is stored in Django's settings
from openai import OpenAI
from dotenv import load_dotenv
import json



# Load environment variables from .env file.
load_dotenv()

# Initialize OpenAI client with API key.
print("api key: ", os.getenv("OPEN_AI_KEY"))
print("okay")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=OPEN_AI_KEY)

# chat_client = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPEN_AI_KEY"))


def test(request):
    # Logic for the about page.
    return render(request, 'HRabout.html')

def ai_interaction(request):
    print("ai_interaction called")

    context = {}
    
    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # # Load your OpenAI API key from settings or environment variable
        # openai.api_key = settings.OPEN_AI_KEY  # Or use os.getenv("OPEN_AI_KEY")

        try:
            # Make a call to the OpenAI API, specifying GPT-4 (or the appropriate engine name for GPT-4 access)
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                # response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are looking to parse the user input text and find relevant information regarding the orgination state, orgination city, destination state, destination state and print that out. Not all information may be present just return the relvant information that is present. Convert all full abbrevations of city names to the full name of the city."},
                    {"role": "user", "content": user_input}
                ]
            )
            # The last message in the response should be from the assistant, extract that message
            ai_text = response.choices[0].message.content
        except Exception as e:
            ai_text = f"Error: {str(e)}"

        destcity = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Based on the inputed text, parse out just the destination city if there is one. If not, return the number 0."},
                {"role": "user", "content": ai_text}
            ]
        )

        destcity_field = destcity.choices[0].message.content

        deststate = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Based on the inputed text, parse out just the destination state if there is one and return the appropriate state abbreviation. If not, return the number 0. For example, if 'Oregon' is the state, the AI should return the abbreviation of the state 'OR'."},
                {"role": "user", "content": ai_text}
            ]
        )

        deststate_field = deststate.choices[0].message.content

        originstate = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Based on the inputed text, parse out just the origin state if there is one and return the appropriate state abbreviation. If not, return the number 0. For example, if 'Oregon' is the state, the AI should return the abbreviation of the state 'OR'."},
                {"role": "user", "content": ai_text}
            ]
        )

        originstate_field = originstate.choices[0].message.content

        origincity = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Based on the inputed text, parse out just the origin city if there is one. If not, return the number 0."},
                {"role": "user", "content": ai_text}
            ]
        )

        origincity_field = origincity.choices[0].message.content

        # # Render the AI response in the template
        # return render(request, 'index_view.html', {
        #     'user_input': user_input,
        #     'ai_text': origincity_field
        # })

        
        # print("uhh")
        # Assuming AI returns JSON-like responses, or adjust parsing logic as needed
        search_city_origin = origincity_field.strip()
        print("origin city: ", search_city_origin)
        search_state_origin = originstate_field.strip().upper()
        search_city_destination = destcity_field.strip()
        search_state_destination = deststate_field.strip().upper()

        search_city_origin = search_city_origin.replace("0","")
        search_state_origin = search_state_origin.replace("0","")
        search_city_destination = search_city_destination.replace("0","")
        search_state_destination = search_state_destination.replace("0", "")

        # # Filter Person objects based on AI-extracted search criteria
        # queryset = Person.objects.all()
        # if search_city_origin:
        #     queryset = queryset.filter(origination__icontains=search_city_origin)
        # if search_state_origin:
        #     queryset = queryset.filter(origination_state__iexact=search_state_origin)
        # if search_city_destination:
        #     queryset = queryset.filter(destination_city__icontains=search_city_destination)
        # if search_state_destination:
        #     queryset = queryset.filter(destination_state__iexact=search_state_destination)

        # context['people'] = queryset


    print("found something to display")
    context = display(search_city_origin, search_state_origin, search_city_destination, search_state_destination)
    return render(request, "HRindex_view.html", context)

        # context = {
        #     'people': queryset,
        #     'form': RideForm(),
        #     'new_ride_form': NewRideForm()
        # }

        # print("context: ", context)
        # return render(request, "index_view.html", context)

    # Include forms in the context.
    context["form"] = RideForm()
    context["new_ride_form"] = NewRideForm()
    return render(request, "index_view.html", context)

    # Handle non-POST requests
    return render(request, 'index_view.html')


def index(request):
    print("searched")
    context = {}
    # Retrieve search parameters.
    
    search_city_origin = request.GET.get('search_origin', '').strip().replace("0", "")
    print("search city origin: ", search_city_origin)
    search_state_origin = request.GET.get('searchstate_origin', '').strip().upper().replace("0", "")
    search_city_destination = request.GET.get('search_destination', '').strip().replace("0", "")
    search_state_destination = request.GET.get('searchstate_destination', '').strip().upper().replace("0", "")


    context = display(search_city_origin, search_state_origin, search_city_destination, search_state_destination)
    # # Filter Person objects based on search criteria.
    # if any([search_city_origin, search_state_origin, search_city_destination, search_state_destination]):
    #     queryset = Person.objects.all()
    #     if search_city_origin:
    #         queryset = queryset.filter(origination__icontains=search_city_origin)
    #     if search_state_origin:
    #         queryset = queryset.filter(origination_state__iexact=search_state_origin)
    #     if search_city_destination:
    #         queryset = queryset.filter(destination_city__icontains=search_city_destination)
    #     if search_state_destination:
    #         queryset = queryset.filter(destination_state__iexact=search_state_destination)
    #     context['people'] = queryset

    # # Include forms in the context.
    # context["form"] = RideForm()
    # context["new_ride_form"] = NewRideForm()
    return render(request, "HRindex_view.html", context)

def display(search_city_origin, search_state_origin, search_city_destination, search_state_destination):
    context = {}
    print("line break")
    print(search_city_destination, search_state_destination, search_city_origin, search_state_origin)
    if any([search_city_origin, search_state_origin, search_city_destination, search_state_destination]):
        queryset = Person.objects.all()
        if search_city_origin:
            queryset = queryset.filter(origination__icontains=search_city_origin)
        if search_state_origin:
            queryset = queryset.filter(origination_state__iexact=search_state_origin)
        if search_city_destination:
            queryset = queryset.filter(destination_city__icontains=search_city_destination)
        if search_state_destination:
            queryset = queryset.filter(destination_state__iexact=search_state_destination)
        context['people'] = queryset


    # Include forms in the context.
    context["form"] = RideForm()
    context["new_ride_form"] = NewRideForm()
    return context

def create(request):
    if request.method == 'POST':
        form = NewRideForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/rides')  # Ensure this redirects to your intended view.
    else:
        form = NewRideForm()
    return render(request, 'HRcreate.html', {'new_ride_form': form})

# def ai_interaction(request):
#     if request.method == 'POST':
#         input_text = request.POST.get('user_input')
#         response = client.completions(prompt=input_text, temperature=0.8)

#         ai_text = response.choices[0].text if response.choices else "No response"
#         return render(request, 'ai_interaction.html', {'user_input': input_text, 'ai_text': ai_text})
#     return render(request, 'ai_interaction.html')
# def ai_interaction(request):
#     if request.method == 'POST':
#         input_text = request.POST.get('user_input')
        
#         try:
#             # Simulated call to the OpenAI client. Adjust according to the actual API.
#             response = client.make_request("completions", data={
#                 "prompt": input_text,
#                 "temperature": 0.8,
#                 # Add other necessary parameters as per the OpenAI API requirements
#             })
#             # Extracting AI text response
#             ai_text = response['choices'][0]['text'] if response.get('choices') else "No response"
            
#             # Printing the AI response to the console
#             print("AI Response:", ai_text)
#         except AttributeError as e:
#             ai_text = "Error: " + str(e)
#             print(ai_text)
        
#         # Rendering the response in the template
#         return render(request, 'ai_interaction.html', {'user_input': input_text, 'ai_text': ai_text})

#     # Handling GET request or other methods
#     return render(request, 'ai_interaction.html')

# def ai_interaction(request):
#     if request.method == 'POST':
#         input_text = request.POST.get('user_input')

#         # Prepare the messages list with the HumanMessage
#         messages = [HumanMessage(content=input_text)]

#         # Attempt to get a response from the ChatOpenAI client
#         try:
#             response_messages = chat_client.invoke(messages)
#             # Assuming the response is a list of message objects, get the last one
#             ai_message = response_messages[-1] if response_messages else None
#             ai_text = ai_message.content if ai_message else "No response"
#         except Exception as e:
#             ai_text = f"Error: {str(e)}"

#         # Render the AI response in the template
#         return render(request, 'ai_interaction.html', {
#             'user_input': input_text, 
#             'ai_text': ai_text
#         })

#     # Handling GET request or other methods
#     return render(request, 'ai_interaction.html')
# def ai_interaction(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input')

#         # # Load your OpenAI API key from settings or environment variable
#         # openai.api_key = settings.OPEN_AI_KEY  # Or use os.getenv("OPEN_AI_KEY")

#         try:
#             # Make a call to the OpenAI API, specifying GPT-4 (or the appropriate engine name for GPT-4 access)
#             response = client.chat.completions.create(
#                 model="gpt-4-turbo-preview",
#                 prompt=user_input,
#                 max_tokens=100,  # Adjust based on your needs
#                 n=1,  # Number of completions to generate
#                 stop=None,  # You can specify stopping criteria if needed
#                 temperature=0.7  # Adjust creativity
#             )
#             # Extracting the text from the response
#             ai_text = response.choices[0].text.strip()
#         except Exception as e:
#             ai_text = f"Error: {str(e)}"

#         # Render the AI response in the template
#         return render(request, 'ai_interaction.html', {
#             'user_input': user_input,
#             'ai_text': ai_text
#         })

#     # Handle non-POST requests
#     return render(request, 'ai_interaction.html')

# def ai_interaction(request):
#     print("ai_interaction called")
#     context = {}
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input')

#         # # Load your OpenAI API key from settings or environment variable
#         # openai.api_key = settings.OPEN_AI_KEY  # Or use os.getenv("OPEN_AI_KEY")

#         try:
#             # Make a call to the OpenAI API, specifying GPT-4 (or the appropriate engine name for GPT-4 access)
#             response = client.chat.completions.create(
#                 model="gpt-4-turbo-preview",
#                 # response_format={ "type": "json_object" },
#                 messages=[
#                     {"role": "system", "content": "You are looking to parse the user input text and find relevant information regarding the orgination state, orgination city, destination state, destination state and print that out. Not all information may be present just return the relvant information that is present. Convert all full abbrevations of city names to the full name of the city."},
#                     {"role": "user", "content": user_input}
#                 ]
#             )
#             # The last message in the response should be from the assistant, extract that message
#             ai_text = response.choices[0].message.content
#         except Exception as e:
#             ai_text = f"Error: {str(e)}"

#         destcity = client.chat.completions.create(
#             model="gpt-4-turbo-preview",
#             messages=[
#                 {"role": "system", "content": "Based on the inputed text, parse out just the destination city if there is one. If not, return the number 0."},
#                 {"role": "user", "content": ai_text}
#             ]
#         )

#         destcity_field = destcity.choices[0].message.content

#         deststate = client.chat.completions.create(
#             model="gpt-4-turbo-preview",
#             messages=[
#                 {"role": "system", "content": "Based on the inputed text, parse out just the destination state if there is one. If not, return the number 0."},
#                 {"role": "user", "content": ai_text}
#             ]
#         )

#         deststate_field = deststate.choices[0].message.content

#         originstate = client.chat.completions.create(
#             model="gpt-4-turbo-preview",
#             messages=[
#                 {"role": "system", "content": "Based on the inputed text, parse out just the origin state if there is one. If not, return the number 0."},
#                 {"role": "user", "content": ai_text}
#             ]
#         )

#         originstate_field = originstate.choices[0].message.content

#         origincity = client.chat.completions.create(
#             model="gpt-4-turbo-preview",
#             messages=[
#                 {"role": "system", "content": "Based on the inputed text, parse out just the origin city if there is one. If not, return the number 0."},
#                 {"role": "user", "content": ai_text}
#             ]
#         )

#         origincity_field = origincity.choices[0].message.content

#         # # Render the AI response in the template
#         # return render(request, 'index_view.html', {
#         #     'user_input': user_input,
#         #     'ai_text': origincity_field
#         # })

        
# # Assuming AI returns JSON-like responses, or adjust parsing logic as needed
#         search_city_origin = origincity_field.strip()
#         search_state_origin = originstate_field.strip().upper()
#         search_city_destination = destcity_field.strip()
#         search_state_destination = deststate_field.strip().upper()

#         # Filter Person objects based on AI-extracted search criteria
#         queryset = Person.objects.all()
#         if search_city_origin and search_city_origin != "0":
#             queryset = queryset.filter(origination__icontains=search_city_origin)
#         if search_state_origin and search_state_origin != "0":
#             queryset = queryset.filter(origination_state__iexact=search_state_origin)
#         if search_city_destination and search_city_destination != "0":
#             queryset = queryset.filter(destination_city__icontains=search_city_destination)
#         if search_state_destination and search_state_destination != "0":
#             queryset = queryset.filter(destination_state__iexact=search_state_destination)
        
#         context = {
#             'people': queryset,
#             'form': RideForm(),
#             'new_ride_form': NewRideForm()
#         }
#         return render(request, "index_view.html", context)

#     # Include forms in the context.
#     context["form"] = RideForm()
#     context["new_ride_form"] = NewRideForm()
#     return render(request, "index_view.html", context)

#     # Handle non-POST requests
#     return render(request, 'index_view.html')