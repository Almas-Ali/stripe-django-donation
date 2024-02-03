from django.shortcuts import render, redirect, reverse
from django.conf import settings

import stripe


def index(request):
	if request.method == 'POST':
		stripe.api_key = settings.STRIPE_PRIVATE_KEY
		# amount should be in cents. Stripe use amount in the smallest currency.
		amount = int(request.POST.get('amount')) * 100

		checkout = stripe.checkout.Session.create(
			line_items = [{
				'quantity': 1,
				'price_data': {
					'currency': 'usd',
					'product_data': {
						'name': 'Donation',
					},
					'unit_amount': amount
				}
			}],
			mode = 'payment',
			success_url = request.build_absolute_uri(reverse('success_donation')),
			cancel_url 	= request.build_absolute_uri(reverse('cancel_donation'))
		)
		return redirect(checkout.url, code=303)

	return render(request, 'donation/index.html')


def success_donation(request):
	return render(request, 'donation/success.html')


def cancel_donation(request):
	return render(request, 'donation/cancel.html')

