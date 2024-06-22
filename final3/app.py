from flask import Flask, render_template, redirect, url_for, request
from dist import calc , db_reader
from plotly.offline import plot
import plotly.express as px
import markupsafe
import re
import graph

cl = calc.TAX_CALCULATOR()
db = db_reader.DB_READER()

app = Flask(__name__)

companies = db.fetchCompanies()
etaxes = [db.selectTaxes(company)[0] for company in companies]
atuals = [db.selectTaxes(company)[1] for company in companies]

tax_diffs = []
tax_growth_rates = []
tax_ids = []
curposx = -1
curposy = -1


for item in db.fetchCompanies():
    etaxes.append(db.selectTaxes(item)[0])
    atuals.append(db.selectTaxes(item)[1])
    for tx in etaxes:
        for mn in atuals:
            try:    
                # print(list(tx)[curposx+1])
                # print(list(mn)[curposy+1])
                tax_diffs.append(cl.tax_diff(list(tx)[curposx+1],list(mn)[curposy+1]))          
                curposx -= 1
                curposy -= 1                  
                tax_growth_rates.append(cl.taxgrowth_rate(list(tx)[curposx+1],list(mn)[curposy+1],db.selectTaxes(item,db.getCurrentmonth())[0]))
                # tgrowths.append(cl.taxgrowth_rate(list(tx)[curposx+1],list(mn)[curposy+1],db.selectTaxes(item,db.getCurrentmonth()))[0])
            except IndexError:
                break

expected_taxes = etaxes
actual_taxes = atuals

tax_diffs = tax_diffs
tax_growth_rates = tax_growth_rates


@app.route('/')
def home():
  return render_template("index.html")


@app.route('/read-form', methods=['POST', 'GET'])
def read_form():

  # Get the form (data) as Python ImmutableDict (data)type
  data = request.form

  print(data)

  company_name = data['userCompanyName']
  tax_id = data['userTaxID']

  jan = data['jan']
  feb = data['feb']
  mar = data['mar']
  apr = data['apr']
  may = data['may']
  jun = data['jun']
  jul = data['jul']
  aug = data['aug']
  sep = data['sep']
  oct = data['oct']
  nov = data['nov']
  dec = data['dec']

  db.createCompany(company_name,tax_id,company_name,cl.rnd_values(),)
  db.insertExpectedTax(company_name, cl.rnd_values(), cl.rnd_values(),
                       cl.rnd_values(), cl.rnd_values(), cl.rnd_values(),
                       cl.rnd_values(), cl.rnd_values(), cl.rnd_values(),
                       cl.rnd_values(), cl.rnd_values(), cl.rnd_values(),
                       cl.rnd_values())
  db.insertActualTax(company_name, jan, feb, mar, apr, may, jun, jul, aug, sep,
                     oct, nov, dec)

  return redirect('/companies')


@app.route('/companies')
def comp_table():
  return render_template("table.html",
                         len=len(companies),
                         Companies=companies,
                         tax_ids=tax_ids,
                         expected_taxes=expected_taxes,
                         actual_taxes=atuals,
                         tax_diffs=tax_diffs,
                         tax_growth_rates=tax_growth_rates)


@app.route('/company/<company>/graph')
def tab_grph(company):
  my = db.dictionizationoData(company=company)
  name = px.scatter(my, x="Months", y="ActualTax", trendline="ols")
  my_plot_div = plot(name, output_type='div')
  results = px.get_trendline_results(name)
  results = results.iloc[0]["px_fit_results"].summary()
  print(results)
  return render_template("graph.html", html=markupsafe.Markup(my_plot_div))


app.run(use_reloader=True, debug=True, port="1234")
