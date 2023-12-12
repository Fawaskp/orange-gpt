from django.shortcuts import render
import requests
import json
from deep_translator import GoogleTranslator
import openai
import re
from decouple import config

def enquiry(query):
        openai.api_key = config('OPENAI_API_KEY')
        prompt = f'{query} User:fasil'
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
        )
        stir=response.choices[0].text.strip()
        print('Chat GPT-> Response')
        print()
        print(response)
        print()
        return stir
        
    
def gpt(request):
    if request.method == 'POST':
        word = request.POST['word']
        splitted = word.split(' ')
        context = {
                'word':request.POST['word']
        }
        if(len(splitted)==1):
            con = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+word)
            result = json.loads(con.text)
            if con.status_code == 200:
                meaning =result[0].get('meanings', '')
                definitions=meaning[0].get('definitions','')
                definition=definitions[0].get('definition','')
                data = GoogleTranslator(source='auto', target='ml').translate(definition)
                print('Translated --> ',data)
                context.update(meaning=f'{data} ')
                context.update(is_result=True)
            
            elif con.status_code == 404:
                pattern = '[A-Za-z]'
                if re.match(pattern, word):
                    message = enquiry('What is the meaning of ' + word)
                else:
                    message = enquiry('Solve ' + word)
                
                data = GoogleTranslator(source='auto', target='ml').translate(message)
                context.update(meaning=data)
                context.update(is_result=True)
            return render(request,'sample.html',context)
        else:
            result = enquiry(word)
            print('Result -> ',result)
            result = json.dumps(result)
            print('')
            print('')
            print('JSONIFIED',result)
            context.update(meaning=f'{result[1:-1]} ')
            context.update(is_result=True)
            return render(request,'sample.html',context)

    return render(request,'sample.html')


