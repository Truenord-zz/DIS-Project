from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from PharmaMarket.forms import FilterDrugForm, AddDrugForm, BuyDrugForm, RestockDrugForm
from PharmaMarket.models import Drug as DrugModel, DrugOrder
from PharmaMarket.queries import insert_drug, get_drug_by_pk, Sell, \
    insert_sell, get_all_drug_by_pharmacist, get_drug_by_filters, insert_drug_order, update_sell, \
    get_orders_by_customer_pk

Drug = Blueprint('Drug', __name__)

@Drug.route("/drug", methods=['GET', 'POST'])
def drug():
    form = FilterDrugForm()
    title = 'Our drug!'
    drug = []
    if request.method == 'POST':
        drug = get_drug_by_filters(name=request.form.get('name'),
                                   brand=request.form.get('brand'),
                                   city=request.form.get('city'),
                                   pharmacist_name=request.form.get('sold_by'),
                                   price=request.form.get('price'))
        title = f'Our {request.form.get("name")}!'
    return render_template('pages/drug.html', drug=drug, form=form, title=title)

@Drug.route("/add-drug", methods=['GET', 'POST'])
@login_required
def add_drug():
    form = AddDrugForm(
        data=dict(pharmacist_pk=current_user.pk))
    if request.method == 'POST':
        if form.validate_on_submit():
            drug_data = dict(
                id=form.id.data,
                name=form.name.data,
                brand=form.brand.data,
                city=form.city.data,
                price=form.price.data
            )
            drug = DrugModel(drug_data)
            new_drug_pk = insert_drug(drug)
            sell = Sell(dict(pharmacist_pk=current_user.pk, drug_pk=new_drug_pk, available=True))
            insert_sell(sell)
    return render_template('pages/add-drug.html', form=form)


@Drug.route("/your-drug", methods=['GET', 'POST'])
@login_required
def your_drug():
    form = FilterDrugForm()
    drug = []
    if request.method == 'GET':
        drug = get_all_drug_by_pharmacist(current_user.pk)
    if request.method == 'POST':
        drug = get_drug_by_filters(name=request.form.get('name'),
                                   brand=request.form.get('brand'),
                                   price=request.form.get('price'),
                                   pharmacist_pk=current_user.pk)
    return render_template('pages/your-drug.html', form=form, drug=drug)


@Drug.route('/drug/buy/<pk>', methods=['GET', 'POST'])
@login_required
def buy_drug(pk):
    form = BuyDrugForm()
    drug = get_drug_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            order = DrugOrder(dict(drug_pk=drug.pk,
                                   pharmacist_pk=drug.pharmacist_pk,
                                   customer_pk=current_user.pk))
            insert_drug_order(order)
            update_sell(available=False,
                        drug_pk=drug.pk,
                        pharmacist_pk=drug.pharmacist_pk)
    return render_template('pages/buy-drug.html', form=form, drug=drug)


@Drug.route('/drug/restock/<pk>', methods=['GET', 'POST'])
@login_required
def restock_drug(pk):
    form = RestockDrugForm()
    drug = get_drug_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            update_sell(available=True,
                        drug_pk=drug.pk,
                        pharmacist_pk=drug.pharmacist_pk)
    return render_template('pages/restock-drug.html', form=form, drug=drug)


@Drug.route('/drug/your-orders')
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/your-orders.html', orders=orders)