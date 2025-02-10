import json
import os
from typing import List

from django.shortcuts import render
from django.http import HttpResponse
from .forms import  SearchForm
from django.shortcuts import render, redirect
from . import service_layer as kb
from .models import SessionData
from .service_query_nlp import  create_query



def customer_search(request):
    sparql_results = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to database, send email)
            customer_prompt = form.cleaned_data['prompt']
            # Store the data in the session
            sparql_results = request.session['data_response']
            # append the input by the customer
            sparql_results.append({ "type" : "user", "content" : customer_prompt })
            # we now go to the model to sanitize the data
            # opportunity in the line to use nlp to resolve customer question
            query = create_query(customer_prompt)
            # pass the query to the model
            results = kb.process_request(query)
            # # we create headers
            body = kb.data_to_obj_create_body(results)
            sparql_results.append({ "type": "system", "content": body})
            request.session['data_response'] = sparql_results
            return redirect('search')
        else:
            # Form is not valid, re-render the form with errors
            return render(request, 'customer_search.html', {'form': form, 'data_response': sparql_results})
    else:  # GET request
        form = SearchForm()
        # request.session['data_response'] = []
        if 'data_response' in request.session:
            sparql_results = request.session['data_response']
        if len(sparql_results) > 5:
            # remove first 2 elements
            sparql_results = sparql_results[2:]
        request.session['data_response'] = sparql_results
        return render(request, 'customer_search.html', {'form': form,  'data_response': sparql_results})