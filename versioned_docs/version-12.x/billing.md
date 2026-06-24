<!-- # Laravel Cashier (Stripe) -->
# Laravel Cashier (Stripe)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Currency Configuration](#currency-configuration)
    - [Tax Configuration](#tax-configuration)
    - [Logging](#logging)
    - [Using Custom Models](#using-custom-models)
- [Quickstart](#quickstart)
    - [Selling Products](#quickstart-selling-products)
    - [Selling Subscriptions](#quickstart-selling-subscriptions)
- [Customers](#customers)
    - [Retrieving Customers](#retrieving-customers)
    - [Creating Customers](#creating-customers)
    - [Updating Customers](#updating-customers)
    - [Balances](#balances)
    - [Tax IDs](#tax-ids)
    - [Syncing Customer Data With Stripe](#syncing-customer-data-with-stripe)
    - [Billing Portal](#billing-portal)
- [Payment Methods](#payment-methods)
    - [Storing Payment Methods](#storing-payment-methods)
    - [Retrieving Payment Methods](#retrieving-payment-methods)
    - [Payment Method Presence](#payment-method-presence)
    - [Updating the Default Payment Method](#updating-the-default-payment-method)
    - [Adding Payment Methods](#adding-payment-methods)
    - [Deleting Payment Methods](#deleting-payment-methods)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Changing Prices](#changing-prices)
    - [Subscription Quantity](#subscription-quantity)
    - [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)
    - [Multiple Subscriptions](#multiple-subscriptions)
    - [Usage Based Billing](#usage-based-billing)
    - [Subscription Taxes](#subscription-taxes)
    - [Subscription Anchor Date](#subscription-anchor-date)
    - [Canceling Subscriptions](#cancelling-subscriptions)
    - [Resuming Subscriptions](#resuming-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Payment Method Up Front](#with-payment-method-up-front)
    - [Without Payment Method Up Front](#without-payment-method-up-front)
    - [Extending Trials](#extending-trials)
- [Handling Stripe Webhooks](#handling-stripe-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
    - [Simple Charge](#simple-charge)
    - [Charge With Invoice](#charge-with-invoice)
    - [Creating Payment Intents](#creating-payment-intents)
    - [Refunding Charges](#refunding-charges)
- [Invoices](#invoices)
    - [Retrieving Invoices](#retrieving-invoices)
    - [Upcoming Invoices](#upcoming-invoices)
    - [Previewing Subscription Invoices](#previewing-subscription-invoices)
    - [Generating Invoice PDFs](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [Product Checkouts](#product-checkouts)
    - [Single Charge Checkouts](#single-charge-checkouts)
    - [Subscription Checkouts](#subscription-checkouts)
    - [Collecting Tax IDs](#collecting-tax-ids)
    - [Guest Checkouts](#guest-checkouts)
- [Handling Failed Payments](#handling-failed-payments)
    - [Confirming Payments](#confirming-payments)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [Payments Requiring Additional Confirmation](#payments-requiring-additional-confirmation)
    - [Off-session Payment Notifications](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe) provides an expressive, fluent interface to [Stripe's](https://stripe.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs. -->
[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe's](https://stripe.com) 구독 청구 서비스에 표현력이 풍부하고 유창한 인터페이스를 제공합니다. 작성하기 두려운 상용구 구독 청구 코드를 거의 모두 처리합니다. 기본 구독 관리 외에도 Cashier는 쿠폰, 구독 교환, 구독 "수량", 취소 유예 기간을 처리하고 송장 PDF를 생성할 수도 있습니다.

<a name="upgrading-cashier"></a>
<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md). -->
Cashier의 새 버전으로 업그레이드할 때는 [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md)를 주의 깊게 검토하는 것이 중요합니다.

> [!WARNING]
> 주요 변경을 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 16은 Stripe API 버전 `2025-06-30.basil`를 활용합니다. Stripe API 버전은 새로운 Stripe 기능과 개선 사항을 활용하기 위해 부 릴리스에서 업데이트될 예정입니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Stripe using the Composer package manager: -->
먼저 Composer 패키지 관리자를 사용하여 Stripe용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier
```

<!-- After installing the package, publish Cashier's migrations using the `vendor:publish` Artisan command: -->
패키지를 설치한 후 `vendor:publish` Artisan 명령을 사용하여 Cashier의 마이그레이션을 게시합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- Then, migrate your database: -->
그런 다음 데이터베이스를 마이그레이션합니다.

```shell
php artisan migrate
```

<!-- Cashier's migrations will add several columns to your `users` table. They will also create a new `subscriptions` table to hold all of your customer's subscriptions and a `subscription_items` table for subscriptions with multiple prices. -->
Cashier의 마이그레이션은 `users` 테이블에 여러 열을 추가합니다. 또한 고객의 모든 구독을 보관하기 위한 새로운 `subscriptions` 테이블과 다양한 가격의 구독을 위한 `subscription_items` 테이블을 생성합니다.

<!-- If you wish, you can also publish Cashier's configuration file using the `vendor:publish` Artisan command: -->
원하는 경우 `vendor:publish` Artisan 명령을 사용하여 Cashier의 구성 파일을 게시할 수도 있습니다.

```shell
php artisan vendor:publish --tag="cashier-config"
```

<!-- Lastly, to ensure Cashier properly handles all Stripe events, remember to [configure Cashier's webhook handling](#handling-stripe-webhooks). -->
마지막으로, Cashier가 모든 Stripe 이벤트를 올바르게 처리하도록 하려면 [configure Cashier's webhook handling](#handling-stripe-webhooks)을 기억하세요.

> [!WARNING]
> Stripe에서는 Stripe 식별자를 저장하는 데 사용되는 모든 열에서 대소문자를 구분할 것을 권장합니다. 따라서 MySQL을 사용할 때 `stripe_id` 열의 열 데이터 정렬이 `utf8_bin`로 설정되어 있는지 확인해야 합니다. 이에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인할 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>
<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, add the `Billable` trait to your billable model definition. Typically, this will be the `App\Models\User` model. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information: -->
Cashier를 사용하기 전에 청구 가능한 모델 정의에 `Billable` 트레이트를 추가하세요. 일반적으로 이는 `App\Models\User` 모델입니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트와 같은 일반적인 청구 작업을 수행할 수 있는 다양한 메서드를 제공합니다.

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- Cashier assumes your billable model will be the `App\Models\User` class that ships with Laravel. If you wish to change this you may specify a different model via the `useCustomerModel` method. This method should typically be called in the `boot` method of your `AppServiceProvider` class: -->
Cashier는 청구 가능한 모델이 Laravel와 함께 제공되는 `App\Models\User` 클래스라고 가정합니다. 이를 변경하려면 `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출되어야 합니다.

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> Laravel에서 제공한 `App\Models\User` 모델 이외의 모델을 사용하는 경우 대체 모델의 테이블 이름과 일치하도록 제공된 [Cashier migrations](#installation)를 게시하고 변경해야 합니다.

<a name="api-keys"></a>
<!-- ### API Keys -->
### API Keys

<!-- Next, you should configure your Stripe API keys in your application's `.env` file. You can retrieve your Stripe API keys from the Stripe control panel: -->
다음으로, 애플리케이션의 `.env` 파일에서 Stripe API 키를 구성해야 합니다. Stripe 제어판에서 Stripe API 키를 검색할 수 있습니다.

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 정의되어 있는지 확인해야 합니다. 이 변수는 들어오는 웹후크가 실제로 Stripe에서 오는지 확인하는 데 사용되기 때문입니다.

<a name="currency-configuration"></a>
<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
기본 Cashier 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일 내에서 `CASHIER_CURRENCY` 환경 변수를 설정하여 기본 통화를 변경할 수 있습니다.

```ini
CASHIER_CURRENCY=eur
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
Cashier의 통화를 구성하는 것 외에도 송장에 표시할 화폐 값의 형식을 지정할 때 사용할 로케일을 지정할 수도 있습니다. 내부적으로 Cashier는 [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php)를 활용하여 통화 로케일을 설정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로캘을 사용하려면 `ext-intl` PHP 확장이 서버에 설치 및 구성되어 있는지 확인하세요.

<a name="tax-configuration"></a>
<!-- ### Tax Configuration -->
### Tax Configuration

<!-- Thanks to [Stripe Tax](https://stripe.com/tax), it's possible to automatically calculate taxes for all invoices generated by Stripe. You can enable automatic tax calculation by invoking the `calculateTaxes` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
[Stripe Tax](https://stripe.com/tax) 덕분에 Stripe에서 생성된 모든 송장에 대한 세금을 자동으로 계산할 수 있습니다. 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하여 자동 세금 계산을 활성화할 수 있습니다.

```php
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

<!-- Once tax calculation has been enabled, any new subscriptions and any one-off invoices that are generated will receive automatic tax calculation. -->
세금 계산이 활성화되면 모든 신규 구독과 생성된 일회성 송장에 자동 세금 계산이 적용됩니다.

<!-- For this feature to work properly, your customer's billing details, such as the customer's name, address, and tax ID, need to be synced to Stripe. You may use the [customer data synchronization](#syncing-customer-data-with-stripe) and [Tax ID](#tax-ids) methods offered by Cashier to accomplish this. -->
이 기능이 제대로 작동하려면 고객 이름, 주소, 세금 ID 등 고객의 청구 세부정보를 Stripe에 동기화해야 합니다. 이를 수행하려면 Cashier에서 제공하는 [customer data synchronization](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 메서드를 사용할 수 있습니다.

<a name="logging"></a>
<!-- ### Logging -->
### Logging

<!-- Cashier allows you to specify the log channel to be used when logging fatal Stripe errors. You may specify the log channel by defining the `CASHIER_LOGGER` environment variable within your application's `.env` file: -->
Cashier를 사용하면 치명적인 Stripe 오류를 기록할 때 사용할 로그 채널을 지정할 수 있습니다. 애플리케이션의 `.env` 파일 내에서 `CASHIER_LOGGER` 환경 변수를 정의하여 로그 채널을 지정할 수 있습니다.

```ini
CASHIER_LOGGER=stack
```

<!-- Exceptions that are generated by API calls to Stripe will be logged through your application's default log channel. -->
Stripe에 대한 API 호출로 생성된 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
<!-- ### Using Custom Models -->
### Using Custom Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
자신만의 모델을 정의하고 해당 Cashier 모델을 확장하여 Cashier에서 내부적으로 사용되는 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Cashier\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
모델을 정의한 후 `Laravel\Cashier\Cashier` 클래스를 통해 사용자 지정 모델을 사용하도록 Cashier에 지시할 수 있습니다. 일반적으로 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 사용자 지정 모델에 대해 Cashier에 알려야 합니다.

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```

<a name="quickstart"></a>
<!-- ## Quickstart -->
## Quickstart

<a name="quickstart-selling-products"></a>
<!-- ### Selling Products -->
### Selling Products

> [!NOTE]
> Stripe Checkout을 활용하기 전에 Stripe 대시보드에서 고정 가격으로 제품을 정의해야 합니다. 또한 [configure Cashier's webhook handling](#handling-stripe-webhooks)해야 합니다.

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations. -->
애플리케이션을 통해 제품 및 구독 청구를 제공하는 것은 어려울 수 있습니다. 그러나 Cashier 및 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 현대적이고 강력한 결제 통합을 쉽게 구축할 수 있습니다.

<!-- To charge customers for non-recurring, single-charge products, we'll utilize Cashier to direct customers to Stripe Checkout, where they will provide their payment details and confirm their purchase. Once the payment has been made via Checkout, the customer will be redirected to a success URL of your choosing within your application: -->
반복되지 않는 단일 청구 제품에 대해 고객에게 비용을 청구하기 위해 Cashier를 활용하여 고객을 Stripe Checkout으로 안내합니다. 여기서 고객은 결제 세부 정보를 제공하고 구매를 확인하게 됩니다. Checkout을 통해 결제가 완료되면 고객은 애플리케이션 내에서 선택한 성공 URL로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/checkout', function (Request $request) {
    $stripePriceId = 'price_deluxe_album';

    $quantity = 1;

    return $request->user()->checkout([$stripePriceId => $quantity], [
        'success_url' => route('checkout-success'),
        'cancel_url' => route('checkout-cancel'),
    ]);
})->name('checkout');

Route::view('/checkout/success', 'checkout.success')->name('checkout-success');
Route::view('/checkout/cancel', 'checkout.cancel')->name('checkout-cancel');
```

<!-- As you can see in the example above, we will utilize Cashier's provided `checkout` method to redirect the customer to Stripe Checkout for a given "price identifier". When using Stripe, "prices" refer to [defined prices for specific products](https://stripe.com/docs/products-prices/how-products-and-prices-work). -->
위의 예에서 볼 수 있듯이 Cashier에서 제공하는 `checkout` 메서드를 활용하여 지정된 "가격 식별자"에 대해 고객을 Stripe Checkout으로 리디렉션합니다. Stripe 사용 시 "가격"은 [defined prices for specific products](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

<!-- If necessary, the `checkout` method will automatically create a customer in Stripe and connect that Stripe customer record to the corresponding user in your application's database. After completing the checkout session, the customer will be redirected to a dedicated success or cancellation page where you can display an informational message to the customer. -->
필요한 경우 `checkout` 메서드는 자동으로 Stripe에 고객을 생성하고 해당 Stripe 고객 레코드를 애플리케이션 데이터베이스의 해당 사용자에 연결합니다. 결제 세션을 완료한 후 고객은 고객에게 정보 메시지를 표시할 수 있는 전용 성공 또는 취소 페이지로 리디렉션됩니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
<!-- #### Providing Meta Data to Stripe Checkout -->
#### Providing Meta Data to Stripe Checkout

<!-- When selling products, it's common to keep track of completed orders and purchased products via `Cart` and `Order` models defined by your own application. When redirecting customers to Stripe Checkout to complete a purchase, you may need to provide an existing order identifier so that you can associate the completed purchase with the corresponding order when the customer is redirected back to your application. -->
제품을 판매할 때 자체 애플리케이션에서 정의한 `Cart` 및 `Order` 모델을 통해 완료된 주문과 구매한 제품을 추적하는 것이 일반적입니다. 구매를 완료하기 위해 고객을 Stripe Checkout으로 리디렉션할 때 고객이 애플리케이션으로 다시 리디렉션될 때 완료된 구매를 해당 주문과 연결할 수 있도록 기존 주문 식별자를 제공해야 할 수도 있습니다.

<!-- To accomplish this, you may provide an array of `metadata` to the `checkout` method. Let's imagine that a pending `Order` is created within our application when a user begins the checkout process. Remember, the `Cart` and `Order` models in this example are illustrative and not provided by Cashier. You are free to implement these concepts based on the needs of your own application: -->
이를 달성하기 위해 `metadata` 배열을 `checkout` 메서드에 제공할 수 있습니다. 사용자가 결제 프로세스를 시작할 때 애플리케이션 내에서 보류 중인 `Order`가 생성된다고 가정해 보겠습니다. 이 예의 `Cart` 및 `Order` 모델은 설명을 위한 것이며 Cashier에서 제공되지 않습니다. 자신의 애플리케이션 요구 사항에 따라 다음 개념을 자유롭게 구현할 수 있습니다.

```php
use App\Models\Cart;
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/cart/{cart}/checkout', function (Request $request, Cart $cart) {
    $order = Order::create([
        'cart_id' => $cart->id,
        'price_ids' => $cart->price_ids,
        'status' => 'incomplete',
    ]);

    return $request->user()->checkout($order->price_ids, [
        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => route('checkout-cancel'),
        'metadata' => ['order_id' => $order->id],
    ]);
})->name('checkout');
```

<!-- As you can see in the example above, when a user begins the checkout process, we will provide all of the cart / order's associated Stripe price identifiers to the `checkout` method. Of course, your application is responsible for associating these items with the "shopping cart" or order as a customer adds them. We also provide the order's ID to the Stripe Checkout session via the `metadata` array. Finally, we have added the `CHECKOUT_SESSION_ID` template variable to the Checkout success route. When Stripe redirects customers back to your application, this template variable will automatically be populated with the Checkout session ID. -->
위의 예에서 볼 수 있듯이 사용자가 결제 프로세스를 시작하면 장바구니/주문과 관련된 모든 Stripe 가격 식별자를 `checkout` 메서드에 제공합니다. 물론 애플리케이션은 이러한 항목을 "장바구니"와 연결하거나 고객이 항목을 추가할 때 주문하는 일을 담당합니다. 또한 `metadata` 배열을 통해 Stripe Checkout 세션에 주문 ID를 제공합니다. 마지막으로 Checkout 성공 라우트에 `CHECKOUT_SESSION_ID` 템플릿 변수를 추가했습니다. Stripe가 고객을 애플리케이션으로 다시 리디렉션하면 이 템플릿 변수가 자동으로 Checkout 세션 ID로 채워집니다.

<!-- Next, let's build the Checkout success route. This is the route that users will be redirected to after their purchase has been completed via Stripe Checkout. Within this route, we can retrieve the Stripe Checkout session ID and the associated Stripe Checkout instance in order to access our provided meta data and update our customer's order accordingly: -->
다음으로 Checkout 성공 라우트를 구축해 보겠습니다. Stripe 체크아웃을 통해 구매가 완료된 후 사용자가 리디렉션되는 라우트입니다. 이 라우트 내에서 제공된 메타 데이터에 액세스하고 그에 따라 고객의 주문을 업데이트하기 위해 Stripe Checkout 세션 ID 및 연결된 Stripe Checkout 인스턴스를 검색할 수 있습니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;
use Laravel\Cashier\Cashier;

Route::get('/checkout/success', function (Request $request) {
    $sessionId = $request->get('session_id');

    if ($sessionId === null) {
        return;
    }

    $session = Cashier::stripe()->checkout->sessions->retrieve($sessionId);

    if ($session->payment_status !== 'paid') {
        return;
    }

    $orderId = $session['metadata']['order_id'] ?? null;

    $order = Order::findOrFail($orderId);

    $order->update(['status' => 'completed']);

    return view('checkout-success', ['order' => $order]);
})->name('checkout-success');
```

<!-- Please refer to Stripe's documentation for more information on the [data contained by the Checkout session object](https://stripe.com/docs/api/checkout/sessions/object). -->
[data contained by the Checkout session object](https://stripe.com/docs/api/checkout/sessions/object)에 대한 자세한 내용은 Stripe의 설명서를 참조하세요.

<a name="quickstart-selling-subscriptions"></a>
<!-- ### Selling Subscriptions -->
### Selling Subscriptions

> [!NOTE]
> Stripe Checkout을 활용하기 전에 Stripe 대시보드에서 고정 가격으로 제품을 정의해야 합니다. 또한 [configure Cashier's webhook handling](#handling-stripe-webhooks)해야 합니다.

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations. -->
애플리케이션을 통해 제품 및 구독 청구를 제공하는 것은 어려울 수 있습니다. 그러나 Cashier 및 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 현대적이고 강력한 결제 통합을 쉽게 구축할 수 있습니다.

<!-- To learn how to sell subscriptions using Cashier and Stripe Checkout, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Stripe dashboard. In addition, our subscription service might offer an Expert plan as `pro_expert`. -->
Cashier 및 Stripe Checkout을 사용하여 구독을 판매하는 방법을 알아보려면 기본 월별(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 요금제를 사용하는 구독 서비스의 간단한 시나리오를 고려해 보겠습니다. 이 두 가지 가격은 Stripe 대시보드의 "기본" 제품(`pro_basic`)으로 그룹화될 수 있습니다. 또한 당사의 구독 서비스에서는 `pro_expert`와 같은 Expert 플랜을 제공할 수도 있습니다.

<!-- First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button or link should direct the user to a Laravel route which creates the Stripe Checkout session for their chosen plan: -->
먼저 고객이 당사 서비스에 가입할 수 있는 방법을 살펴보겠습니다. 물론 고객이 애플리케이션 가격 페이지에서 기본 요금제에 대한 "구독" 버튼을 클릭할 수도 있다고 상상할 수 있습니다. 이 버튼 또는 링크는 선택한 계획에 대한 Stripe 체크아웃 세션을 생성하는 Laravel 라우트로 사용자를 연결해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_basic_monthly')
        ->trialDays(5)
        ->allowPromotionCodes()
        ->checkout([
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

<!-- As you can see in the example above, we will redirect the customer to a Stripe Checkout session which will allow them to subscribe to our Basic plan. After a successful checkout or cancellation, the customer will be redirected back to the URL we provided to the `checkout` method. To know when their subscription has actually started (since some payment methods require a few seconds to process), we'll also need to [configure Cashier's webhook handling](#handling-stripe-webhooks). -->
위의 예에서 볼 수 있듯이 고객을 Stripe Checkout 세션으로 리디렉션하여 기본 플랜을 구독할 수 있도록 합니다. 성공적으로 체크아웃하거나 취소한 후 고객은 `checkout` 메서드에 제공한 URL로 다시 리디렉션됩니다. 구독이 실제로 언제 시작되었는지 확인하려면(일부 결제 수단을 처리하는 데 몇 초가 걸리기 때문에) [configure Cashier's webhook handling](#handling-stripe-webhooks)도 필요합니다.

<!-- Now that customers can start subscriptions, we need to restrict certain portions of our application so that only subscribed users can access them. Of course, we can always determine a user's current subscription status via the `subscribed` method provided by Cashier's `Billable` trait: -->
이제 고객이 구독을 시작할 수 있으므로 구독한 사용자만 액세스할 수 있도록 애플리케이션의 특정 부분을 제한해야 합니다. 물론, Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 통해 언제든지 사용자의 현재 구독 상태를 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

<!-- We can even easily determine if a user is subscribed to specific product or price: -->
사용자가 특정 제품이나 가격을 구독하는지 쉽게 확인할 수도 있습니다.

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
<!-- #### Building a Subscribed Middleware -->
#### Building a Subscribed Middleware

<!-- For convenience, you may wish to create a [middleware](/docs/12.x/middleware) which determines if the incoming request is from a subscribed user. Once this middleware has been defined, you may easily assign it to a route to prevent users that are not subscribed from accessing the route: -->
편의를 위해 수신 요청이 구독 사용자로부터 오는 것인지 확인하는 [middleware](/docs/12.x/middleware)를 생성할 수 있습니다. 이 미들웨어가 정의되면 이를 라우트에 쉽게 할당하여 구독하지 않은 사용자가 라우트에 액세스하지 못하도록 방지할 수 있습니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class Subscribed
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->subscribed()) {
            // Redirect user to billing page and ask them to subscribe...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

<!-- Once the middleware has been defined, you may assign it to a route: -->
미들웨어가 정의되면 이를 라우트에 할당할 수 있습니다.

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
<!-- #### Allowing Customers to Manage Their Billing Plan -->
#### Allowing Customers to Manage Their Billing Plan

<!-- Of course, customers may want to change their subscription plan to another product or "tier". The easiest way to allow this is by directing customers to Stripe's [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal), which provides a hosted user interface that allows customers to download invoices, update their payment method, and change subscription plans. -->
물론 고객은 구독 계획을 다른 제품이나 "계층"으로 변경하기를 원할 수도 있습니다. 이를 허용하는 가장 쉬운 방법은 고객을 Stripe의 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)로 안내하는 것입니다. 이 포털에서는 고객이 송장을 다운로드하고, 결제 수단을 업데이트하고, 구독 요금제를 변경할 수 있는 호스팅된 사용자 인터페이스를 제공합니다.

<!-- First, define a link or button within your application that directs users to a Laravel route which we will utilize to initiate a Billing Portal session: -->
먼저, 청구 포털 세션을 시작하는 데 활용할 Laravel 라우트로 사용자를 안내하는 링크나 버튼을 애플리케이션 내에서 정의합니다.

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

<!-- Next, let's define the route that initiates a Stripe Customer Billing Portal session and redirects the user to the Portal. The `redirectToBillingPortal` method accepts the URL that users should be returned to when exiting the Portal: -->
다음으로, Stripe 고객 청구 포털 세션을 시작하고 사용자를 포털로 리디렉션하는 라우트를 정의해 보겠습니다. `redirectToBillingPortal` 메서드는 포털을 종료할 때 사용자가 반환되어야 하는 URL를 허용합니다.

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 웹훅 ​​처리를 구성한 한, Cashier는 Stripe에서 들어오는 웹훅을 검사하여 자동으로 애플리케이션의 계산원 관련 데이터베이스 테이블을 동기화된 상태로 유지합니다. 예를 들어 사용자가 Stripe의 고객 청구 포털을 통해 구독을 취소하면 Cashier는 해당 웹후크를 수신하고 애플리케이션 데이터베이스에서 구독을 "취소됨"으로 표시합니다.

<a name="customers"></a>
<!-- ## Customers -->
## Customers

<a name="retrieving-customers"></a>
<!-- ### Retrieving Customers -->
### Retrieving Customers

<!-- You can retrieve a customer by their Stripe ID using the `Cashier::findBillable` method. This method will return an instance of the billable model: -->
`Cashier::findBillable` 메서드를 사용하여 Stripe ID로 고객을 검색할 수 있습니다. 이 메서드는 청구 가능한 모델의 인스턴스를 반환합니다.

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
<!-- ### Creating Customers -->
### Creating Customers

<!-- Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method: -->
경우에 따라 구독을 시작하지 않고 Stripe 고객을 생성하고 싶을 수 있습니다. `createAsStripeCustomer` 메서드를 사용하여 이 작업을 수행할 수 있습니다.

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

<!-- Once the customer has been created in Stripe, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create): -->
Stripe에서 고객이 생성되면 나중에 구독을 시작할 수 있습니다. 추가 [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create)를 전달하기 위해 선택적 `$options` 배열을 제공할 수 있습니다.

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

<!-- You may use the `asStripeCustomer` method if you want to return the Stripe customer object for a billable model: -->
청구 가능한 모델에 대해 Stripe 고객 개체를 반환하려는 경우 `asStripeCustomer` 메서드를 사용할 수 있습니다.

```php
$stripeCustomer = $user->asStripeCustomer();
```

<!-- The `createOrGetStripeCustomer` method may be used if you would like to retrieve the Stripe customer object for a given billable model but are not sure whether the billable model is already a customer within Stripe. This method will create a new customer in Stripe if one does not already exist: -->
지정된 청구 가능 모델에 대한 Stripe 고객 개체를 검색하고 싶지만 청구 가능 모델이 이미 Stripe 내의 고객인지 확실하지 않은 경우 `createOrGetStripeCustomer` 메서드를 사용할 수 있습니다. 이 메서드는 아직 존재하지 않는 경우 Stripe에 새 고객을 생성합니다.

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
<!-- ### Updating Customers -->
### Updating Customers

<!-- Occasionally, you may wish to update the Stripe customer directly with additional information. You may accomplish this using the `updateStripeCustomer` method. This method accepts an array of [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update): -->
경우에 따라 Stripe 고객에게 추가 정보를 직접 업데이트하고 싶을 수도 있습니다. `updateStripeCustomer` 메서드를 사용하여 이 작업을 수행할 수 있습니다. 이 메서드는 [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update) 배열을 허용합니다.

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
<!-- ### Balances -->
### Balances

<!-- Stripe allows you to credit or debit a customer's "balance". Later, this balance will be credited or debited on new invoices. To check the customer's total balance you may use the `balance` method that is available on your billable model. The `balance` method will return a formatted string representation of the balance in the customer's currency: -->
Stripe를 사용하면 고객의 "잔액"을 입금하거나 출금할 수 있습니다. 나중에 이 잔액은 새 송장에 기입되거나 차감됩니다. 고객의 총 잔액을 확인하려면 청구 가능한 모델에서 사용할 수 있는 `balance` 메서드를 사용할 수 있습니다. `balance` 메서드는 고객의 통화 잔액을 형식화된 문자열 표현으로 반환합니다.

```php
$balance = $user->balance();
```

<!-- To credit a customer's balance, you may provide a value to the `creditBalance` method. If you wish, you may also provide a description: -->
고객의 잔액을 적립하려면 `creditBalance` 메서드에 값을 제공할 수 있습니다. 원하는 경우 설명을 제공할 수도 있습니다.

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

<!-- Providing a value to the `debitBalance` method will debit the customer's balance: -->
`debitBalance` 메서드에 값을 제공하면 고객 잔액이 인출됩니다.

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

<!-- The `applyBalance` method will create new customer balance transactions for the customer. You may retrieve these transaction records using the `balanceTransactions` method, which may be useful in order to provide a log of credits and debits for the customer to review: -->
`applyBalance` 메서드는 고객을 위한 새로운 고객 잔액 거래를 생성합니다. `balanceTransactions` 메서드를 사용하여 이러한 거래 기록을 검색할 수 있습니다. 이는 고객이 검토할 대변 및 차변 로그를 제공하는 데 유용할 수 있습니다.

```php
// Retrieve all transactions...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // Transaction amount...
    $amount = $transaction->amount(); // $2.31

    // Retrieve the related invoice when available...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
<!-- ### Tax IDs -->
### Tax IDs

<!-- Cashier offers an easy way to manage a customer's tax IDs. For example, the `taxIds` method may be used to retrieve all of the [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object) that are assigned to a customer as a collection: -->
Cashier는 고객의 세금 ID를 관리하는 쉬운 방법을 제공합니다. 예를 들어, `taxIds` 메서드를 사용하여 고객에게 컬렉션으로 할당된 모든 [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object)를 검색할 수 있습니다.

```php
$taxIds = $user->taxIds();
```

<!-- You can also retrieve a specific tax ID for a customer by its identifier: -->
식별자로 고객의 특정 세금 ID를 검색할 수도 있습니다.

```php
$taxId = $user->findTaxId('txi_belgium');
```

<!-- You may create a new Tax ID by providing a valid [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) and value to the `createTaxId` method: -->
유효한 [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) 및 값을 `createTaxId` 메서드에 제공하여 새 세금 ID를 생성할 수 있습니다.

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

<!-- The `createTaxId` method will immediately add the VAT ID to the customer's account. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); however, this is an asynchronous process. You can be notified of verification updates by subscribing to the `customer.tax_id.updated` webhook event and inspecting [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). For more information on handling webhooks, please consult the [documentation on defining webhook handlers](#handling-stripe-webhooks). -->
`createTaxId` 메서드는 VAT ID를 고객 계정에 즉시 추가합니다. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); 그러나 이는 비동기 프로세스입니다. `customer.tax_id.updated` 웹훅 이벤트를 구독하고 [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 검사하면 검증 업데이트 알림을 받을 수 있습니다. 웹훅 처리에 대한 자세한 내용은 [documentation on defining webhook handlers](#handling-stripe-webhooks)를 참조하세요.

<!-- You may delete a tax ID using the `deleteTaxId` method: -->
`deleteTaxId` 메서드를 사용하여 세금 ID를 삭제할 수 있습니다.

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
<!-- ### Syncing Customer Data With Stripe -->
### Syncing Customer Data With Stripe

<!-- Typically, when your application's users update their name, email address, or other information that is also stored by Stripe, you should inform Stripe of the updates. By doing so, Stripe's copy of the information will be in sync with your application's. -->
일반적으로 애플리케이션 사용자가 이름, 이메일 주소 또는 Stripe에 저장되어 있는 기타 정보를 업데이트하는 경우 Stripe에 업데이트 내용을 알려야 합니다. 이렇게 하면 Stripe의 정보 사본이 귀하의 애플리케이션 정보와 동기화됩니다.

<!-- To automate this, you may define an event listener on your billable model that reacts to the model's `updated` event. Then, within your event listener, you may invoke the `syncStripeCustomerDetails` method on the model: -->
이를 자동화하려면 모델의 `updated` 이벤트에 반응하는 청구 가능한 모델에 이벤트 리스너를 정의할 수 있습니다. 그런 다음 이벤트 리스너 내에서 모델의 `syncStripeCustomerDetails` 메서드를 호출할 수 있습니다.

```php
use App\Models\User;
use function Illuminate\Events\queueable;

/**
 * The "booted" method of the model.
 */
protected static function booted(): void
{
    static::updated(queueable(function (User $customer) {
        if ($customer->hasStripeId()) {
            $customer->syncStripeCustomerDetails();
        }
    }));
}
```

<!-- Now, every time your customer model is updated, its information will be synced with Stripe. For convenience, Cashier will automatically sync your customer's information with Stripe on the initial creation of the customer. -->
이제 고객 모델이 업데이트될 때마다 해당 정보가 Stripe와 동기화됩니다. 편의를 위해 Cashier는 고객을 처음 생성할 때 고객 정보를 Stripe와 자동으로 동기화합니다.

<!-- You may customize the columns used for syncing customer information to Stripe by overriding a variety of methods provided by Cashier. For example, you may override the `stripeName` method to customize the attribute that should be considered the customer's "name" when Cashier syncs customer information to Stripe: -->
Cashier에서 제공하는 다양한 메서드를 재정의하여 고객 정보를 Stripe에 동기화하는 데 사용되는 열을 사용자 지정할 수 있습니다. 예를 들어, Cashier가 고객 정보를 Stripe에 동기화할 때 고객의 "이름"으로 간주되어야 하는 속성을 사용자 지정하기 위해 `stripeName` 메서드를 재정의할 수 있습니다.

```php
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

<!-- Similarly, you may override the `stripeEmail`, `stripePhone` (20 character maximum), `stripeAddress`, and `stripePreferredLocales` methods. These methods will sync information to their corresponding customer parameters when [updating the Stripe customer object](https://stripe.com/docs/api/customers/update). If you wish to take total control over the customer information sync process, you may override the `syncStripeCustomerDetails` method. -->
마찬가지로 `stripeEmail`, `stripePhone`(최대 20자), `stripeAddress` 및 `stripePreferredLocales` 메서드를 재정의할 수 있습니다. 이러한 메서드는 [updating the Stripe customer object](https://stripe.com/docs/api/customers/update) 시 해당 고객 매개변수에 정보를 동기화합니다. 고객 정보 동기화 프로세스를 완전히 제어하려면 `syncStripeCustomerDetails` 메서드를 재정의할 수 있습니다.

<a name="billing-portal"></a>
<!-- ### Billing Portal -->
### Billing Portal

<!-- Stripe offers [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) so that your customer can manage their subscription, payment methods, and view their billing history. You can redirect your users to the billing portal by invoking the `redirectToBillingPortal` method on the billable model from a controller or route: -->
Stripe는 고객이 구독, 결제 수단 및 청구 내역을 뷰 관리할 수 있도록 [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 컨트롤러 또는 라우트에서 청구 가능한 모델에 대해 `redirectToBillingPortal` 메서드를 호출하여 사용자를 청구 포털로 리디렉션할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

<!-- By default, when the user is finished managing their subscription, they will be able to return to the `home` route of your application via a link within the Stripe billing portal. You may provide a custom URL that the user should return to by passing the URL as an argument to the `redirectToBillingPortal` method: -->
기본적으로 사용자가 구독 관리를 마치면 Stripe 청구 포털 내의 링크를 통해 애플리케이션의 `home` 라우트로 돌아갈 수 있습니다. URL를 `redirectToBillingPortal` 메서드에 인수로 전달하여 사용자가 반환해야 하는 사용자 지정 URL를 제공할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

<!-- If you would like to generate the URL to the billing portal without generating an HTTP redirect response, you may invoke the `billingPortalUrl` method: -->
HTTP 리디렉션 응답을 생성하지 않고 청구 포털에 URL를 생성하려는 경우 `billingPortalUrl` 메서드를 호출할 수 있습니다.

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
<!-- ## Payment Methods -->
## Payment Methods

<a name="storing-payment-methods"></a>
<!-- ### Storing Payment Methods -->
### Storing Payment Methods

<!-- In order to create subscriptions or perform "one-off" charges with Stripe, you will need to store a payment method and retrieve its identifier from Stripe. The approach used to accomplish this differs based on whether you plan to use the payment method for subscriptions or single charges, so we will examine both below. -->
Stripe를 사용하여 구독을 생성하거나 "일회성" 청구를 수행하려면 결제 수단을 저장하고 Stripe에서 해당 식별자를 검색해야 합니다. 이를 달성하는 데 사용되는 접근 방식은 구독 또는 단일 청구에 대한 결제 수단을 사용할지 여부에 따라 다르므로 아래에서 두 가지를 모두 검토하겠습니다.

<a name="payment-methods-for-subscriptions"></a>
<!-- #### Payment Methods for Subscriptions -->
#### Payment Methods for Subscriptions

<!-- When storing a customer's credit card information for future use by a subscription, the Stripe "Setup Intents" API must be used to securely gather the customer's payment method details. A "Setup Intent" indicates to Stripe the intention to charge a customer's payment method. Cashier's `Billable` trait includes the `createSetupIntent` method to easily create a new Setup Intent. You should invoke this method from the route or controller that will render the form which gathers your customer's payment method details: -->
나중에 구독을 통해 사용할 수 있도록 고객의 신용 카드 정보를 저장할 때 Stripe "설정 의도" API를 사용하여 고객의 결제 수단 세부 정보를 안전하게 수집해야 합니다. "설정 의도"는 Stripe에 고객의 결제 수단으로 요금을 청구하려는 의도를 나타냅니다. Cashier의 `Billable` 트레이트에는 새로운 설정 의도를 쉽게 생성할 수 있는 `createSetupIntent` 메서드가 포함되어 있습니다. 고객의 결제 수단 세부정보를 수집하는 양식을 렌더링하는 라우트 또는 컨트롤러에서 이 메서드를 호출해야 합니다.

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

<!-- After you have created the Setup Intent and passed it to the view, you should attach its secret to the element that will gather the payment method. For example, consider this "update payment method" form: -->
설정 인텐트를 생성하여 뷰에 전달한 후에는 결제 수단을 수집할 요소에 해당 비밀 정보를 첨부해야 합니다. 예를 들어 다음 "결제 수단 업데이트" 양식을 고려해 보세요.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

<!-- Next, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
다음으로, Stripe.js 라이브러리를 사용하여 [Stripe Element](https://stripe.com/docs/stripe-js)를 양식에 첨부하고 고객의 결제 세부정보를 안전하게 수집할 수 있습니다.

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

<!-- Next, the card can be verified and a secure "payment method identifier" can be retrieved from Stripe using [Stripe's `confirmCardSetup` method](https://stripe.com/docs/js/setup_intents/confirm_card_setup): -->
다음으로, 카드를 확인하고 [Stripe's `confirmCardSetup` method](https://stripe.com/docs/js/setup_intents/confirm_card_setup)을 사용하여 Stripe에서 안전한 "결제 수단 식별자"를 검색할 수 있습니다.

```js
const cardHolderName = document.getElementById('card-holder-name');
const cardButton = document.getElementById('card-button');
const clientSecret = cardButton.dataset.secret;

cardButton.addEventListener('click', async (e) => {
    const { setupIntent, error } = await stripe.confirmCardSetup(
        clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: { name: cardHolderName.value }
            }
        }
    );

    if (error) {
        // Display "error.message" to the user...
    } else {
        // The card has been verified successfully...
    }
});
```

<!-- After the card has been verified by Stripe, you may pass the resulting `setupIntent.payment_method` identifier to your Laravel application, where it can be attached to the customer. The payment method can either be [added as a new payment method](#adding-payment-methods) or [used to update the default payment method](#updating-the-default-payment-method). You can also immediately use the payment method identifier to [create a new subscription](#creating-subscriptions). -->
Stripe에서 카드를 확인한 후 결과 `setupIntent.payment_method` 식별자를 Laravel 애플리케이션에 전달하여 고객에게 연결할 수 있습니다. 결제 수단은 [added as a new payment method](#adding-payment-methods)하거나 [used to update the default payment method](#updating-the-default-payment-method)할 수 있습니다. 또한 결제 수단 식별자를 즉시 ​​사용하여 [create a new subscription](#creating-subscriptions)할 수도 있습니다.

> [!NOTE]
> 설정 의도 및 고객 결제 세부정보 수집에 대한 자세한 내용을 보려면 [review this overview provided by Stripe](https://stripe.com/docs/payments/save-and-reuse#php)하세요.

<a name="payment-methods-for-single-charges"></a>
<!-- #### Payment Methods for Single Charges -->
#### Payment Methods for Single Charges

<!-- Of course, when making a single charge against a customer's payment method, we will only need to use a payment method identifier once. Due to Stripe limitations, you may not use the stored default payment method of a customer for single charges. You must allow the customer to enter their payment method details using the Stripe.js library. For example, consider the following form: -->
물론 고객의 결제 수단에 대해 단일 요금을 청구하는 경우 결제 수단 식별자는 한 번만 사용하면 됩니다. Stripe 제한으로 인해 단일 청구에 대해 고객의 저장된 기본 결제 수단을 사용할 수 없습니다. 고객이 Stripe.js 라이브러리를 사용하여 결제 수단 세부정보를 입력할 수 있도록 허용해야 합니다. 예를 들어 다음 형식을 고려해보세요.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

<!-- After defining such a form, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
이러한 양식을 정의한 후 Stripe.js 라이브러리를 사용하여 [Stripe Element](https://stripe.com/docs/stripe-js)를 양식에 첨부하고 고객의 결제 세부정보를 안전하게 수집할 수 있습니다.

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

<!-- Next, the card can be verified and a secure "payment method identifier" can be retrieved from Stripe using [Stripe's `createPaymentMethod` method](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method): -->
다음으로, 카드를 확인하고 [Stripe's `createPaymentMethod` method](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method)을 사용하여 Stripe에서 안전한 "결제 수단 식별자"를 검색할 수 있습니다.

```js
const cardHolderName = document.getElementById('card-holder-name');
const cardButton = document.getElementById('card-button');

cardButton.addEventListener('click', async (e) => {
    const { paymentMethod, error } = await stripe.createPaymentMethod(
        'card', cardElement, {
            billing_details: { name: cardHolderName.value }
        }
    );

    if (error) {
        // Display "error.message" to the user...
    } else {
        // The card has been verified successfully...
    }
});
```

<!-- If the card is verified successfully, you may pass the `paymentMethod.id` to your Laravel application and process a [single charge](#simple-charge). -->
카드가 성공적으로 인증되면 `paymentMethod.id`를 Laravel 애플리케이션에 전달하고 [single charge](#simple-charge)를 처리할 수 있습니다.

<a name="retrieving-payment-methods"></a>
<!-- ### Retrieving Payment Methods -->
### Retrieving Payment Methods

<!-- The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances: -->
청구 가능한 모델 인스턴스의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다.

```php
$paymentMethods = $user->paymentMethods();
```

<!-- By default, this method will return payment methods of every type. To retrieve payment methods of a specific type, you may pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 모든 유형의 결제 수단을 반환합니다. 특정 유형의 결제 수단을 검색하려면 `type`를 메서드에 대한 인수로 전달할 수 있습니다.

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

<!-- To retrieve the customer's default payment method, the `defaultPaymentMethod` method may be used: -->
고객의 기본 결제 수단을 검색하려면 `defaultPaymentMethod` 메서드를 사용할 수 있습니다.

```php
$paymentMethod = $user->defaultPaymentMethod();
```

<!-- You can retrieve a specific payment method that is attached to the billable model using the `findPaymentMethod` method: -->
`findPaymentMethod` 메서드를 사용하여 청구 가능한 모델에 연결된 특정 결제 수단을 검색할 수 있습니다.

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
<!-- ### Payment Method Presence -->
### Payment Method Presence

<!-- To determine if a billable model has a default payment method attached to their account, invoke the `hasDefaultPaymentMethod` method: -->
청구 가능한 모델의 계정에 기본 결제 수단이 연결되어 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 호출하세요.

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

<!-- You may use the `hasPaymentMethod` method to determine if a billable model has at least one payment method attached to their account: -->
`hasPaymentMethod` 메서드를 사용하여 청구 가능한 모델의 계정에 하나 이상의 결제 수단이 연결되어 있는지 확인할 수 있습니다.

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```

<!-- This method will determine if the billable model has any payment method at all. To determine if a payment method of a specific type exists for the model, you may pass the `type` as an argument to the method: -->
이 메서드는 청구 가능한 모델에 결제 수단이 있는지 확인합니다. 모델에 대한 특정 유형의 결제 수단이 존재하는지 확인하려면 `type`를 메서드에 대한 인수로 전달할 수 있습니다.

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
<!-- ### Updating the Default Payment Method -->
### Updating the Default Payment Method

<!-- The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method: -->
`updateDefaultPaymentMethod` 메서드는 고객의 기본 결제 수단 정보를 업데이트하는 데 사용될 수 있습니다. 이 메서드는 Stripe 결제 수단 식별자를 허용하고 새 결제 수단을 기본 청구 결제 수단으로 할당합니다.

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

<!-- To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method: -->
기본 결제 수단 정보를 Stripe의 고객 기본 결제 수단 정보와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용할 수 있습니다.

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 고객의 기본 결제 수단은 송장 발행 및 새 구독 생성에만 사용할 수 있습니다. Stripe의 제한으로 인해 단일 충전에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
<!-- ### Adding Payment Methods -->
### Adding Payment Methods

<!-- To add a new payment method, you may call the `addPaymentMethod` method on the billable model, passing the payment method identifier: -->
새 결제 수단을 추가하려면 청구 가능한 모델에서 `addPaymentMethod` 메서드를 호출하여 결제 수단 식별자를 전달하면 됩니다.

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 식별자를 검색하는 방법을 알아보려면 [payment method storage documentation](#storing-payment-methods)를 검토하세요.

<a name="deleting-payment-methods"></a>
<!-- ### Deleting Payment Methods -->
### Deleting Payment Methods

<!-- To delete a payment method, you may call the `delete` method on the `Laravel\Cashier\PaymentMethod` instance you wish to delete: -->
결제 수단을 삭제하려면 삭제하려는 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```php
$paymentMethod->delete();
```

<!-- The `deletePaymentMethod` method will delete a specific payment method from the billable model: -->
`deletePaymentMethod` 메서드는 청구 가능한 모델에서 특정 결제 수단을 삭제합니다.

```php
$user->deletePaymentMethod('pm_visa');
```

<!-- The `deletePaymentMethods` method will delete all of the payment method information for the billable model: -->
`deletePaymentMethods` 메서드는 청구 가능한 모델에 대한 모든 결제 수단 정보를 삭제합니다.

```php
$user->deletePaymentMethods();
```

<!-- By default, this method will delete payment methods of every type. To delete payment methods of a specific type you can pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 모든 유형의 결제 수단을 삭제합니다. 특정 유형의 결제 수단을 삭제하려면 `type`를 메서드에 대한 인수로 전달할 수 있습니다.

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 사용자가 활성 구독을 갖고 있는 경우 애플리케이션은 사용자가 기본 결제 수단을 삭제하도록 허용해서는 안 됩니다.

<a name="subscriptions"></a>
<!-- ## Subscriptions -->
## Subscriptions

<!-- Subscriptions provide a way to set up recurring payments for your customers. Stripe subscriptions managed by Cashier provide support for multiple subscription prices, subscription quantities, trials, and more. -->
구독은 고객에 대한 반복 결제를 설정하는 방법을 제공합니다. Cashier에서 관리하는 Stripe 구독은 다양한 구독 가격, 구독 수량, 평가판 등에 대한 지원을 제공합니다.

<a name="creating-subscriptions"></a>
<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription: -->
구독을 생성하려면 먼저 청구 가능한 모델의 인스턴스를 검색하세요. 이는 일반적으로 `App\Models\User`의 인스턴스입니다. 모델 인스턴스를 검색한 후에는 `newSubscription` 메서드를 사용하여 모델 구독을 생성할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

<!-- The first argument passed to the `newSubscription` method should be the internal type of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription type is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument is the specific price the user is subscribing to. This value should correspond to the price's identifier in Stripe. -->
`newSubscription` 메서드에 전달된 첫 번째 인수는 구독의 내부 유형이어야 합니다. 애플리케이션이 단일 구독만 제공하는 경우 이를 `default` 또는 `primary`로 호출할 수 있습니다. 이 구독 유형은 내부 애플리케이션 용도로만 사용되며 사용자에게 표시되지 않습니다. 또한 공백이 없어야 하며 구독을 만든 후에는 변경하면 안 됩니다. 두 번째 인수는 사용자가 구독하는 특정 가격입니다. 이 값은 Stripe의 가격 식별자와 일치해야 합니다.

<!-- The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information. -->
[a Stripe payment method identifier](#storing-payment-methods) 또는 Stripe `PaymentMethod` 개체를 허용하는 `create` 메서드는 구독을 시작하고 청구 가능한 모델의 Stripe 고객 ID 및 기타 관련 청구 정보로 데이터베이스를 업데이트합니다.

> [!WARNING]
> 결제 수단 식별자를 `create` 구독 메서드에 직접 전달하면 사용자의 저장된 결제 수단에도 자동으로 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
<!-- #### Collecting Recurring Payments via Invoice Emails -->
#### Collecting Recurring Payments via Invoice Emails

<!-- Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices: -->
고객의 반복 결제를 자동으로 수집하는 대신, 반복 결제 기한이 다가올 때마다 고객에게 송장을 이메일로 보내도록 Stripe에 지시할 수 있습니다. 그런 다음 고객은 청구서를 받은 후 수동으로 지불할 수 있습니다. 고객은 송장을 통해 반복 결제를 받을 때 결제 수단을 미리 제공할 필요가 없습니다.

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

<!-- The amount of time a customer has to pay their invoice before their subscription is canceled is determined by the `days_until_due` option. By default, this is 30 days; however, you may provide a specific value for this option if you wish: -->
구독이 취소되기 전에 고객이 청구서를 지불해야 하는 기간은 `days_until_due` 옵션에 따라 결정됩니다. 기본적으로 이는 30일입니다. 그러나 원하는 경우 이 옵션에 특정 값을 제공할 수 있습니다.

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
<!-- #### Quantities -->
#### Quantities

<!-- If you would like to set a specific [quantity](https://stripe.com/docs/billing/subscriptions/quantities) for the price when creating the subscription, you should invoke the `quantity` method on the subscription builder before creating the subscription: -->
구독을 생성할 때 가격에 특정 [quantity](https://stripe.com/docs/billing/subscriptions/quantities)을 설정하려면 구독을 생성하기 전에 구독 빌더에서 `quantity` 메서드를 호출해야 합니다.

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional [customer](https://stripe.com/docs/api/customers/create) or [subscription](https://stripe.com/docs/api/subscriptions/create) options supported by Stripe, you may do so by passing them as the second and third arguments to the `create` method: -->
Stripe에서 지원하는 추가 [customer](https://stripe.com/docs/api/customers/create) 또는 [subscription](https://stripe.com/docs/api/subscriptions/create) 옵션을 지정하려면 해당 옵션을 `create` 메서드에 두 번째 및 세 번째 인수로 전달하면 됩니다.

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => 'Some extra information.'],
]);
```

<a name="coupons"></a>
<!-- #### Coupons -->
#### Coupons

<!-- If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method: -->
구독을 생성할 때 쿠폰을 적용하려면 `withCoupon` 메서드를 사용할 수 있습니다.

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

<!-- Or, if you would like to apply a [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes), you may use the `withPromotionCode` method: -->
또는 [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 적용하려면 `withPromotionCode` 메서드를 사용할 수 있습니다.

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

<!-- The given promotion code ID should be the Stripe API ID assigned to the promotion code and not the customer facing promotion code. If you need to find a promotion code ID based on a given customer facing promotion code, you may use the `findPromotionCode` method: -->
제공된 프로모션 코드 ID는 고객이 접하는 프로모션 코드가 아니라 프로모션 코드에 할당된 Stripe API ID여야 합니다. 특정 고객 대상 프로모션 코드를 기반으로 프로모션 코드 ID를 찾아야 하는 경우 `findPromotionCode` 메서드를 사용할 수 있습니다.

```php
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

<!-- In the example above, the returned `$promotionCode` object is an instance of `Laravel\Cashier\PromotionCode`. This class decorates an underlying `Stripe\PromotionCode` object. You can retrieve the coupon related to the promotion code by invoking the `coupon` method: -->
위의 예에서 반환된 `$promotionCode` 개체는 `Laravel\Cashier\PromotionCode`의 인스턴스입니다. 이 클래스는 기본 `Stripe\PromotionCode` 객체를 장식합니다. `coupon` 메서드를 호출하여 프로모션 코드와 관련된 쿠폰을 검색할 수 있습니다.

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

<!-- The coupon instance allows you to determine the discount amount and whether the coupon represents a fixed discount or percentage based discount: -->
쿠폰 인스턴스를 사용하면 할인 금액과 쿠폰이 고정 할인을 나타내는지 또는 백분율 기반 할인을 나타내는지 여부를 확인할 수 있습니다.

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

<!-- You can also retrieve the discounts that are currently applied to a customer or subscription: -->
현재 고객 또는 구독에 적용되는 할인을 검색할 수도 있습니다.

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

<!-- The returned `Laravel\Cashier\Discount` instances decorate an underlying `Stripe\Discount` object instance. You may retrieve the coupon related to this discount by invoking the `coupon` method: -->
반환된 `Laravel\Cashier\Discount` 인스턴스는 기본 `Stripe\Discount` 개체 인스턴스를 장식합니다. `coupon` 메서드를 호출하여 이 할인과 관련된 쿠폰을 검색할 수 있습니다.

```php
$coupon = $subscription->discount()->coupon();
```

<!-- If you would like to apply a new coupon or promotion code to a customer or subscription, you may do so via the `applyCoupon` or `applyPromotionCode` methods: -->
고객이나 구독에 새로운 쿠폰이나 프로모션 코드를 적용하려면 `applyCoupon` 또는 `applyPromotionCode` 메서드를 통해 적용할 수 있습니다.

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

<!-- Remember, you should use the Stripe API ID assigned to the promotion code and not the customer facing promotion code. Only one coupon or promotion code can be applied to a customer or subscription at a given time. -->
고객용 프로모션 코드가 아닌 프로모션 코드에 할당된 Stripe API ID를 사용해야 한다는 점을 기억하세요. 특정 시점에 하나의 쿠폰 또는 프로모션 코드만 고객 또는 구독에 적용될 수 있습니다.

<!-- For more info on this subject, please consult the Stripe documentation regarding [coupons](https://stripe.com/docs/billing/subscriptions/coupons) and [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes). -->
이 주제에 대한 자세한 내용은 [coupons](https://stripe.com/docs/billing/subscriptions/coupons) 및 [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes)에 관한 Stripe 문서를 참조하세요.

<a name="adding-subscriptions"></a>
<!-- #### Adding Subscriptions -->
#### Adding Subscriptions

<!-- If you would like to add a subscription to a customer who already has a default payment method you may invoke the `add` method on the subscription builder: -->
이미 기본 결제 수단을 갖고 있는 고객에게 구독을 추가하려면 구독 빌더에서 `add` 메서드를 호출하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
<!-- #### Creating Subscriptions From the Stripe Dashboard -->
#### Creating Subscriptions From the Stripe Dashboard

<!-- You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a type of `default`. To customize the subscription type that is assigned to dashboard created subscriptions, [define webhook event handlers](#defining-webhook-event-handlers). -->
Stripe 대시보드 자체에서 구독을 생성할 수도 있습니다. 이렇게 하면 Cashier는 새로 추가된 구독을 동기화하고 `default` 유형을 할당합니다. 대시보드 생성 구독에 할당된 구독 유형을 사용자 지정하려면 [define webhook event handlers](#defining-webhook-event-handlers)를 참조하세요.

<!-- In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different types, only one type of subscription may be added through the Stripe dashboard. -->
또한 Stripe 대시보드를 통해 한 가지 유형의 구독만 생성할 수 있습니다. 애플리케이션이 서로 다른 유형을 사용하는 여러 구독을 제공하는 경우 Stripe 대시보드를 통해 한 가지 유형의 구독만 추가할 수 있습니다.

<!-- Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If a customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database. -->
마지막으로, 항상 애플리케이션에서 제공하는 구독 유형당 하나의 활성 구독만 추가해야 합니다. 고객이 두 개의 `default` 구독을 가지고 있는 경우 두 구독 모두 애플리케이션의 데이터베이스와 동기화되더라도 가장 최근에 추가된 구독만 Cashier에서 사용됩니다.

<a name="checking-subscription-status"></a>
<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the type of the subscription as its first argument: -->
고객이 애플리케이션을 구독하면 다양하고 편리한 메서드를 사용하여 구독 상태를 쉽게 확인할 수 있습니다. 먼저, 구독이 현재 평가판 기간 내에 있더라도 고객에게 활성 구독이 있는 경우 `subscribed` 메서드는 `true`를 반환합니다. `subscribed` 메서드는 구독 유형을 첫 번째 인수로 승인합니다.

```php
if ($user->subscribed('default')) {
    // ...
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/12.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` 메서드는 또한 [route middleware](/docs/12.x/middleware)에 대한 훌륭한 후보가 되어 사용자의 구독 상태에 따라 라우트 및 컨트롤러에 대한 액세스를 필터링할 수 있습니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // This user is not a paying customer...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

<!-- If you would like to determine if a user is still within their trial period, you may use the `onTrial` method. This method can be useful for determining if you should display a warning to the user that they are still on their trial period: -->
사용자가 아직 평가판 기간 내에 있는지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이 메서드는 사용자에게 아직 평가판 기간에 있다는 경고를 표시해야 하는지 결정하는 데 유용할 수 있습니다.

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

<!-- The `subscribedToProduct` method may be used to determine if the user is subscribed to a given product based on a given Stripe product's identifier. In Stripe, products are collections of prices. In this example, we will determine if the user's `default` subscription is actively subscribed to the application's "premium" product. The given Stripe product identifier should correspond to one of your product's identifiers in the Stripe dashboard: -->
`subscribedToProduct` 메서드는 주어진 Stripe 제품의 식별자를 기반으로 사용자가 특정 제품에 가입했는지 여부를 결정하는 데 사용될 수 있습니다. Stripe에서 제품은 가격 모음입니다. 이 예에서는 사용자의 `default` 구독이 애플리케이션의 "프리미엄" 제품에 적극적으로 구독되어 있는지 확인합니다. 지정된 Stripe 제품 식별자는 Stripe 대시보드에 있는 제품 식별자 중 하나와 일치해야 합니다.

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

<!-- By passing an array to the `subscribedToProduct` method, you may determine if the user's `default` subscription is actively subscribed to the application's "basic" or "premium" product: -->
`subscribedToProduct` 메서드에 배열을 전달하면 사용자의 `default` 구독이 애플리케이션의 "기본" 또는 "프리미엄" 제품에 적극적으로 구독되어 있는지 확인할 수 있습니다.

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

<!-- The `subscribedToPrice` method may be used to determine if a customer's subscription corresponds to a given price ID: -->
`subscribedToPrice` 메서드는 고객의 구독이 주어진 가격 ID에 해당하는지 확인하는 데 사용될 수 있습니다.

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
`recurring` 메서드를 사용하여 사용자가 현재 구독 중이고 더 이상 평가판 기간 내에 있지 않은지 확인할 수 있습니다.

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> 사용자에게 동일한 유형의 구독이 두 개 있는 경우 가장 최근 구독이 항상 `subscription` 메서드에 의해 반환됩니다. 예를 들어, 사용자에게 `default` 유형의 구독 레코드가 두 개 있을 수 있습니다. 그러나 구독 중 하나는 오래되고 만료된 구독이고 다른 하나는 현재 활성 구독일 수 있습니다. 가장 최근 구독은 항상 반환되며 이전 구독은 기록 검토를 위해 데이터베이스에 보관됩니다.

<a name="cancelled-subscription-status"></a>
<!-- #### Canceled Subscription Status -->
#### Canceled Subscription Status

<!-- To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method: -->
사용자가 한때 활성 구독자였으나 구독을 취소했는지 확인하려면 `canceled` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

<!-- You may also determine if a user has canceled their subscription but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
사용자가 구독을 취소했지만 구독이 완전히 만료될 때까지 여전히 '유예 기간'에 있는지 확인할 수도 있습니다. 예를 들어 원래 3월 10일에 만료될 예정이었던 구독을 사용자가 3월 5일에 취소한 경우 사용자는 3월 10일까지 '유예 기간'을 유지하게 됩니다. 이 시간 동안 `subscribed` 메서드는 여전히 `true`를 반환합니다.

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

<!-- To determine if the user has canceled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
사용자가 구독을 취소했고 더 이상 "유예 기간"이 지나지 않았는지 확인하려면 `ended` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
<!-- #### Incomplete and Past Due Status -->
#### Incomplete and Past Due Status

<!-- If a subscription requires a secondary payment action after creation the subscription will be marked as `incomplete`. Subscription statuses are stored in the `stripe_status` column of Cashier's `subscriptions` database table. -->
구독 생성 후 보조 결제 작업이 필요한 경우 구독은 `incomplete`로 표시됩니다. 구독 상태는 Cashier의 `subscriptions` 데이터베이스 테이블의 `stripe_status` 열에 저장됩니다.

<!-- Similarly, if a secondary payment action is required when swapping prices the subscription will be marked as `past_due`. When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Determining if a subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
마찬가지로, 가격을 교환할 때 보조 결제 작업이 필요한 경우 구독은 `past_due`로 표시됩니다. 귀하의 구독이 이러한 상태 중 하나이면 고객이 결제를 확인할 때까지 활성화되지 않습니다. 구독에 불완전한 결제가 있는지 확인하려면 청구 가능한 모델 또는 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용하여 수행할 수 있습니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

<!-- When a subscription has an incomplete payment, you should direct the user to Cashier's payment confirmation page, passing the `latestPayment` identifier. You may use the `latestPayment` method available on subscription instance to retrieve this identifier: -->
구독에 결제가 완료되지 않은 경우 `latestPayment` 식별자를 전달하여 사용자를 Cashier의 결제 확인 페이지로 안내해야 합니다. 구독 인스턴스에서 사용할 수 있는 `latestPayment` 메서드를 사용하여 이 식별자를 검색할 수 있습니다.

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

<!-- If you would like the subscription to still be considered active when it's in a `past_due` or `incomplete` state, you may use the `keepPastDueSubscriptionsActive` and `keepIncompleteSubscriptionsActive` methods provided by Cashier. Typically, these methods should be called in the `register` method of your `App\Providers\AppServiceProvider`: -->
`past_due` 또는 `incomplete` 상태에 있을 때 구독이 계속 활성 상태로 간주되도록 하려면 Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 및 `keepIncompleteSubscriptionsActive` 메서드를 사용할 수 있습니다. 일반적으로 이러한 메서드는 `App\Providers\AppServiceProvider`의 `register` 메서드에서 호출되어야 합니다.

```php
use Laravel\Cashier\Cashier;

/**
 * Register any application services.
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
    Cashier::keepIncompleteSubscriptionsActive();
}
```

> [!WARNING]
> 구독이 `incomplete` 상태인 경우 결제가 확인될 때까지 변경할 수 없습니다. 따라서 구독이 `incomplete` 상태에 있을 때 `swap` 및 `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
대부분의 구독 상태는 쿼리 범위로도 사용할 수 있으므로 특정 상태에 있는 구독에 대해 데이터베이스를 쉽게 쿼리할 수 있습니다.

```php
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

<!-- A complete list of available scopes is available below: -->
사용 가능한 범위의 전체 목록은 아래에서 확인할 수 있습니다.

```php
Subscription::query()->active();
Subscription::query()->canceled();
Subscription::query()->ended();
Subscription::query()->incomplete();
Subscription::query()->notCanceled();
Subscription::query()->notOnGracePeriod();
Subscription::query()->notOnTrial();
Subscription::query()->onGracePeriod();
Subscription::query()->onTrial();
Subscription::query()->pastDue();
Subscription::query()->recurring();
```

<a name="changing-prices"></a>
<!-- ### Changing Prices -->
### Changing Prices

<!-- After a customer is subscribed to your application, they may occasionally want to change to a new subscription price. To swap a customer to a new price, pass the Stripe price's identifier to the `swap` method. When swapping prices, it is assumed that the user would like to re-activate their subscription if it was previously canceled. The given price identifier should correspond to a Stripe price identifier available in the Stripe dashboard: -->
고객이 애플리케이션을 구독한 후 가끔 새 구독 가격으로 변경하고 싶을 수도 있습니다. 고객을 새 가격으로 교환하려면 Stripe 가격 식별자를 `swap` 메서드에 전달하세요. 가격을 교환할 때 사용자는 이전에 구독을 취소한 경우 구독을 다시 활성화하기를 원한다고 가정합니다. 지정된 가격 식별자는 Stripe 대시보드에서 사용할 수 있는 Stripe 가격 식별자와 일치해야 합니다.

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

<!-- If the customer is on trial, the trial period will be maintained. Additionally, if a "quantity" exists for the subscription, that quantity will also be maintained. -->
고객이 평가판을 사용 중인 경우 평가판 기간이 유지됩니다. 또한 구독에 대한 "수량"이 존재하는 경우 해당 수량도 유지됩니다.

<!-- If you would like to swap prices and cancel any trial period the customer is currently on, you may invoke the `skipTrial` method: -->
가격을 교환하고 고객이 현재 진행 중인 평가판 기간을 취소하려면 `skipTrial` 메서드를 호출하면 됩니다.

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

<!-- If you would like to swap prices and immediately invoice the customer instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
가격을 교환하고 다음 청구 주기를 기다리지 않고 즉시 고객에게 청구하려면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
<!-- #### Prorations -->
#### Prorations

<!-- By default, Stripe prorates charges when swapping between prices. The `noProrate` method may be used to update the subscription's price without prorating the charges: -->
기본적으로 Stripe는 가격을 교환할 때 요금을 비례 배분합니다. `noProrate` 메서드를 사용하면 요금을 비례배분하지 않고 구독 가격을 업데이트할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

<!-- For more information on subscription proration, consult the [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations). -->
구독 비례배분에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations)를 참조하세요.

> [!WARNING]
> `swapAndInvoice` 메서드 이전에 `noProrate` 메서드를 실행하면 비례 배분에 영향을 주지 않습니다. 청구서는 항상 발행됩니다.

<a name="subscription-quantity"></a>
<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. You may use the `incrementQuantity` and `decrementQuantity` methods to easily increment or decrement your subscription quantity: -->
때때로 구독은 "수량"의 ​​영향을 받습니다. 예를 들어 프로젝트 관리 애플리케이션은 프로젝트당 월 10달러를 청구할 수 있습니다. `incrementQuantity` 및 `decrementQuantity` 메서드를 사용하여 구독 수량을 쉽게 늘리거나 줄일 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription('default')->decrementQuantity(5);
```

<!-- Alternatively, you may set a specific quantity using the `updateQuantity` method: -->
또는 `updateQuantity` 메서드를 사용하여 특정 수량을 설정할 수도 있습니다.

```php
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
`noProrate` 메서드를 사용하면 요금을 비례배분하지 않고 구독 수량을 업데이트할 수 있습니다.

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<!-- For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities). -->
구독 수량에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/subscriptions/quantities)를 참조하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
<!-- #### Quantities for Subscriptions With Multiple Products -->
#### Quantities for Subscriptions With Multiple Products

<!-- If your subscription is a [subscription with multiple products](#subscriptions-with-multiple-products), you should pass the ID of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods: -->
구독이 [subscription with multiple products](#subscriptions-with-multiple-products)인 경우 수량을 늘리거나 줄이려는 가격의 ID를 증가/감소 메서드의 두 번째 인수로 전달해야 합니다.

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
<!-- ### Subscriptions With Multiple Products -->
### Subscriptions With Multiple Products

<!-- [Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products) allow you to assign multiple billing products to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on product for an additional $15 per month. Information for subscriptions with multiple products is stored in Cashier's `subscription_items` database table. -->
[Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products)을 사용하면 단일 구독에 여러 결제 제품을 할당할 수 있습니다. 예를 들어, 기본 구독 가격이 월 10달러이지만 추가 월 15달러에 실시간 채팅 추가 기능 제품을 제공하는 고객 서비스 "헬프데스크" 애플리케이션을 구축한다고 가정해 보겠습니다. 여러 제품이 포함된 구독에 대한 정보는 Cashier의 `subscription_items` 데이터베이스 테이블에 저장됩니다.

<!-- You may specify multiple products for a given subscription by passing an array of prices as the second argument to the `newSubscription` method: -->
가격 배열을 `newSubscription` 메서드의 두 번째 인수로 전달하여 특정 구독에 대해 여러 제품을 지정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', [
        'price_monthly',
        'price_chat',
    ])->create($request->paymentMethodId);

    // ...
});
```

<!-- In the example above, the customer will have two prices attached to their `default` subscription. Both prices will be charged on their respective billing intervals. If necessary, you may use the `quantity` method to indicate a specific quantity for each price: -->
위의 예에서 고객은 `default` 구독에 두 가지 가격을 첨부하게 됩니다. 두 가격 모두 해당 청구 간격에 따라 청구됩니다. 필요한 경우 `quantity` 메서드를 사용하여 각 가격에 대한 특정 수량을 표시할 수 있습니다.

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

<!-- If you would like to add another price to an existing subscription, you may invoke the subscription's `addPrice` method: -->
기존 구독에 다른 가격을 추가하려면 구독의 `addPrice` 메서드를 호출하면 됩니다.

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

<!-- The example above will add the new price and the customer will be billed for it on their next billing cycle. If you would like to bill the customer immediately you may use the `addPriceAndInvoice` method: -->
위의 예에서는 새 가격을 추가하고 고객에게 다음 청구 주기에 해당 가격이 청구됩니다. 고객에게 즉시 비용을 청구하려면 `addPriceAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

<!-- If you would like to add a price with a specific quantity, you can pass the quantity as the second argument of the `addPrice` or `addPriceAndInvoice` methods: -->
특정 수량의 가격을 추가하려면 해당 수량을 `addPrice` 또는 `addPriceAndInvoice` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

<!-- You may remove prices from subscriptions using the `removePrice` method: -->
`removePrice` 메서드를 사용하여 구독에서 가격을 제거할 수 있습니다.

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> 구독의 마지막 가격은 제거할 수 없습니다. 대신 구독을 취소하면 됩니다.

<a name="swapping-prices"></a>
<!-- #### Swapping Prices -->
#### Swapping Prices

<!-- You may also change the prices attached to a subscription with multiple products. For example, imagine a customer has a `price_basic` subscription with a `price_chat` add-on product and you want to upgrade the customer from the `price_basic` to the `price_pro` price: -->
여러 제품이 포함된 구독에 첨부된 가격을 변경할 수도 있습니다. 예를 들어, 고객이 `price_chat` 추가 제품이 포함된 `price_basic` 구독을 가지고 있고 고객을 `price_basic`에서 `price_pro` 가격으로 업그레이드하려고 한다고 가정해 보겠습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

<!-- When executing the example above, the underlying subscription item with the `price_basic` is deleted and the one with the `price_chat` is preserved. Additionally, a new subscription item for the `price_pro` is created. -->
위의 예를 실행하면 `price_basic`가 있는 기본 구독 항목이 삭제되고 `price_chat`가 있는 구독 항목이 유지됩니다. 또한 `price_pro`에 대한 새 구독 항목이 생성됩니다.

<!-- You can also specify subscription item options by passing an array of key / value pairs to the `swap` method. For example, you may need to specify the subscription price quantities: -->
키/값 쌍 배열을 `swap` 메서드에 전달하여 구독 항목 옵션을 지정할 수도 있습니다. 예를 들어 구독 가격 수량을 지정해야 할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

<!-- If you want to swap a single price on a subscription, you may do so using the `swap` method on the subscription item itself. This approach is particularly useful if you would like to preserve all of the existing metadata on the subscription's other prices: -->
구독의 단일 가격을 교환하려면 구독 항목 자체에 `swap` 메서드를 사용하면 됩니다. 이 접근 방식은 구독의 다른 가격에 대한 기존 메타데이터를 모두 보존하려는 경우 특히 유용합니다.

```php
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>
<!-- #### Proration -->
#### Proration

<!-- By default, Stripe will prorate charges when adding or removing prices from a subscription with multiple products. If you would like to make a price adjustment without proration, you should chain the `noProrate` method onto your price operation: -->
기본적으로 Stripe는 여러 제품이 포함된 구독에서 가격을 추가하거나 제거할 때 요금을 비례 배분합니다. 비례배분 없이 가격을 조정하려면 `noProrate` 메서드를 가격 작업에 연결해야 합니다.

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
<!-- #### Quantities -->
#### Quantities

<!-- If you would like to update quantities on individual subscription prices, you may do so using the [existing quantity methods](#subscription-quantity) by passing the ID of the price as an additional argument to the method: -->
개별 구독 가격의 수량을 업데이트하려면 가격 ID를 메서드에 추가 인수로 전달하여 [existing quantity methods](#subscription-quantity)를 사용하여 업데이트할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 구독에 여러 가격이 있는 경우 `Subscription` 모델의 `stripe_price` 및 `quantity` 속성은 `null`가 됩니다. 개별 가격 속성에 액세스하려면 `Subscription` 모델에서 사용 가능한 `items` 관계를 사용해야 합니다.

<a name="subscription-items"></a>
<!-- #### Subscription Items -->
#### Subscription Items

<!-- When a subscription has multiple prices, it will have multiple subscription "items" stored in your database's `subscription_items` table. You may access these via the `items` relationship on the subscription: -->
구독 가격이 여러 개인 경우 데이터베이스의 `subscription_items` 테이블에 여러 구독 "항목"이 저장됩니다. 구독의 `items` 관계를 통해 이러한 항목에 액세스할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

<!-- You can also retrieve a specific price using the `findItemOrFail` method: -->
`findItemOrFail` 메서드를 사용하여 특정 가격을 검색할 수도 있습니다.

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
<!-- ### Multiple Subscriptions -->
### Multiple Subscriptions

<!-- Stripe allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans. -->
Stripe를 사용하면 고객이 동시에 여러 구독을 가질 수 있습니다. 예를 들어 수영 구독과 역도 구독을 제공하는 체육관을 운영할 수 있으며 각 구독마다 가격이 다를 수 있습니다. 물론 고객은 둘 중 하나 또는 두 가지 요금제 모두에 가입할 수 있어야 합니다.

<!-- When your application creates subscriptions, you may provide the type of the subscription to the `newSubscription` method. The type may be any string that represents the type of subscription the user is initiating: -->
애플리케이션이 구독을 생성할 때 `newSubscription` 메서드에 구독 유형을 제공할 수 있습니다. 유형은 사용자가 시작하는 구독 유형을 나타내는 문자열일 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- In this example, we initiated a monthly swimming subscription for the customer. However, they may want to swap to a yearly subscription at a later time. When adjusting the customer's subscription, we can simply swap the price on the `swimming` subscription: -->
이 예에서는 고객을 위해 월간 수영 구독을 시작했습니다. 그러나 나중에 연간 구독으로 전환할 수도 있습니다. 고객의 구독을 조정할 때 `swimming` 구독의 가격을 간단히 교환할 수 있습니다.

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

<!-- Of course, you may also cancel the subscription entirely: -->
물론 구독을 완전히 취소할 수도 있습니다.

```php
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
<!-- ### Usage Based Billing -->
### Usage Based Billing

<!-- [Usage based billing](https://stripe.com/docs/billing/subscriptions/metered-billing) allows you to charge customers based on their product usage during a billing cycle. For example, you may charge customers based on the number of text messages or emails they send per month. -->
[Usage based billing](https://stripe.com/docs/billing/subscriptions/metered-billing)를 사용하면 청구 주기 동안 제품 사용량을 기준으로 고객에게 요금을 청구할 수 있습니다. 예를 들어, 매월 보내는 문자 메시지나 이메일 수를 기준으로 고객에게 요금을 청구할 수 있습니다.

<!-- To start using usage billing, you will first need to create a new product in your Stripe dashboard with a [usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) and a [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter). After creating the meter, store the associated event name and meter ID, which you will need to report and retrieve usage. Then, use the `meteredPrice` method to add the metered price ID to a customer subscription: -->
사용량 청구 사용을 시작하려면 먼저 Stripe 대시보드에서 [usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) 및 [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter)를 사용하여 새 제품을 생성해야 합니다. 측정기를 생성한 후 사용량을 보고하고 검색하는 데 필요한 연결된 이벤트 이름과 측정기 ID를 저장합니다. 그런 다음 `meteredPrice` 메서드를 사용하여 측정 가격 ID를 고객 구독에 추가합니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- You may also start a metered subscription via [Stripe Checkout](#checkout): -->
[Stripe Checkout](#checkout)을 통해 종량제 구독을 시작할 수도 있습니다.

```php
$checkout = Auth::user()
    ->newSubscription('default', [])
    ->meteredPrice('price_metered')
    ->checkout();

return view('your-checkout-view', [
    'checkout' => $checkout,
]);
```

<a name="reporting-usage"></a>
<!-- #### Reporting Usage -->
#### Reporting Usage

<!-- As your customer uses your application, you will report their usage to Stripe so that they can be billed accurately. To report the usage of a metered event, you may use the `reportMeterEvent` method on your `Billable` model: -->
고객이 애플리케이션을 사용할 때 정확한 요금이 청구될 수 있도록 사용량을 Stripe에 보고하게 됩니다. 측정된 이벤트의 사용량을 보고하려면 `Billable` 모델에서 `reportMeterEvent` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

<!-- By default, a "usage quantity" of 1 is added to the billing period. Alternatively, you may pass a specific amount of "usage" to add to the customer's usage for the billing period: -->
기본적으로 "사용 수량" 1이 청구 기간에 추가됩니다. 또는 특정 양의 "사용량"을 전달하여 청구 기간 동안 고객의 사용량에 추가할 수 있습니다.

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

<!-- To retrieve a customer's event summary for a meter, you may use a `Billable` instance's `meterEventSummaries` method: -->
미터에 대한 고객의 이벤트 요약을 검색하려면 `Billable` 인스턴스의 `meterEventSummaries` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

<!-- Please refer to Stripe's [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object) for more information on meter event summaries. -->
미터 이벤트 요약에 대한 자세한 내용은 Stripe의 [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object)를 참조하세요.

<!-- To [list all meters](https://docs.stripe.com/api/billing/meter/list), you may use a `Billable` instance's `meters` method: -->
[list all meters](https://docs.stripe.com/api/billing/meter/list)하려면 `Billable` 인스턴스의 `meters` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>
<!-- ### Subscription Taxes -->
### Subscription Taxes

> [!WARNING]
> 세율을 수동으로 계산하는 대신 [automatically calculate taxes using Stripe Tax](#tax-configuration)할 수 있습니다.

<!-- To specify the tax rates a user pays on a subscription, you should implement the `taxRates` method on your billable model and return an array containing the Stripe tax rate IDs. You can define these tax rates in [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates): -->
사용자가 구독에 대해 지불하는 세율을 지정하려면 청구 가능한 모델에 `taxRates` 메서드를 구현하고 Stripe 세율 ID가 포함된 배열을 반환해야 합니다. [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates)에서 다음 세율을 정의할 수 있습니다.

```php
/**
 * The tax rates that should apply to the customer's subscriptions.
 *
 * @return array<int, string>
 */
public function taxRates(): array
{
    return ['txr_id'];
}
```

<!-- The `taxRates` method enables you to apply a tax rate on a customer-by-customer basis, which may be helpful for a user base that spans multiple countries and tax rates. -->
`taxRates` 메서드를 사용하면 고객별로 세율을 적용할 수 있으며, 이는 여러 국가 및 세율에 걸쳐 있는 사용자 기반에 도움이 될 수 있습니다.

<!-- If you're offering subscriptions with multiple products, you may define different tax rates for each price by implementing a `priceTaxRates` method on your billable model: -->
여러 제품이 포함된 구독을 제공하는 경우 청구 가능한 모델에 `priceTaxRates` 메서드를 구현하여 각 가격에 대해 서로 다른 세율을 정의할 수 있습니다.

```php
/**
 * The tax rates that should apply to the customer's subscriptions.
 *
 * @return array<string, array<int, string>>
 */
public function priceTaxRates(): array
{
    return [
        'price_monthly' => ['txr_id'],
    ];
}
```

> [!WARNING]
> `taxRates` 메서드는 구독 요금에만 적용됩니다. Cashier를 사용하여 "일회성" 요금을 부과하는 경우 해당 시점에 세율을 수동으로 지정해야 합니다.

<a name="syncing-tax-rates"></a>
<!-- #### Syncing Tax Rates -->
#### Syncing Tax Rates

<!-- When changing the hard-coded tax rate IDs returned by the `taxRates` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the new `taxRates` values, you should call the `syncTaxRates` method on the user's subscription instance: -->
`taxRates` 메서드에서 반환된 하드 코딩된 세율 ID를 변경하는 경우 사용자의 기존 구독에 대한 세금 설정은 동일하게 유지됩니다. 새로운 `taxRates` 값으로 기존 구독의 세금 값을 업데이트하려면 사용자의 구독 인스턴스에서 `syncTaxRates` 메서드를 호출해야 합니다.

```php
$user->subscription('default')->syncTaxRates();
```

<!-- This will also sync any item tax rates for a subscription with multiple products. If your application is offering subscriptions with multiple products, you should ensure that your billable model implements the `priceTaxRates` method [discussed above](#subscription-taxes). -->
또한 여러 제품의 구독에 대한 항목 세율도 동기화됩니다. 애플리케이션이 여러 제품에 대한 구독을 제공하는 경우 청구 가능한 모델이 [discussed above](#subscription-taxes) `priceTaxRates` 메서드를 구현하는지 확인해야 합니다.

<a name="tax-exemption"></a>
<!-- #### Tax Exemption -->
#### Tax Exemption

<!-- Cashier also offers the `isNotTaxExempt`, `isTaxExempt`, and `reverseChargeApplies` methods to determine if the customer is tax exempt. These methods will call the Stripe API to determine a customer's tax exemption status: -->
Cashier는 또한 고객이 면세 대상인지 확인하기 위해 `isNotTaxExempt`, `isTaxExempt` 및 `reverseChargeApplies` 메서드를 제공합니다. 이러한 메서드는 Stripe API를 호출하여 고객의 면세 상태를 확인합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]
> 이러한 메서드는 모든 `Laravel\Cashier\Invoice` 개체에서도 사용할 수 있습니다. 그러나 `Invoice` 객체에서 호출되면 메서드는 송장이 생성될 당시의 면제 상태를 결정합니다.

<a name="subscription-anchor-date"></a>
<!-- ### Subscription Anchor Date -->
### Subscription Anchor Date

<!-- By default, the billing cycle anchor is the date the subscription was created or, if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method: -->
기본적으로 청구 주기 기준은 구독이 생성된 날짜이거나 평가판 기간이 사용된 경우 평가판이 종료되는 날짜입니다. 청구 기준일을 수정하려면 `anchorBillingCycleOn` 메서드를 사용하세요.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $anchor = Carbon::parse('first day of next month');

    $request->user()->newSubscription('default', 'price_monthly')
        ->anchorBillingCycleOn($anchor->startOfDay())
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- For more information on managing subscription billing cycles, consult the [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle) -->
구독 청구 주기 관리에 대한 자세한 내용은 [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참조하세요.

<a name="cancelling-subscriptions"></a>
<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
구독을 취소하려면 사용자 구독에서 `cancel` 메서드를 호출하세요.

```php
$user->subscription('default')->cancel();
```

<!-- When a subscription is canceled, Cashier will automatically set the `ends_at` column in your `subscriptions` database table. This column is used to know when the `subscribed` method should begin returning `false`. -->
구독이 취소되면 Cashier는 `subscriptions` 데이터베이스 테이블에 `ends_at` 열을 자동으로 설정합니다. 이 열은 `subscribed` 메서드가 `false` 반환을 시작해야 하는 시기를 아는 데 사용됩니다.

<!-- For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
예를 들어, 고객이 3월 1일에 구독을 취소했지만 구독이 3월 5일까지 종료될 예정이 아닌 경우 `subscribed` 메서드는 3월 5일까지 `true`를 계속 반환합니다. 이는 일반적으로 사용자가 청구 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있도록 허용되기 때문에 수행됩니다.

<!-- You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
`onGracePeriod` 메서드를 사용하여 사용자가 구독을 취소했지만 여전히 "유예 기간"에 있는지 확인할 수 있습니다.

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

<!-- If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription: -->
구독을 즉시 취소하려면 사용자 구독에서 `cancelNow` 메서드를 호출하세요.

```php
$user->subscription('default')->cancelNow();
```

<!-- If you wish to cancel a subscription immediately and invoice any remaining un-invoiced metered usage or new / pending proration invoice items, call the `cancelNowAndInvoice` method on the user's subscription: -->
구독을 즉시 취소하고 청구되지 않은 남은 측정 사용량 또는 새/보류 중인 비례 할당 청구 항목에 대해 청구하려면 사용자의 구독에서 `cancelNowAndInvoice` 메서드를 호출하세요.

```php
$user->subscription('default')->cancelNowAndInvoice();
```

<!-- You may also choose to cancel the subscription at a specific moment in time: -->
특정 시점에 구독을 취소하도록 선택할 수도 있습니다.

```php
$user->subscription('default')->cancelAt(
    now()->plus(days: 10)
);
```

<!-- Finally, you should always cancel user subscriptions before deleting the associated user model: -->
마지막으로, 연결된 사용자 모델을 삭제하기 전에 항상 사용자 구독을 취소해야 합니다.

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
<!-- ### Resuming Subscriptions -->
### Resuming Subscriptions

<!-- If a customer has canceled their subscription and you wish to resume it, you may invoke the `resume` method on the subscription. The customer must still be within their "grace period" in order to resume a subscription: -->
고객이 구독을 취소했고 이를 재개하려는 경우 구독에서 `resume` 메서드를 호출할 수 있습니다. 구독을 재개하려면 고객이 '유예 기간' 내에 있어야 합니다.

```php
$user->subscription('default')->resume();
```

<!-- If the customer cancels a subscription and then resumes that subscription before the subscription has fully expired the customer will not be billed immediately. Instead, their subscription will be re-activated and they will be billed on the original billing cycle. -->
고객이 구독을 취소한 다음 구독이 완전히 만료되기 전에 해당 구독을 재개하는 경우 고객에게 즉시 요금이 청구되지 않습니다. 대신 구독이 다시 활성화되고 원래 청구 주기에 따라 비용이 청구됩니다.

<a name="subscription-trials"></a>
<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>
<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions: -->
결제 수단 정보를 미리 수집하면서 고객에게 평가판 기간을 제공하려면 구독을 생성할 때 `trialDays` 메서드를 사용해야 합니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- This method will set the trial period ending date on the subscription record within the database and instruct Stripe to not begin billing the customer until after this date. When using the `trialDays` method, Cashier will overwrite any default trial period configured for the price in Stripe. -->
이 메서드는 데이터베이스 내의 구독 기록에 평가 기간 종료 날짜를 설정하고 이 날짜 이후까지 고객에게 청구를 시작하지 않도록 Stripe에 지시합니다. `trialDays` 메서드를 사용하는 경우 Cashier는 Stripe의 가격에 대해 구성된 기본 평가판 기간을 덮어씁니다.

> [!WARNING]
> 평가판 종료 날짜 이전에 고객의 구독을 취소하지 않으면 평가판이 만료되는 즉시 요금이 청구되므로 사용자에게 평가판 종료 날짜를 알려야 합니다.

<!-- The `trialUntil` method allows you to provide a `DateTime` instance that specifies when the trial period should end: -->
`trialUntil` 메서드를 사용하면 평가판 기간 종료 시기를 지정하는 `DateTime` 인스턴스를 제공할 수 있습니다.

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->plus(days: 10))
    ->create($paymentMethod);
```

<!-- You may determine if a user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
사용자 인스턴스의 `onTrial` 메서드 또는 구독 인스턴스의 `onTrial` 메서드를 사용하여 사용자가 평가판 기간 내에 있는지 확인할 수 있습니다. 아래 두 예는 동일합니다.

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

<!-- You may use the `endTrial` method to immediately end a subscription trial: -->
`endTrial` 메서드를 사용하여 구독 평가판을 즉시 종료할 수 있습니다.

```php
$user->subscription('default')->endTrial();
```

<!-- To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods: -->
기존 평가판이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
<!-- #### Defining Trial Days in Stripe / Cashier -->
#### Defining Trial Days in Stripe / Cashier

<!-- You may choose to define how many trial days your price's receive in the Stripe dashboard or always pass them explicitly using Cashier. If you choose to define your price's trial days in Stripe you should be aware that new subscriptions, including new subscriptions for a customer that had a subscription in the past, will always receive a trial period unless you explicitly call the `skipTrial()` method. -->
Stripe 대시보드에서 가격이 수신되는 평가판 일수를 정의하거나 항상 Cashier를 사용하여 명시적으로 통과하도록 선택할 수 있습니다. Stripe에서 가격의 평가판 날짜를 정의하기로 선택한 경우 과거에 구독이 있었던 고객의 새 구독을 포함하여 새 구독은 `skipTrial()` 메서드를 명시적으로 호출하지 않는 한 항상 평가판 기간을 받게 된다는 점을 알아야 합니다.

<a name="without-payment-method-up-front"></a>
<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration: -->
사용자의 결제 수단 정보를 미리 수집하지 않고 평가판 기간을 제공하려는 경우 사용자 기록의 `trial_ends_at` 열을 원하는 평가판 종료 날짜로 설정하면 됩니다. 이는 일반적으로 사용자 등록 시 수행됩니다:

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->plus(days: 10),
]);
```

> [!WARNING]
> 청구 가능한 모델 클래스 정의 내에서 `trial_ends_at` 속성에 대해 [date cast](/docs/12.x/eloquent-mutators#date-casting)를 추가해야 합니다.

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the billable model instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
Cashier는 이러한 유형의 평가판을 "일반 평가판"이라고 부릅니다. 기존 구독에 연결되어 있지 않기 때문입니다. 청구 가능한 모델 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 값을 지나지 않은 경우 `true`를 반환합니다.

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
사용자를 위한 실제 구독을 생성할 준비가 되면 평소처럼 `newSubscription` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription type parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
사용자의 평가판 종료 날짜를 검색하려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 평가판을 사용 중인 경우 Carbon 날짜 인스턴스를 반환하고 그렇지 않은 경우 `null`를 반환합니다. 기본 구독이 아닌 특정 구독에 대한 평가판 종료 날짜를 확인하려는 경우 선택적 구독 유형 매개변수를 전달할 수도 있습니다.

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not yet created an actual subscription: -->
사용자가 "일반" 평가판 기간 내에 있고 아직 실제 구독을 생성하지 않았는지 구체적으로 알고 싶은 경우 `onGenericTrial` 메서드를 사용할 수도 있습니다.

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>
<!-- ### Extending Trials -->
### Extending Trials

<!-- The `extendTrial` method allows you to extend the trial period of a subscription after the subscription has been created. If the trial has already expired and the customer is already being billed for the subscription, you can still offer them an extended trial. The time spent within the trial period will be deducted from the customer's next invoice: -->
`extendTrial` 메서드를 사용하면 구독이 생성된 후 구독의 평가판 기간을 연장할 수 있습니다. 평가판이 이미 만료되었고 고객에게 이미 구독 요금이 청구된 경우에도 연장된 평가판을 제공할 수 있습니다. 평가판 기간 내에 소요된 시간은 고객의 다음 청구서에서 공제됩니다.

```php
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// End the trial 7 days from now...
$subscription->extendTrial(
    now()->plus(days: 7)
);

// Add an additional 5 days to the trial...
$subscription->extendTrial(
    $subscription->trial_ends_at->plus(days: 5)
);
```

<a name="handling-stripe-webhooks"></a>
<!-- ## Handling Stripe Webhooks -->
## Handling Stripe Webhooks

> [!NOTE]
> [the Stripe CLI](https://stripe.com/docs/stripe-cli)를 사용하여 로컬 개발 중에 웹훅을 테스트할 수 있습니다.

<!-- Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Stripe는 웹후크를 통해 다양한 이벤트를 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier의 웹훅 ​​컨트롤러를 가리키는 라우트는 Cashier 서비스 프로바이더에 의해 자동으로 등록됩니다. 이 컨트롤러는 들어오는 모든 웹훅 요청을 처리합니다.

<!-- By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like. -->
기본적으로 Cashier 웹후크 컨트롤러는 요금 실패(Stripe 설정에 정의됨)가 너무 많은 구독 취소, 고객 업데이트, 고객 삭제, 구독 업데이트 및 결제 수단 변경을 자동으로 처리합니다. 그러나 곧 알게 되겠지만 이 컨트롤러를 확장하여 원하는 Stripe 웹훅 이벤트를 처리할 수 있습니다.

<!-- To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are: -->
애플리케이션이 Stripe 웹훅을 처리할 수 있도록 하려면 Stripe 제어판에서 웹훅 URL를 구성해야 합니다. 기본적으로 Cashier의 웹훅 ​​컨트롤러는 `/stripe/webhook` URL 경로에 응답합니다. Stripe 제어판에서 활성화해야 하는 모든 웹후크의 전체 목록은 다음과 같습니다.

<!--
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`
-->
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

<!-- For convenience, Cashier includes a `cashier:webhook` Artisan command. This command will create a webhook in Stripe that listens to all of the events required by Cashier: -->
편의를 위해 Cashier에는 `cashier:webhook` Artisan 명령이 포함되어 있습니다. 이 명령은 Cashier에 필요한 모든 이벤트를 수신하는 Stripe에 웹후크를 생성합니다.

```shell
php artisan cashier:webhook
```

<!-- By default, the created webhook will point to the URL defined by the `APP_URL` environment variable and the `cashier.webhook` route that is included with Cashier. You may provide the `--url` option when invoking the command if you would like to use a different URL: -->
기본적으로 생성된 웹훅은 `APP_URL` 환경 변수로 정의된 URL와 Cashier에 포함된 `cashier.webhook` 라우트를 가리킵니다. 다른 URL를 사용하려는 경우 명령을 호출할 때 `--url` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

<!-- The webhook that is created will use the Stripe API version that your version of Cashier is compatible with. If you would like to use a different Stripe version, you may provide the `--api-version` option: -->
생성된 웹훅은 귀하의 Cashier 버전과 호환되는 Stripe API 버전을 사용합니다. 다른 Stripe 버전을 사용하려면 `--api-version` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

<!-- After creation, the webhook will be immediately active. If you wish to create the webhook but have it disabled until you're ready, you may provide the `--disabled` option when invoking the command: -->
웹훅이 생성되면 즉시 활성화됩니다. 웹훅을 생성하고 싶지만 준비가 될 때까지 비활성화한 경우 명령을 호출할 때 `--disabled` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Cashier에 포함된 [webhook signature verification](#verifying-webhook-signatures) 미들웨어를 사용하여 들어오는 Stripe 웹훅 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
<!-- #### Webhooks and CSRF Protection -->
#### Webhooks and CSRF Protection

<!-- Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/12.x/csrf), you should ensure that Laravel does not attempt to validate the CSRF token for incoming Stripe webhooks. To accomplish this, you should exclude `stripe/*` from CSRF protection in your application's `bootstrap/app.php` file: -->
Stripe 웹훅은 Laravel의 [CSRF protection](/docs/12.x/csrf)를 우회해야 하므로 Laravel가 수신 Stripe 웹훅에 대한 CSRF 토큰의 유효성을 검사하려고 시도하지 않도록 해야 합니다. 이를 달성하려면 애플리케이션의 `bootstrap/app.php` 파일의 CSRF 보호에서 `stripe/*`를 제외해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancellations for failed charges and other common Stripe webhook events. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier는 청구 실패 및 기타 일반적인 Stripe 웹훅 이벤트에 대한 구독 취소를 자동으로 처리합니다. 그러나 처리하고 싶은 추가 웹훅 이벤트가 있는 경우 Cashier의 디스패치인 다음 이벤트를 청취하여 처리할 수 있습니다.

<!--
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`
-->
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

<!-- Both events contain the full payload of the Stripe webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/12.x/events#defining-listeners) that will handle the event: -->
두 이벤트 모두 Stripe 웹훅의 전체 페이로드를 포함합니다. 예를 들어, `invoice.payment_succeeded` 웹훅을 처리하려는 경우 이벤트를 처리할 [listener](/docs/12.x/events#defining-listeners)를 등록할 수 있습니다.

```php
<?php

namespace App\Listeners;

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    /**
     * Handle received Stripe webhooks.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['type'] === 'invoice.payment_succeeded') {
            // Handle the incoming event...
        }
    }
}
```

<a name="verifying-webhook-signatures"></a>
<!-- ### Verifying Webhook Signatures -->
### Verifying Webhook Signatures

<!-- To secure your webhooks, you may use [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures). For convenience, Cashier automatically includes a middleware which validates that the incoming Stripe webhook request is valid. -->
웹훅을 보호하려면 [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures)을 사용할 수 있습니다. 편의를 위해 Cashier에는 들어오는 Stripe 웹훅 요청이 유효한지 확인하는 미들웨어가 자동으로 포함됩니다.

<!-- To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is set in your application's `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard. -->
웹훅 확인을 활성화하려면 `STRIPE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 설정되어 있는지 확인하세요. 웹훅 `secret`는 Stripe 계정 대시보드에서 검색할 수 있습니다.

<a name="single-charges"></a>
<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>
<!-- ### Simple Charge -->
### Simple Charge

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance. You will need to [provide a payment method identifier](#payment-methods-for-single-charges) as the second argument to the `charge` method: -->
고객에게 일회성 비용을 청구하려면 청구 가능한 모델 인스턴스에서 `charge` 메서드를 사용할 수 있습니다. `charge` 메서드에 대한 두 번째 인수로 [provide a payment method identifier](#payment-methods-for-single-charges)해야 합니다.

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

<!-- The `charge` method accepts an array as its third argument, allowing you to pass any options you wish to the underlying Stripe charge creation. More information regarding the options available to you when creating charges may be found in the [Stripe documentation](https://stripe.com/docs/api/charges/create): -->
`charge` 메서드는 배열을 세 번째 인수로 허용하므로 기본 Stripe 요금 생성에 원하는 옵션을 전달할 수 있습니다. 요금을 생성할 때 사용할 수 있는 옵션에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/api/charges/create)에서 확인할 수 있습니다.

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

<!-- You may also use the `charge` method without an underlying customer or user. To accomplish this, invoke the `charge` method on a new instance of your application's billable model: -->
기본 고객이나 사용자 없이 `charge` 메서드를 사용할 수도 있습니다. 이를 수행하려면 애플리케이션의 청구 가능한 모델의 새 인스턴스에서 `charge` 메서드를 호출하십시오.

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

<!-- The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method: -->
청구에 실패하면 `charge` 메서드에서 예외가 발생합니다. 요금이 성공적으로 청구되면 `Laravel\Cashier\Payment` 인스턴스가 메서드에서 반환됩니다.

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]
> `charge` 메서드는 애플리케이션에서 사용되는 통화의 가장 낮은 분모로 결제 금액을 허용합니다. 예를 들어, 고객이 미국 달러로 지불하는 경우 금액은 페니로 지정되어야 합니다.

<a name="charge-with-invoice"></a>
<!-- ### Charge With Invoice -->
### Charge With Invoice

<!-- Sometimes you may need to make a one-time charge and offer a PDF invoice to your customer. The `invoicePrice` method lets you do just that. For example, let's invoice a customer for five new shirts: -->
때로는 일회성 비용을 청구하고 고객에게 PDF 송장을 제공해야 할 수도 있습니다. `invoicePrice` 메서드를 사용하면 바로 이러한 작업을 수행할 수 있습니다. 예를 들어 고객에게 새 셔츠 5벌에 대한 송장을 발행해 보겠습니다.

```php
$user->invoicePrice('price_tshirt', 5);
```

<!-- The invoice will be immediately charged against the user's default payment method. The `invoicePrice` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array which should contain the billing options for the invoice itself: -->
청구서는 사용자의 기본 결제 수단으로 즉시 청구됩니다. `invoicePrice` 메서드는 세 번째 인수로 배열을 허용합니다. 이 배열에는 송장 항목에 대한 청구 옵션이 포함되어 있습니다. 이 메서드에서 허용하는 네 번째 인수는 송장 자체에 대한 청구 옵션을 포함해야 하는 배열이기도 합니다.

```php
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

<!-- Similarly to `invoicePrice`, you may use the `tabPrice` method to create a one-time charge for multiple items (up to 250 items per invoice) by adding them to the customer's "tab" and then invoicing the customer. For example, we may invoice a customer for five shirts and two mugs: -->
`invoicePrice`와 마찬가지로 `tabPrice` 메서드를 사용하여 여러 품목(송장당 최대 250개 품목)에 대해 일회성 요금을 생성할 수 있습니다. 이를 고객의 "탭"에 추가한 다음 고객에게 송장을 발행합니다. 예를 들어 고객에게 셔츠 5개와 머그잔 2개에 대한 송장을 보낼 수 있습니다.

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

<!-- Alternatively, you may use the `invoiceFor` method to make a "one-off" charge against the customer's default payment method: -->
또는 `invoiceFor` 메서드를 사용하여 고객의 기본 결제 수단에 대해 "일회성" 청구를 할 수도 있습니다.

```php
$user->invoiceFor('One Time Fee', 500);
```

<!-- Although the `invoiceFor` method is available for you to use, it is recommended that you use the `invoicePrice` and `tabPrice` methods with pre-defined prices. By doing so, you will have access to better analytics and data within your Stripe dashboard regarding your sales on a per-product basis. -->
`invoiceFor` 메서드를 사용할 수 있지만 사전 정의된 가격으로 `invoicePrice` 및 `tabPrice` 메서드를 사용하는 것이 좋습니다. 이렇게 하면 Stripe 대시보드 내에서 제품별 판매와 관련된 더 나은 분석 및 데이터에 액세스할 수 있습니다.

> [!WARNING]
> `invoice`, `invoicePrice` 및 `invoiceFor` 메서드는 실패한 청구 시도를 다시 시도하는 Stripe 송장을 생성합니다. 청구서에서 실패한 청구를 다시 시도하지 않으려면 첫 번째 청구 실패 후 Stripe API를 사용하여 청구서를 마감해야 합니다.

<a name="creating-payment-intents"></a>
<!-- ### Creating Payment Intents -->
### Creating Payment Intents

<!-- You can create a new Stripe payment intent by invoking the `pay` method on a billable model instance. Calling this method will create a payment intent that is wrapped in a `Laravel\Cashier\Payment` instance: -->
청구 가능한 모델 인스턴스에서 `pay` 메서드를 호출하여 새로운 Stripe 결제 의도를 생성할 수 있습니다. 이 메서드를 호출하면 `Laravel\Cashier\Payment` 인스턴스에 래핑된 결제 인텐트가 생성됩니다.

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

<!-- After creating the payment intent, you can return the client secret to your application's frontend so that the user can complete the payment in their browser. To read more about building entire payment flows using Stripe payment intents, please consult the [Stripe documentation](https://stripe.com/docs/payments/accept-a-payment?platform=web). -->
결제 의도를 생성한 후 사용자가 브라우저에서 결제를 완료할 수 있도록 클라이언트 비밀번호를 애플리케이션의 프론트엔드에 반환할 수 있습니다. Stripe 결제 의도를 사용하여 전체 결제 흐름을 구축하는 방법에 대해 자세히 알아보려면 [Stripe documentation](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참조하세요.

<!-- When using the `pay` method, the default payment methods that are enabled within your Stripe dashboard will be available to the customer. Alternatively, if you only want to allow for some specific payment methods to be used, you may use the `payWith` method: -->
`pay` 메서드를 사용하는 경우 고객은 Stripe 대시보드 내에서 활성화된 기본 결제 수단을 사용할 수 있습니다. 또는 일부 특정 결제 수단만 사용하도록 허용하려는 경우 `payWith` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->payWith(
        $request->get('amount'), ['card', 'bancontact']
    );

    return $payment->client_secret;
});
```

> [!WARNING]
> `pay` 및 `payWith` 메서드는 애플리케이션에서 사용되는 통화의 가장 낮은 분모로 결제 금액을 허용합니다. 예를 들어, 고객이 미국 달러로 지불하는 경우 금액은 페니로 지정되어야 합니다.

<a name="refunding-charges"></a>
<!-- ### Refunding Charges -->
### Refunding Charges

<!-- If you need to refund a Stripe charge, you may use the `refund` method. This method accepts the Stripe [payment intent ID](#payment-methods-for-single-charges) as its first argument: -->
Stripe 요금을 환불해야 하는 경우 `refund` 메서드를 사용할 수 있습니다. 이 메서드는 Stripe [payment intent ID](#payment-methods-for-single-charges)를 첫 번째 인수로 허용합니다.

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
<!-- ## Invoices -->
## Invoices

<a name="retrieving-invoices"></a>
<!-- ### Retrieving Invoices -->
### Retrieving Invoices

<!-- You may easily retrieve an array of a billable model's invoices using the `invoices` method. The `invoices` method returns a collection of `Laravel\Cashier\Invoice` instances: -->
`invoices` 메서드를 사용하면 청구 가능한 모델의 송장 배열을 쉽게 검색할 수 있습니다. `invoices` 메서드는 `Laravel\Cashier\Invoice` 인스턴스 컬렉션을 반환합니다.

```php
$invoices = $user->invoices();
```

<!-- If you would like to include pending invoices in the results, you may use the `invoicesIncludingPending` method: -->
결과에 보류 중인 송장을 포함하려면 `invoicesIncludingPending` 메서드를 사용할 수 있습니다.

```php
$invoices = $user->invoicesIncludingPending();
```

<!-- You may use the `findInvoice` method to retrieve a specific invoice by its ID: -->
`findInvoice` 메서드를 사용하여 ID별로 특정 송장을 검색할 수 있습니다.

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
<!-- #### Displaying Invoice Information -->
#### Displaying Invoice Information

<!-- When listing the invoices for the customer, you may use the invoice's methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them: -->
고객의 송장을 나열할 때 송장의 메서드를 사용하여 관련 송장 정보를 표시할 수 있습니다. 예를 들어, 사용자가 쉽게 다운로드할 수 있도록 모든 송장을 테이블에 나열할 수 있습니다.

```blade
<table>
    @foreach ($invoices as $invoice)
        <tr>
            <td>{{ $invoice->date()->toFormattedDateString() }}</td>
            <td>{{ $invoice->total() }}</td>
            <td><a href="/user/invoice/{{ $invoice->id }}">Download</a></td>
        </tr>
    @endforeach
</table>
```

<a name="upcoming-invoices"></a>
<!-- ### Upcoming Invoices -->
### Upcoming Invoices

<!-- To retrieve the upcoming invoice for a customer, you may use the `upcomingInvoice` method: -->
고객에 대한 향후 송장을 검색하려면 `upcomingInvoice` 메서드를 사용할 수 있습니다.

```php
$invoice = $user->upcomingInvoice();
```

<!-- Similarly, if the customer has multiple subscriptions, you can also retrieve the upcoming invoice for a specific subscription: -->
마찬가지로, 고객이 여러 구독을 갖고 있는 경우 특정 구독에 대해 예정된 송장을 검색할 수도 있습니다.

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
<!-- ### Previewing Subscription Invoices -->
### Previewing Subscription Invoices

<!-- Using the `previewInvoice` method, you can preview an invoice before making price changes. This will allow you to determine what your customer's invoice will look like when a given price change is made: -->
`previewInvoice` 메서드를 사용하면 가격을 변경하기 전에 송장을 미리 볼 수 있습니다. 이를 통해 특정 가격이 변경될 때 고객의 송장이 어떻게 표시되는지 결정할 수 있습니다.

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

<!-- You may pass an array of prices to the `previewInvoice` method in order to preview invoices with multiple new prices: -->
여러 개의 새로운 가격이 포함된 송장을 미리 보려면 `previewInvoice` 메서드에 일련의 가격을 전달할 수 있습니다.

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
<!-- ### Generating Invoice PDFs -->
### Generating Invoice PDFs

<!-- Before generating invoice PDFs, you should use Composer to install the Dompdf library, which is the default invoice renderer for Cashier: -->
송장 PDF를 생성하기 전에 Composer를 사용하여 Cashier의 기본 송장 렌더러인 Dompdf 라이브러리를 설치해야 합니다.

```shell
composer require dompdf/dompdf
```

<!-- From within a route or controller, you may use the `downloadInvoice` method to generate a PDF download of a given invoice. This method will automatically generate the proper HTTP response needed to download the invoice: -->
라우트 또는 컨트롤러 내에서 `downloadInvoice` 메서드를 사용하여 특정 송장의 PDF 다운로드를 생성할 수 있습니다. 이 메서드는 송장을 다운로드하는 데 필요한 적절한 HTTP 응답을 자동으로 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

<!-- By default, all data on the invoice is derived from the customer and invoice data stored in Stripe. The filename is based on your `app.name` config value. However, you can customize some of this data by providing an array as the second argument to the `downloadInvoice` method. This array allows you to customize information such as your company and product details: -->
기본적으로 송장의 모든 데이터는 Stripe에 저장된 고객 및 송장 데이터에서 파생됩니다. 파일 이름은 `app.name` 구성 값을 기반으로 합니다. 그러나 배열을 `downloadInvoice` 메서드의 두 번째 인수로 제공하여 이 데이터 중 일부를 사용자 지정할 수 있습니다. 이 배열을 사용하면 회사 및 제품 세부 정보와 같은 정보를 사용자 지정할 수 있습니다.

```php
return $request->user()->downloadInvoice($invoiceId, [
    'vendor' => 'Your Company',
    'product' => 'Your Product',
    'street' => 'Main Str. 1',
    'location' => '2000 Antwerp, Belgium',
    'phone' => '+32 499 00 00 00',
    'email' => 'info@example.com',
    'url' => 'https://example.com',
    'vendorVat' => 'BE123456789',
]);
```

<!-- The `downloadInvoice` method also allows for a custom filename via its third argument. This filename will automatically be suffixed with `.pdf`: -->
`downloadInvoice` 메서드는 세 번째 인수를 통해 사용자 지정 파일 이름도 허용합니다. 이 파일 이름에는 자동으로 `.pdf` 접미사가 붙습니다.

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
<!-- #### Custom Invoice Renderer -->
#### Custom Invoice Renderer

<!-- Cashier also makes it possible to use a custom invoice renderer. By default, Cashier uses the `DompdfInvoiceRenderer` implementation, which utilizes the [dompdf](https://github.com/dompdf/dompdf) PHP library to generate Cashier's invoices. However, you may use any renderer you wish by implementing the `Laravel\Cashier\Contracts\InvoiceRenderer` interface. For example, you may wish to render an invoice PDF using an API call to a third-party PDF rendering service: -->
Cashier를 사용하면 맞춤형 송장 렌더러를 사용할 수도 있습니다. 기본적으로 Cashier는 [dompdf](https://github.com/dompdf/dompdf) PHP 라이브러리를 활용하여 Cashier의 송장을 생성하는 `DompdfInvoiceRenderer` 구현을 사용합니다. 그러나 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현하여 원하는 렌더러를 사용할 수 있습니다. 예를 들어, 타사 PDF 렌더링 서비스에 대한 API 호출을 사용하여 송장 PDF를 렌더링할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * Render the given invoice and return the raw PDF bytes.
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

<!-- Once you have implemented the invoice renderer contract, you should update the `cashier.invoices.renderer` configuration value in your application's `config/cashier.php` configuration file. This configuration value should be set to the class name of your custom renderer implementation. -->
송장 렌더러 계약을 구현한 후에는 애플리케이션의 `config/cashier.php` 구성 파일에서 `cashier.invoices.renderer` 구성 값을 업데이트해야 합니다. 이 구성 값은 사용자 지정 렌더러 구현의 클래스 이름으로 설정되어야 합니다.

<a name="checkout"></a>
<!-- ## Checkout -->
## Checkout

<!-- Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page. -->
Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout)도 지원합니다. Stripe Checkout은 사전 구축된 호스팅 결제 페이지를 제공함으로써 결제를 허용하는 사용자 지정 페이지를 구현하는 수고를 덜어줍니다.

<!-- The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout). -->
다음 문서에는 Cashier로 Stripe Checkout을 사용하여 시작하는 방법에 대한 정보가 포함되어 있습니다. Stripe Checkout에 대해 자세히 알아보려면 [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout) 검토도 고려해야 합니다.

<a name="product-checkouts"></a>
<!-- ### Product Checkouts -->
### Product Checkouts

<!-- You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID: -->
청구 가능한 모델에서 `checkout` 메서드를 사용하여 Stripe 대시보드 내에서 생성된 기존 제품에 대한 체크아웃을 수행할 수 있습니다. `checkout` 메서드는 새로운 Stripe Checkout 세션을 시작합니다. 기본적으로 Stripe 가격 ID를 전달해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

<!-- If needed, you may also specify a product quantity: -->
필요한 경우 제품 수량을 지정할 수도 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

<!-- When a customer visits this route they will be redirected to Stripe's Checkout page. By default, when a user successfully completes or cancels a purchase they will be redirected to your `home` route location, but you may specify custom callback URLs using the `success_url` and `cancel_url` options: -->
고객이 이 라우트를 방문하면 Stripe의 결제 페이지로 리디렉션됩니다. 기본적으로 사용자가 구매를 성공적으로 완료하거나 취소하면 `home` 라우트 위치로 리디렉션되지만 `success_url` 및 `cancel_url` 옵션을 사용하여 사용자 지정 콜백 URL을 지정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

<!-- When defining your `success_url` checkout option, you may instruct Stripe to add the checkout session ID as a query string parameter when invoking your URL. To do so, add the literal string `{CHECKOUT_SESSION_ID}` to your `success_url` query string. Stripe will replace this placeholder with the actual checkout session ID: -->
`success_url` 체크아웃 옵션을 정의할 때 URL를 호출할 때 체크아웃 세션 ID를 쿼리 문자열 매개변수로 추가하도록 Stripe에 지시할 수 있습니다. 이렇게 하려면 리터럴 문자열 `{CHECKOUT_SESSION_ID}`를 `success_url` 쿼리 문자열에 추가하세요. Stripe는 이 자리 표시자를 실제 결제 세션 ID로 대체합니다.

```php
use Illuminate\Http\Request;
use Stripe\Checkout\Session;
use Stripe\Customer;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => route('checkout-cancel'),
    ]);
});

Route::get('/checkout-success', function (Request $request) {
    $checkoutSession = $request->user()->stripe()->checkout->sessions->retrieve($request->get('session_id'));

    return view('checkout.success', ['checkoutSession' => $checkoutSession]);
})->name('checkout-success');
```

<a name="checkout-promotion-codes"></a>
<!-- #### Promotion Codes -->
#### Promotion Codes

<!-- By default, Stripe Checkout does not allow [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes). Luckily, there's an easy way to enable these for your Checkout page. To do so, you may invoke the `allowPromotionCodes` method: -->
기본적으로 Stripe Checkout에서는 [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 허용하지 않습니다. 다행히 결제 페이지에서 이를 활성화하는 쉬운 방법이 있습니다. 그렇게 하려면 `allowPromotionCodes` 메서드를 호출하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
<!-- ### Single Charge Checkouts -->
### Single Charge Checkouts

<!-- You can also perform a simple charge for an ad-hoc product that has not been created in your Stripe dashboard. To do so you may use the `checkoutCharge` method on a billable model and pass it a chargeable amount, a product name, and an optional quantity. When a customer visits this route they will be redirected to Stripe's Checkout page: -->
Stripe 대시보드에서 생성되지 않은 임시 제품에 대해 단순 청구를 수행할 수도 있습니다. 이렇게 하려면 청구 가능한 모델에서 `checkoutCharge` 메서드를 사용하고 청구 가능한 금액, 제품 이름 및 선택적 수량을 전달할 수 있습니다. 고객이 이 라우트를 방문하면 Stripe의 결제 페이지로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` 메서드를 사용하면 Stripe는 항상 Stripe 대시보드에 새로운 제품과 가격을 생성합니다. 따라서 Stripe 대시보드에서 제품을 미리 생성하고 대신 `checkout` 메서드를 사용하는 것이 좋습니다.

<a name="subscription-checkouts"></a>
<!-- ### Subscription Checkouts -->
### Subscription Checkouts

> [!WARNING]
> 구독을 위해 Stripe Checkout을 사용하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 활성화해야 합니다. 이 웹훅은 데이터베이스에 구독 기록을 생성하고 모든 관련 구독 항목을 저장합니다.

<!-- You may also use Stripe Checkout to initiate subscriptions. After defining your subscription with Cashier's subscription builder methods, you may call the `checkout `method. When a customer visits this route they will be redirected to Stripe's Checkout page: -->
Stripe Checkout을 사용하여 구독을 시작할 수도 있습니다. Cashier의 구독 빌더 메서드로 구독을 정의한 후 `checkout ` 메서드를 호출할 수 있습니다. 고객이 이 라우트를 방문하면 Stripe의 결제 페이지로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

<!-- Just as with product checkouts, you may customize the success and cancellation URLs: -->
제품 결제와 마찬가지로 성공 및 취소 URL을 맞춤 설정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout([
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

<!-- Of course, you can also enable promotion codes for subscription checkouts: -->
물론 구독 결제를 위해 프로모션 코드를 활성화할 수도 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->allowPromotionCodes()
        ->checkout();
});
```

> [!WARNING]
> 안타깝게도 Stripe Checkout은 구독을 시작할 때 모든 구독 청구 옵션을 지원하지 않습니다. 구독 빌더에서 `anchorBillingCycleOn` 메서드를 사용하거나 비례 배분 방식을 설정하거나 결제 방식을 설정하면 Stripe Checkout 세션 중에는 아무런 영향을 미치지 않습니다. 사용 가능한 매개변수를 검토하려면 [the Stripe Checkout Session API documentation](https://stripe.com/docs/api/checkout/sessions/create)를 참조하세요.

<a name="stripe-checkout-trial-periods"></a>
<!-- #### Stripe Checkout and Trial Periods -->
#### Stripe Checkout and Trial Periods

<!-- Of course, you can define a trial period when building a subscription that will be completed using Stripe Checkout: -->
물론, Stripe Checkout을 사용하여 완료할 구독을 구축할 때 시험 기간을 정의할 수 있습니다.

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<!-- However, the trial period must be at least 48 hours, which is the minimum amount of trial time supported by Stripe Checkout. -->
그러나 평가판 기간은 Stripe Checkout에서 지원하는 최소 평가판 시간인 48시간 이상이어야 합니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
<!-- #### Subscriptions and Webhooks -->
#### Subscriptions and Webhooks

<!-- Remember, Stripe and Cashier update subscription statuses via webhooks, so there's a possibility a subscription might not yet be active when the customer returns to the application after entering their payment information. To handle this scenario, you may wish to display a message informing the user that their payment or subscription is pending. -->
Stripe 및 Cashier는 웹후크를 통해 구독 상태를 업데이트하므로 고객이 결제 정보를 입력한 후 애플리케이션으로 돌아올 때 구독이 아직 활성화되지 않았을 가능성이 있다는 점을 기억하세요. 이 시나리오를 처리하기 위해 사용자에게 결제 또는 구독이 보류 중임을 알리는 메시지를 표시할 수 있습니다.

<a name="collecting-tax-ids"></a>
<!-- ### Collecting Tax IDs -->
### Collecting Tax IDs

<!-- Checkout also supports collecting a customer's Tax ID. To enable this on a checkout session, invoke the `collectTaxIds` method when creating the session: -->
Checkout에서는 고객의 세금 ID 수집도 지원합니다. 결제 세션에서 이를 활성화하려면 세션을 생성할 때 `collectTaxIds` 메서드를 호출하십시오.

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

<!-- When this method is invoked, a new checkbox will be available to the customer that allows them to indicate if they're purchasing as a company. If so, they will have the opportunity to provide their Tax ID number. -->
이 메서드가 호출되면 고객이 회사로서 구매하는지 여부를 표시할 수 있는 새 확인란을 사용할 수 있습니다. 그렇다면 세금 ID 번호를 제공할 기회가 주어집니다.

> [!WARNING]
> 애플리케이션의 서비스 프로바이더에서 [automatic tax collection](#tax-configuration)를 이미 구성한 경우 이 기능이 자동으로 활성화되며 `collectTaxIds` 메서드를 호출할 필요가 없습니다.

<a name="guest-checkouts"></a>
<!-- ### Guest Checkouts -->
### Guest Checkouts

<!-- Using the `Checkout::guest` method, you may initiate checkout sessions for guests of your application that do not have an "account": -->
`Checkout::guest` 메서드를 사용하면 "계정"이 없는 애플리케이션 게스트에 대한 체크아웃 세션을 시작할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()->create('price_tshirt', [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

<!-- Similarly to when creating checkout sessions for existing users, you may utilize additional methods available on the `Laravel\Cashier\CheckoutBuilder` instance to customize the guest checkout session: -->
기존 사용자를 위한 체크아웃 세션을 생성할 때와 마찬가지로 `Laravel\Cashier\CheckoutBuilder` 인스턴스에서 사용 가능한 추가 메서드를 활용하여 손님 체크아웃 세션을 사용자 지정할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()
        ->withPromotionCode('promo-code')
        ->create('price_tshirt', [
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

<!-- After a guest checkout has been completed, Stripe can dispatch a `checkout.session.completed` webhook event, so make sure to [configure your Stripe webhook](https://dashboard.stripe.com/webhooks) to actually send this event to your application. Once the webhook has been enabled within the Stripe dashboard, you may [handle the webhook with Cashier](#handling-stripe-webhooks). The object contained in the webhook payload will be a [checkout object](https://stripe.com/docs/api/checkout/sessions/object) that you may inspect in order to fulfill your customer's order. -->
게스트 체크아웃이 완료된 후 Stripe는 디스패치를 `checkout.session.completed` 웹훅 이벤트로 설정할 수 있으므로 실제로 이 이벤트를 애플리케이션에 보내려면 [configure your Stripe webhook](https://dashboard.stripe.com/webhooks)해야 합니다. Stripe 대시보드 내에서 웹훅이 활성화되면 [handle the webhook with Cashier](#handling-stripe-webhooks)할 수 있습니다. 웹훅 페이로드에 포함된 개체는 고객의 주문을 이행하기 위해 검사할 수 있는 [checkout object](https://stripe.com/docs/api/checkout/sessions/object)입니다.

<a name="handling-failed-payments"></a>
<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed. -->
때로는 구독 또는 단일 청구에 대한 결제가 실패할 수 있습니다. 이런 일이 발생하면 Cashier는 이러한 일이 발생했음을 알리는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이 예외를 포착한 후 진행 방법에 대한 두 가지 옵션이 있습니다.

<!-- First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page: -->
먼저 고객을 Cashier에 포함된 전용 결제 확인 페이지로 리디렉션할 수 있습니다. 이 페이지에는 이미 Cashier의 서비스 프로바이더를 통해 등록된 라우트라는 연결 항목이 있습니다. 따라서 `IncompletePayment` 예외를 포착하고 사용자를 결제 확인 페이지로 리디렉션할 수 있습니다.

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $subscription = $user->newSubscription('default', 'price_monthly')
        ->create($paymentMethod);
} catch (IncompletePayment $exception) {
    return redirect()->route(
        'cashier.payment',
        [$exception->payment->id, 'redirect' => route('home')]
    );
}
```

<!-- On the payment confirmation page, the customer will be prompted to enter their credit card information again and perform any additional actions required by Stripe, such as "3D Secure" confirmation. After confirming their payment, the user will be redirected to the URL provided by the `redirect` parameter specified above. Upon redirection, `message` (string) and `success` (integer) query string variables will be added to the URL. The payment page currently supports the following payment method types: -->
결제 확인 페이지에서 고객은 신용 카드 정보를 다시 입력하고 "3D Secure" 확인과 같이 Stripe에서 요구하는 추가 작업을 수행하라는 메시지를 받게 됩니다. 결제를 확인한 후 사용자는 위에 지정된 `redirect` 매개변수에서 제공하는 URL로 리디렉션됩니다. 리디렉션 시 `message`(문자열) 및 `success`(정수) 쿼리 문자열 변수가 URL에 추가됩니다. 결제 페이지는 현재 다음과 같은 결제 수단 유형을 지원합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Credit Cards
- Alipay
- Bancontact
- BECS Direct Debit
- EPS
- Giropay
- iDEAL
- SEPA Direct Debit
-->
- 신용카드
- 알리페이
- 반콘택트
- BECS 자동이체
- EPS
- 지로페이
- 이상적인
- SEPA 자동이체

<!-- </div> -->
</div>

<!-- Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions. -->
또는 Stripe가 결제 확인을 처리하도록 허용할 수도 있습니다. 이 경우 결제 확인 페이지로 리디렉션하는 대신 Stripe 대시보드에서 [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic)할 수 있습니다. 그러나 `IncompletePayment` 예외가 발생하는 경우 사용자에게 추가 결제 확인 지침이 포함된 이메일을 받게 될 것임을 알려야 합니다.

<!-- Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions. -->
`Billable` 트레이트를 사용하는 모델의 `charge`, `invoiceFor` 및 `invoice` 메서드에 대해 지불 예외가 발생할 수 있습니다. 구독과 상호 작용할 때 `SubscriptionBuilder`의 `create` 메서드와 `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice` 및 `swapAndInvoice` 메서드에서 불완전한 결제 예외가 발생할 수 있습니다.

<!-- Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
기존 구독에 불완전한 결제가 있는지 확인하려면 청구 가능한 모델 또는 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용하여 수행할 수 있습니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

<!-- You can derive the specific status of an incomplete payment by inspecting the `payment` property on the exception instance: -->
예외 인스턴스에서 `payment` 속성을 검사하여 불완전한 결제의 특정 상태를 파생할 수 있습니다.

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // Get the payment intent status...
    $exception->payment->status;

    // Check specific conditions...
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```

<a name="confirming-payments"></a>
<!-- ### Confirming Payments -->
### Confirming Payments

<!-- Some payment methods require additional data in order to confirm payments. For example, SEPA payment methods require additional "mandate" data during the payment process. You may provide this data to Cashier using the `withPaymentConfirmationOptions` method: -->
일부 결제 수단에는 결제를 확인하기 위해 추가 데이터가 필요합니다. 예를 들어, SEPA 결제 수단에는 결제 프로세스 중에 추가 "명령" 데이터가 필요합니다. `withPaymentConfirmationOptions` 메서드를 사용하여 이 데이터를 Cashier에 제공할 수 있습니다.

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

<!-- You may consult the [Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm) to review all of the options accepted when confirming payments. -->
[Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm)를 참조하여 결제 확인 시 허용되는 모든 옵션을 검토할 수 있습니다.

<a name="strong-customer-authentication"></a>
<!-- ## Strong Customer Authentication -->
## Strong Customer Authentication

<!-- If your business or one of your customers is based in Europe you will need to abide by the EU's Strong Customer Authentication (SCA) regulations. These regulations were imposed in September 2019 by the European Union to prevent payment fraud. Luckily, Stripe and Cashier are prepared for building SCA compliant applications. -->
귀하의 회사 또는 고객 중 한 명이 유럽에 본사를 두고 있는 경우 EU의 SCA(강력한 고객 인증) 규정을 준수해야 합니다. 이 규정은 결제 사기를 방지하기 위해 유럽 연합에서 2019년 9월에 제정한 것입니다. 다행히 Stripe 및 Cashier는 SCA 호환 애플리케이션을 구축할 준비가 되어 있습니다.

> [!WARNING]
> 시작하기 전에 [Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication)와 [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication)를 검토하세요.

<a name="payments-requiring-additional-confirmation"></a>
<!-- ### Payments Requiring Additional Confirmation -->
### Payments Requiring Additional Confirmation

<!-- SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions can be found in the documentation on [handling failed payments](#handling-failed-payments). -->
SCA 규정에 따라 결제를 확인하고 처리하기 위해 추가 확인이 필요한 경우가 많습니다. 이런 일이 발생하면 Cashier는 추가 확인이 필요함을 알리는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이러한 예외를 처리하는 방법에 대한 자세한 내용은 [handling failed payments](#handling-failed-payments) 문서에서 확인할 수 있습니다.

<!-- Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
Stripe 또는 Cashier가 제공하는 결제 확인 화면은 특정 은행이나 카드 발급사의 결제 흐름에 맞게 맞춤화될 수 있으며 추가 카드 확인, 임시 소액 청구, 별도의 장치 인증 또는 기타 형태의 확인이 포함될 수 있습니다.

<a name="incomplete-and-past-due-state"></a>
<!-- #### Incomplete and Past Due State -->
#### Incomplete and Past Due State

<!-- When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion. -->
결제에 추가 확인이 필요한 경우 구독은 `stripe_status` 데이터베이스 열에 표시된 대로 `incomplete` 또는 `past_due` 상태로 유지됩니다. Cashier는 결제 확인이 완료되고 웹후크를 통해 Stripe가 애플리케이션 완료 알림을 보내는 즉시 고객의 구독을 자동으로 활성화합니다.

<!-- For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status). -->
`incomplete` 및 `past_due` 상태에 대한 자세한 내용은 [our additional documentation on these states](#incomplete-and-past-due-status)를 참조하세요.

<a name="off-session-payment-notifications"></a>
<!-- ### Off-Session Payment Notifications -->
### Off-Session Payment Notifications

<!-- Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to a notification class. By default, this notification is disabled. Of course, Cashier includes a notification class you may use for this purpose, but you are free to provide your own notification class if desired: -->
SCA 규정에 따라 고객은 구독이 활성화된 동안에도 때때로 결제 세부 정보를 확인해야 하므로 Cashier는 세션 외 결제 확인이 필요할 때 고객에게 알림을 보낼 수 있습니다. 예를 들어, 구독이 갱신될 때 이런 일이 발생할 수 있습니다. Cashier의 결제 알림은 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수를 알림 클래스로 설정하여 활성화할 수 있습니다. 기본적으로 이 알림은 비활성화되어 있습니다. 물론 Cashier에는 이 목적으로 사용할 수 있는 알림 클래스가 포함되어 있지만 원하는 경우 고유한 알림 클래스를 자유롭게 제공할 수 있습니다.

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

<!-- To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait. -->
세션 외 결제 확인 알림이 전달되도록 하려면 애플리케이션에 [Stripe webhooks are configured](#handling-stripe-webhooks)되고 `invoice.payment_action_required` 웹훅이 Stripe 대시보드에서 활성화되어 있는지 확인하세요. 또한 `Billable` 모델은 Laravel의 `Illuminate\Notifications\Notifiable` 트레이트도 사용해야 합니다.

> [!WARNING]
> 고객이 추가 확인이 필요한 수동 결제를 하는 경우에도 알림이 전송됩니다. 불행하게도 Stripe에서는 결제가 수동으로 이루어졌는지 또는 "세션 외"로 이루어졌는지 알 수 있는 방법이 없습니다. 그러나 고객이 이미 결제를 확인한 후 결제 페이지를 방문하면 '결제 성공' 메시지만 표시됩니다. 고객이 실수로 동일한 결제를 두 번 확인하여 실수로 두 번째 요금이 청구되는 일은 허용되지 않습니다.

<a name="stripe-sdk"></a>
<!-- ## Stripe SDK -->
## Stripe SDK

<!-- Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method: -->
Cashier 개체 중 다수는 Stripe SDK 개체를 둘러싼 래퍼입니다. Stripe 개체와 직접 상호 작용하려면 `asStripe` 메서드를 사용하여 편리하게 검색할 수 있습니다.

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

<!-- You may also use the `updateStripeSubscription` method to update a Stripe subscription directly: -->
`updateStripeSubscription` 메서드를 사용하여 Stripe 구독을 직접 업데이트할 수도 있습니다.

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

<!-- You may invoke the `stripe` method on the `Cashier` class if you would like to use the `Stripe\StripeClient` client directly. For example, you could use this method to access the `StripeClient` instance and retrieve a list of prices from your Stripe account: -->
`Stripe\StripeClient` 클라이언트를 직접 사용하려는 경우 `Cashier` 클래스에서 `stripe` 메서드를 호출할 수 있습니다. 예를 들어 이 메서드를 사용하여 `StripeClient` 인스턴스에 액세스하고 Stripe 계정에서 가격 목록을 검색할 수 있습니다.

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- When testing an application that uses Cashier, you may mock the actual HTTP requests to the Stripe API; however, this requires you to partially re-implement Cashier's own behavior. Therefore, we recommend allowing your tests to hit the actual Stripe API. While this is slower, it provides more confidence that your application is working as expected and any slow tests may be placed within their own Pest / PHPUnit testing group. -->
Cashier를 사용하는 애플리케이션을 테스트할 때 실제 HTTP 요청을 Stripe API로 모의할 수 있습니다. 그러나 이를 위해서는 Cashier 자체 동작을 부분적으로 다시 구현해야 합니다. 따라서 테스트가 실제 Stripe API에 도달하도록 허용하는 것이 좋습니다. 속도는 느리지만 애플리케이션이 예상대로 작동하고 있다는 확신을 더 많이 제공하며 느린 테스트는 자체 Pest / PHPUnit 테스트 그룹 내에 배치될 수 있습니다.

<!-- When testing, remember that Cashier itself already has a great test suite, so you should only focus on testing the subscription and payment flow of your own application and not every underlying Cashier behavior. -->
테스트할 때 Cashier 자체에는 이미 훌륭한 테스트 모음이 있다는 점을 기억하십시오. 따라서 모든 기본 Cashier 동작이 아니라 자신의 애플리케이션의 구독 및 결제 흐름을 테스트하는 데에만 집중해야 합니다.

<!-- To get started, add the **testing** version of your Stripe secret to your `phpunit.xml` file: -->
시작하려면 Stripe 비밀의 **테스트** 버전을 `phpunit.xml` 파일에 추가하세요.

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

<!-- Now, whenever you interact with Cashier while testing, it will send actual API requests to your Stripe testing environment. For convenience, you should pre-fill your Stripe testing account with subscriptions / prices that you may use during testing. -->
이제 테스트하는 동안 Cashier와 상호 작용할 때마다 실제 API 요청을 Stripe 테스트 환경으로 보냅니다. 편의를 위해 테스트에 사용할 수 있는 구독/가격으로 Stripe 테스트 계정을 미리 채워야 합니다.

> [!NOTE]
> 신용 카드 거부 및 실패와 같은 다양한 청구 시나리오를 테스트하려면 Stripe에서 제공하는 광범위한 [testing card numbers and tokens](https://stripe.com/docs/testing)을 사용할 수 있습니다.
