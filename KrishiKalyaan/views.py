from django.shortcuts import render
import requests, json
from django.http import JsonResponse
import pickle
import numpy as np
from .models import Data, Feedback_form
loaded_model = pickle.load(open("model\model.pkl", 'rb'))

# Create your views here.

def index(request):
    return render(request, 'KrishiKalyaan/index.html')

def about(request):
    return render(request,'KrishiKalyaan/about.html')



def schemes(request):
    return render(request,'KrishiKalyaan/schemes.html')




def organic(request):
    return render(request,'KrishiKalyaan/organicfarming.html')

def contact(request):
    return render(request,'KrishiKalyaan/contact.html')

def predict(request):
    result={}
   
    if request.method == 'POST':
        N = int(request.POST['Nitrogen'])
        P = int(request.POST['Phosporus'])
        K = int(request.POST['Potassium'])
        temp = float(request.POST['Temperature'])
        humidity = float(request.POST['Humidity'])
        ph = float(request.POST['pH'])
        rainfall = float(request.POST['Rainfall'])

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        prediction = loaded_model.predict(single_pred)

        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            data = Data(nitrogen=N, phosphorus=P, potassium=K, temperature=temp, humidity=humidity, pH=ph, rainfall=rainfall, crop_result = crop)
            data.save()
            result = "{} is the best crop to be cultivated right there".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

        return render(request, 'Krishikalyaan/prediction.html', {'prediction': result, 'crop': crop})

    return render(request, 'KrishiKalyaan/prediction.html')

def latestnews(request):
   
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=in&'
        #    'category=technology&'
           'apiKey=f5f8d71c4026477a911ece0719e040ff')
    response = requests.get(url)
    l=response.json()['articles']
    #pprint(response.json()['articles'][0]['urlToImage'])
    desc = []
    news = []
    img = []

    for i in range(len(l)):
        f = l[i]
        news.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
    mylist = zip(news, desc, img)

    return render(request, 'KrishiKalyaan/news.html', context={"mylist": mylist})

def index1(request):
    if request.method == 'POST':
        try:
            dataa = json.loads(request.POST['content'] )
            print(dataa)
            t1,t2,t3=getCityInfo(dataa[0])

            crop1=recommend(dataa[2],dataa[3],dataa[4], t1, t2, dataa[1], t3)
            print(crop1)
        except:
            crop1="Invalid Input"
            print("Invalid Input")
        #print(type(dataa))
        #return HttpResponse(dataa)
        return JsonResponse({'message': 'success', 'username': "username", 'content': crop1})
    

    def getCityInfo(city_name):
        api_key = "15e46bb2ab66ccd2c49c545973237381"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        #city_name = input("Enter city name : ")
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        print(x)
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]-273.15
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            #print(current_temperature,current_pressure,current_humidiy,weather_description)
            return current_temperature,current_humidiy,current_temperature+100
        


def feedback(request):
    if request.method == 'POST':
        name = str(request.POST.get('feedback_name'))
        phone = str(request.POST.get('feedback_phone'))
        email = str (request.POST.get('feedback_email'))
        message = str(request.POST.get('feedback_msg'))

        existing_submission = Feedback_form.objects.filter(phone = phone, email=email).exists()
        if existing_submission:
            return render(request, 'KrishiKalyaan/index.html')
        
        data = Feedback_form(name=name,
                             phone=phone,
                             email=email,
                             message=message)
        
        data.save()
        data = Feedback_form()
        return render(request, 'KrishiKalyaan/index.html')


