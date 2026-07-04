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
- [Checkout](#checkout)
    - [Product Checkouts](#product-checkouts)
    - [Single Charge Checkouts](#single-charge-checkouts)
    - [Subscription Checkouts](#subscription-checkouts)
    - [Collecting Tax IDs](#collecting-tax-ids)
    - [Guest Checkouts](#guest-checkouts)
- [Invoices](#invoices)
    - [Retrieving Invoices](#retrieving-invoices)
    - [Upcoming Invoices](#upcoming-invoices)
    - [Previewing Subscription Invoices](#previewing-subscription-invoices)
    - [Generating Invoice PDFs](#generating-invoice-pdfs)
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
[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe's](https://stripe.com)의 구독 결제 서비스를 사용할 수 있도록 간결하고 직관적인 인터페이스를 제공합니다. 이 패키지는 여러분이 작성하기 번거롭게 느끼는 반복적(subscribe billing) 코드의 거의 모든 부분을 대신 처리해줍니다. 기본적인 구독 관리 외에도 Cashier는 쿠폰 적용, 구독 변경, 구독 "수량" 관리, 취소 유예기간, 인보이스 PDF 생성 등 다양한 기능을 제공합니다.

<a name="upgrading-cashier"></a>

<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md). -->
Cashier를 새로운 버전으로 업그레이드할 때는 반드시 [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

> [!WARNING]
> 변경에 따른 장애를 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`를 이용합니다. Stripe API 버전은 Stripe의 새로운 기능이나 개선사항을 활용하기 위해 소규모 릴리스(minor release)에서 업데이트됩니다.

<a name="installation"></a>

<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Stripe using the Composer package manager: -->
먼저 Composer 패키지 관리자를 이용해 Stripe용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier
```

<!-- After installing the package, publish Cashier's migrations using the `vendor:publish` Artisan command: -->
패키지를 설치한 후, `vendor:publish` 아티즌 명령어로 Cashier의 마이그레이션을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- Then, migrate your database: -->
이제 데이터베이스를 마이그레이션합니다:

```shell
php artisan migrate
```

<!-- Cashier's migrations will add several columns to your `users` table. They will also create a new `subscriptions` table to hold all of your customer's subscriptions and a `subscription_items` table for subscriptions with multiple prices. -->
Cashier에서 제공하는 마이그레이션은 여러분의 `users` 테이블에 여러 컬럼을 추가합니다. 또한, 고객의 모든 구독 정보를 저장하는 `subscriptions` 테이블과, 여러 가격이 포함된 구독을 위한 `subscription_items` 테이블을 새로 생성합니다.

<!-- If you wish, you can also publish Cashier's configuration file using the `vendor:publish` Artisan command: -->
원할 경우, `vendor:publish` Artisan 명령어로 Cashier의 설정 파일도 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

<!-- Lastly, to ensure Cashier properly handles all Stripe events, remember to [configure Cashier's webhook handling](#handling-stripe-webhooks). -->
마지막으로, Stripe에서 발생하는 모든 이벤트를 Cashier가 올바르게 처리할 수 있도록 [configure Cashier's webhook handling](#handling-stripe-webhooks)을 반드시 진행하세요.

> [!WARNING]
> Stripe에서는 Stripe ID를 저장하는 컬럼이 대소문자를 구분하도록 할 것을 권장합니다. 따라서 MySQL을 사용할 경우 `stripe_id` 컬럼의 collation을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe documentation](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>

<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>

<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, add the `Billable` trait to your billable model definition. Typically, this will be the `App\Models\User` model. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information: -->
Cashier를 사용하기 전에, 여러분이 요금을 청구할 모델(주로 `App\Models\User` 모델)에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트를 통해 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 다양한 청구 관련 기능을 간편하게 사용할 수 있습니다:

```
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- Cashier assumes your billable model will be the `App\Models\User` class that ships with Laravel. If you wish to change this you may specify a different model via the `useCustomerModel` method. This method should typically be called in the `boot` method of your `AppServiceProvider` class: -->
Cashier는 기본적으로 Laravel에서 제공하는 `App\Models\User` 클래스를 청구 가능 모델로 가정합니다. 만약 이를 변경하고 싶다면, `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출하면 됩니다:

```
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
> Laravel에서 제공하는 기본 `App\Models\User` 모델이 아닌 다른 모델을 사용하는 경우, 반드시 [Cashier migrations](#installation) 과정에서 제공되는 Cashier의 마이그레이션 파일을 퍼블리시 및 수정하여 새로운 모델의 테이블명과 구조에 맞게 변경해야 합니다.

<a name="api-keys"></a>

<!-- ### API Keys -->
### API Keys

<!-- Next, you should configure your Stripe API keys in your application's `.env` file. You can retrieve your Stripe API keys from the Stripe control panel: -->
다음으로, Stripe API 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Stripe API 키는 Stripe 관리 패널에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 반드시 정의되어 있는지 확인하세요. 이 값은 실제로 Stripe에서 전송된 웹훅인지 검증하는 데 사용됩니다.

<a name="currency-configuration"></a>

<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
Cashier의 기본 통화(currency)는 미국 달러(USD)입니다. 기본 통화를 변경하려면 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정하면 됩니다:

```ini
CASHIER_CURRENCY=eur
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
또한, Cashier의 통화 외에도 인보이스 등에서 금액을 표시할 때 사용할 로케일(locale)도 설정할 수 있습니다. 내부적으로 Cashier는 [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php)를 이용해 금액 표시 시 로케일을 반영합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면, 서버에 PHP 확장 모듈인 `ext-intl`이 설치되어 있어야 하며, 올바르게 설정되어야 합니다.

<a name="tax-configuration"></a>

<!-- ### Tax Configuration -->
### Tax Configuration

<!-- Thanks to [Stripe Tax](https://stripe.com/tax), it's possible to automatically calculate taxes for all invoices generated by Stripe. You can enable automatic tax calculation by invoking the `calculateTaxes` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
[Stripe Tax](https://stripe.com/tax) 덕분에 Stripe에서 생성된 모든 인보이스에 대해 세금을 자동으로 계산할 수 있습니다. 자동 세금 계산을 사용하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

```
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
세금 계산을 활성화하면, 신규 구독 및 일회성 인보이스 모두 자동으로 세금이 계산 및 적용됩니다.

<!-- For this feature to work properly, your customer's billing details, such as the customer's name, address, and tax ID, need to be synced to Stripe. You may use the [customer data synchronization](#syncing-customer-data-with-stripe) and [Tax ID](#tax-ids) methods offered by Cashier to accomplish this. -->
이 기능이 제대로 동작하려면, 고객의 이름, 주소, Tax ID 등 청구 정보가 Stripe로 동기화되어 있어야 합니다. 이때는 Cashier에서 제공하는 [customer data synchronization](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 메서드를 활용하실 수 있습니다.

<a name="logging"></a>

<!-- ### Logging -->
### Logging

<!-- Cashier allows you to specify the log channel to be used when logging fatal Stripe errors. You may specify the log channel by defining the `CASHIER_LOGGER` environment variable within your application's `.env` file: -->
Cashier는 Stripe에서 발생하는 치명적(fatal) 오류를 로깅할 때 사용할 로그 채널을 지정할 수 있습니다. `.env` 파일에서 `CASHIER_LOGGER` 환경 변수를 지정해 설정할 수 있습니다:

```ini
CASHIER_LOGGER=stack
```

<!-- Exceptions that are generated by API calls to Stripe will be logged through your application's default log channel. -->
Stripe API 호출로 인해 발생한 예외는 여러분 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>

<!-- ### Using Custom Models -->
### Using Custom Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
Cashier에서 내부적으로 사용하는 모델을 여러분이 직접 확장하여 정의할 수 있습니다. 이를 위해 직접 커스텀 모델을 작성하고 Cashier의 관련 모델을 상속하면 됩니다:

```
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Cashier\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
커스텀 모델을 정의한 후, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier에서 여러분의 모델을 사용하도록 지정할 수 있습니다. 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 아래처럼 지정합니다:

```
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
> Stripe Checkout을 사용하기 전에, Stripe 대시보드에서 고정 가격의 상품(Products)을 미리 정의해야 합니다. 또한 [configure Cashier's webhook handling](#handling-stripe-webhooks)해야 합니다.

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations. -->
여러분의 애플리케이션에서 상품 및 구독 상품의 결제 기능을 제공하는 것은 쉽지 않게 느껴질 수 있습니다. 하지만 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 현대적이고 견고한 결제 연동을 간단하게 구축할 수 있습니다.

<!-- To charge customers for non-recurring, single-charge products, we'll utilize Cashier to direct customers to Stripe Checkout, where they will provide their payment details and confirm their purchase. Once the payment has been made via Checkout, the customer will be redirected to a success URL of your choosing within your application: -->
비정기 단일 결제 상품을 판매할 때는, Cashier를 통해 고객을 Stripe Checkout으로 리디렉션하여 결제 정보를 입력 받고 구매를 완료하도록 할 수 있습니다. 결제가 완료되면 여러분의 애플리케이션에서 지정한 성공 URL로 고객이 이동하게 됩니다:

```
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
위 예시처럼, Cashier에서 제공하는 `checkout` 메서드를 사용해 고객을 Stripe Checkout으로 리디렉션할 수 있습니다. Stripe에서 말하는 "price"란 [defined prices for specific products](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

<!-- If necessary, the `checkout` method will automatically create a customer in Stripe and connect that Stripe customer record to the corresponding user in your application's database. After completing the checkout session, the customer will be redirected to a dedicated success or cancellation page where you can display an informational message to the customer. -->
필요하다면, `checkout` 메서드는 Stripe에 고객 계정을 자동으로 생성하고, Stripe의 고객 레코드를 애플리케이션의 사용자와 연동시킵니다. 결제가 완료되거나 취소될 경우, 고객은 여러분이 지정한 성공/취소 페이지로 리디렉션됩니다. 이곳에서 안내 메시지 등을 표시할 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>

<!-- #### Providing Meta Data to Stripe Checkout -->
#### Providing Meta Data to Stripe Checkout

<!-- When selling products, it's common to keep track of completed orders and purchased products via `Cart` and `Order` models defined by your own application. When redirecting customers to Stripe Checkout to complete a purchase, you may need to provide an existing order identifier so that you can associate the completed purchase with the corresponding order when the customer is redirected back to your application. -->
상품을 판매할 때, 여러분의 애플리케이션에서 정의한 `Cart` 및 `Order` 모델을 이용해 구매 완료 내역을 기록하거나 주문 정보를 관리하는 것이 일반적입니다. Stripe Checkout을 통한 결제 과정에서 완성된 주문을 특정 주문 ID와 연결해야 할 수도 있습니다.

<!-- To accomplish this, you may provide an array of `metadata` to the `checkout` method. Let's imagine that a pending `Order` is created within our application when a user begins the checkout process. Remember, the `Cart` and `Order` models in this example are illustrative and not provided by Cashier. You are free to implement these concepts based on the needs of your own application: -->
이를 위해 `checkout` 메서드의 옵션 배열에 `metadata`를 추가할 수 있습니다. 예를 들어, 사용자가 결제 과정을 시작하면 애플리케이션 내에 임시 `Order`를 생성한다고 가정합시다. (참고: 이 예시의 `Cart`와 `Order` 모델은 여러분이 직접 구현해야 하며, Cashier에서 자동 제공되는 것은 아닙니다.)

```
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
위와 같이 사용자가 결제를 시작할 때 주문에 연관된 가격 ID들을 모두 `checkout` 메서드에 전달하고, Stripe Checkout 세션의 `metadata`에 주문의 ID도 포함시킵니다. 또한 성공 URL에는 `CHECKOUT_SESSION_ID` 템플릿 변수를 추가했습니다. Stripe Checkout이 완료되어 리디렉션할 때 이 변수는 자동으로 세션 ID로 치환됩니다.

<!-- Next, let's build the Checkout success route. This is the route that users will be redirected to after their purchase has been completed via Stripe Checkout. Within this route, we can retrieve the Stripe Checkout session ID and the associated Stripe Checkout instance in order to access our provided meta data and update our customer's order accordingly: -->
다음으로 Checkout 성공 처리를 담당하는 라우트를 만듭니다. 이 라우트는 Stripe 결제가 완료된 고객이 돌아오게 되는 경로이며, 여기서 세션 ID와 연관된 Stripe Checkout 세션 정보를 조회하고, 저장해둔 메타데이터를 통해 주문 정보를 업데이트합니다:

```
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
Stripe Checkout 세션 객체에 포함된 데이터에 대한 자세한 내용은 [data contained by the Checkout session object](https://stripe.com/docs/api/checkout/sessions/object)를 참고하시기 바랍니다.

<a name="quickstart-selling-subscriptions"></a>

<!-- ### Selling Subscriptions -->
### Selling Subscriptions

> [!NOTE]
> Stripe Checkout을 사용하기 전에, Stripe 대시보드에서 고정 가격의 상품(Products)을 미리 정의해야 합니다. 또한 [configure Cashier's webhook handling](#handling-stripe-webhooks)해야 합니다.

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations. -->
애플리케이션에서 상품 및 구독 결제를 제공하는 것은 처음엔 어려울 수 있지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 누구나 쉽고 안정적으로 결제 연동을 만들 수 있습니다.

<!-- To learn how to sell subscriptions using Cashier and Stripe Checkout, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Stripe dashboard. In addition, our subscription service might offer an Expert plan as `pro_expert`. -->
Cashier와 Stripe Checkout을 사용해 구독 상품을 판매하고 싶다면, 기본적인 시나리오를 살펴보면 좋습니다. 예를 들어 월간(`price_basic_monthly`)과 연간(`price_basic_yearly`)이라는 두 가지 플랜이 있는 "Basic" 상품(`pro_basic`)이 있고, 별도의 Expert 플랜(`pro_expert`)도 있다고 가정해 보겠습니다.

<!-- First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button or link should direct the user to a Laravel route which creates the Stripe Checkout session for their chosen plan: -->
먼저, 고객이 우리의 서비스를 구독하는 과정을 살펴봅니다. 보통 고객은 가격 안내 페이지에서 Basic 플랜의 "구독하기" 버튼을 클릭할 것입니다. 이 버튼이나 링크는 Stripe Checkout 세션을 생성하는 Laravel 라우트로 연결합니다:

```
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
위 코드처럼, 고객을 Stripe Checkout 세션으로 리디렉션하여 Basic 플랜에 가입할 수 있습니다. 결제가 성공하거나 취소되면, `checkout` 메서드에 전달한 URL로 고객이 다시 이동하게 됩니다. 단, 구독이 실제로 시작된 시점을 알려면(일부 결제 방식은 처리에 몇 초가 걸릴 수 있음) [configure Cashier's webhook handling](#handling-stripe-webhooks)해야 합니다.

<!-- Now that customers can start subscriptions, we need to restrict certain portions of our application so that only subscribed users can access them. Of course, we can always determine a user's current subscription status via the `subscribed` method provided by Cashier's `Billable` trait: -->
구독 기능을 제공했다면, 이제 특정 페이지나 기능을 구독한 사용자만 이용할 수 있도록 제한해야겠죠. Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 이용해 사용자의 구독 상태를 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

<!-- We can even easily determine if a user is subscribed to specific product or price: -->
특정 상품 또는 가격에 구독 중인지도 쉽게 확인할 수 있습니다:

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

<!-- For convenience, you may wish to create a [middleware](/docs/11.x/middleware) which determines if the incoming request is from a subscribed user. Once this middleware has been defined, you may easily assign it to a route to prevent users that are not subscribed from accessing the route: -->
좀 더 편리하게 사용하고 싶다면, 요청이 구독한 사용자에 의해 들어왔는지 확인하는 [middleware](/docs/11.x/middleware)를 만들 수도 있습니다. 이를 만든 후에는 미들웨어를 라우트에 할당하여 미구독 사용자의 접근을 막을 수 있습니다:

```
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
작성한 미들웨어는 아래처럼 라우트에 지정할 수 있습니다:

```
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>

<!-- #### Allowing Customers to Manage Their Billing Plan -->
#### Allowing Customers to Manage Their Billing Plan

<!-- Of course, customers may want to change their subscription plan to another product or "tier". The easiest way to allow this is by directing customers to Stripe's [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal), which provides a hosted user interface that allows customers to download invoices, update their payment method, and change subscription plans. -->
고객이 구독하고 있는 상품이나 플랜(티어)을 변경하고 싶어할 수도 있습니다. 이때 가장 간단한 방법은 Stripe의 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)로 유도하는 것입니다. 이 포털에서는 청구서 다운로드, 결제 수단 변경, 구독 플랜 변경 등이 가능한 자체 UI를 제공합니다.

<!-- First, define a link or button within your application that directs users to a Laravel route which we will utilize to initiate a Billing Portal session: -->
먼저, 애플리케이션 내에 Billing 페이지로 이동하는 링크나 버튼을 만듭니다:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

<!-- Next, let's define the route that initiates a Stripe Customer Billing Portal session and redirects the user to the Portal. The `redirectToBillingPortal` method accepts the URL that users should be returned to when exiting the Portal: -->
다음으로, Stripe 결제 포털 세션을 생성하고 사용자를 포털로 리디렉션하는 라우트를 작성합니다. `redirectToBillingPortal` 메서드는 포털에서 나올 때 돌아올 URL을 인자로 받습니다:

```
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 웹훅 핸들링이 설정되어 있으면, Stripe에서 들어오는 웹훅을 Cashier가 처리하여 관련 데이터베이스를 자동으로 동기화합니다. 예를 들어, 사용자가 Stripe의 고객 포털에서 구독을 취소하면, Cashier가 해당 웹훅을 받아 애플리케이션의 구독도 자동으로 '취소됨' 상태로 반영합니다.

<a name="customers"></a>

<!-- ## Customers -->
## Customers

<a name="retrieving-customers"></a>

<!-- ### Retrieving Customers -->
### Retrieving Customers

<!-- You can retrieve a customer by their Stripe ID using the `Cashier::findBillable` method. This method will return an instance of the billable model: -->
`Cashier::findBillable` 메서드를 사용하면 Stripe ID를 기준으로 고객을 조회할 수 있습니다. 이 메서드는 청구 가능 모델의 인스턴스를 반환합니다:

```
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>

<!-- ### Creating Customers -->
### Creating Customers

<!-- Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method: -->
때때로 구독을 바로 시작하지 않고 Stripe 고객만 등록하고 싶을 때가 있습니다. 이럴 때는 `createAsStripeCustomer` 메서드를 사용할 수 있습니다:

```
$stripeCustomer = $user->createAsStripeCustomer();
```

<!-- Once the customer has been created in Stripe, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create): -->
Stripe에 고객이 정상적으로 생성된 후에는 언제든 구독을 시작할 수 있습니다. Stripe API에서 지원하는 [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create)를 추가로 전달하려면 선택적으로 `$options` 배열을 넘기면 됩니다:

```
$stripeCustomer = $user->createAsStripeCustomer($options);
```

<!-- You may use the `asStripeCustomer` method if you want to return the Stripe customer object for a billable model: -->
빌러블 모델에 대한 Stripe 고객 객체를 반환받고 싶다면 `asStripeCustomer` 메서드를 사용하면 됩니다:

```
$stripeCustomer = $user->asStripeCustomer();
```

<!-- The `createOrGetStripeCustomer` method may be used if you would like to retrieve the Stripe customer object for a given billable model but are not sure whether the billable model is already a customer within Stripe. This method will create a new customer in Stripe if one does not already exist: -->
빌러블 모델이 이미 Stripe에 고객으로 등록되어 있는지 모를 경우, `createOrGetStripeCustomer` 메서드를 사용할 수 있습니다. 이미 고객이 Stripe에 있으면 반환하고, 없으면 새로 생성합니다:

```
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>

<!-- ### Updating Customers -->
### Updating Customers

<!-- Occasionally, you may wish to update the Stripe customer directly with additional information. You may accomplish this using the `updateStripeCustomer` method. This method accepts an array of [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update): -->
Stripe의 고객 정보를 직접 추가로 업데이트해야 할 때가 있습니다. 이때는 `updateStripeCustomer` 메서드를 사용하세요. 이 메서드는 Stripe API에서 지원하는 [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update) 배열을 받습니다:

```
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>

<!-- ### Balances -->
### Balances

<!-- Stripe allows you to credit or debit a customer's "balance". Later, this balance will be credited or debited on new invoices. To check the customer's total balance you may use the `balance` method that is available on your billable model. The `balance` method will return a formatted string representation of the balance in the customer's currency: -->
Stripe에서는 고객의 ‘잔액(Balance)’을 충전(credit)하거나 차감(debit)할 수 있습니다. 이후 새로 생성되는 인보이스에서 이 잔액이 적용됩니다. 고객의 총 잔액을 확인하려면 빌러블 모델에서 `balance` 메서드를 사용하세요. `balance` 메서드는 고객의 통화에 맞춘 문자열 형태로 잔액을 반환합니다:

```
$balance = $user->balance();
```

<!-- To credit a customer's balance, you may provide a value to the `creditBalance` method. If you wish, you may also provide a description: -->
고객의 잔액을 충전(credit)하려면, `creditBalance` 메서드에 금액과 원하는 경우 설명을 전달할 수 있습니다:

```
$user->creditBalance(500, 'Premium customer top-up.');
```

<!-- Providing a value to the `debitBalance` method will debit the customer's balance: -->
`debitBalance` 메서드에 값을 전달하면 고객의 잔액이 차감(debit)됩니다:

```
$user->debitBalance(300, 'Bad usage penalty.');
```

<!-- The `applyBalance` method will create new customer balance transactions for the customer. You may retrieve these transaction records using the `balanceTransactions` method, which may be useful in order to provide a log of credits and debits for the customer to review: -->
`applyBalance` 메서드를 사용하면 고객의 잔액에 대한 새 거래 내역(balance transaction)을 생성할 수 있습니다. 고객의 크레딧 및 차감 내역을 로그로 제공하고 싶을 때는 `balanceTransactions` 메서드로 해당 거래들을 조회할 수 있습니다:

```
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
Cashier는 고객의 Tax ID(세금 식별자)를 손쉽게 관리할 수 있는 기능을 제공합니다. 예를 들어, `taxIds` 메서드로 해당 고객에 할당된 [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션으로 받을 수 있습니다:

```
$taxIds = $user->taxIds();
```

<!-- You can also retrieve a specific tax ID for a customer by its identifier: -->
또, ID로 특정 Tax ID를 조회할 수도 있습니다:

```
$taxId = $user->findTaxId('txi_belgium');
```

<!-- You may create a new Tax ID by providing a valid [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) and value to the `createTaxId` method: -->
유효한 [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 `createTaxId` 메서드에 전달하여 새로운 Tax ID를 생성할 수 있습니다:

```
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

<!-- The `createTaxId` method will immediately add the VAT ID to the customer's account. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); however, this is an asynchronous process. You can be notified of verification updates by subscribing to the `customer.tax_id.updated` webhook event and inspecting [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). For more information on handling webhooks, please consult the [documentation on defining webhook handlers](#handling-stripe-webhooks). -->
`createTaxId` 메서드는 VAT ID를 즉시 고객 계정에 추가합니다. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation)하지만, 이 과정은 비동기로 처리됩니다. 검증 단계의 상태 변화를 확인하려면 `customer.tax_id.updated` 웹훅 이벤트를 구독하여 [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 확인할 수 있습니다. 웹훅 처리에 대해서는 [documentation on defining webhook handlers](#handling-stripe-webhooks)를 참고하세요.

<!-- You may delete a tax ID using the `deleteTaxId` method: -->
Tax ID를 삭제하려면 `deleteTaxId` 메서드를 사용합니다:

```
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>

<!-- ### Syncing Customer Data With Stripe -->
### Syncing Customer Data With Stripe

<!-- Typically, when your application's users update their name, email address, or other information that is also stored by Stripe, you should inform Stripe of the updates. By doing so, Stripe's copy of the information will be in sync with your application's. -->
일반적으로, 애플리케이션의 사용자가 이름, 이메일 주소 등 Stripe에도 저장되는 정보를 업데이트할 때 Stripe 측에도 변경 내용을 알려야 합니다. 이렇게 하면 Stripe에 저장된 정보와 여러분의 애플리케이션 정보가 항상 일치하게 됩니다.

<!-- To automate this, you may define an event listener on your billable model that reacts to the model's `updated` event. Then, within your event listener, you may invoke the `syncStripeCustomerDetails` method on the model: -->
이 작업을 자동화하려면, 과금 가능한(billable) 모델에서 `updated` 이벤트가 발생했을 때 실행되는 이벤트 리스너를 정의할 수 있습니다. 이벤트 리스너 내에서는 모델의 `syncStripeCustomerDetails` 메서드를 호출하면 됩니다.

```
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
이제 고객 모델이 업데이트될 때마다 해당 정보가 Stripe와 동기화됩니다. 참고로, Cashier는 고객이 처음 생성될 때 Stripe와 자동으로 고객 정보를 동기화합니다.

<!-- You may customize the columns used for syncing customer information to Stripe by overriding a variety of methods provided by Cashier. For example, you may override the `stripeName` method to customize the attribute that should be considered the customer's "name" when Cashier syncs customer information to Stripe: -->
Stripe로 동기화할 때 사용하는 컬럼을 직접 지정하고 싶다면, Cashier에서 제공하는 여러 메서드를 오버라이드할 수 있습니다. 예를 들어, Stripe와 동기화할 때 사용할 "이름" 속성을 지정하려면 `stripeName` 메서드를 오버라이드할 수 있습니다.

```
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

<!-- Similarly, you may override the `stripeEmail`, `stripePhone`, `stripeAddress`, and `stripePreferredLocales` methods. These methods will sync information to their corresponding customer parameters when [updating the Stripe customer object](https://stripe.com/docs/api/customers/update). If you wish to take total control over the customer information sync process, you may override the `syncStripeCustomerDetails` method. -->
이와 비슷하게, `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales` 메서드도 오버라이드할 수 있습니다. 이러한 메서드는 [updating the Stripe customer object](https://stripe.com/docs/api/customers/update) 시 각각의 고객 파라미터로 정보를 동기화합니다. 만약 고객 정보 동기화 과정을 완전히 제어하고 싶다면, `syncStripeCustomerDetails` 메서드를 직접 오버라이드하면 됩니다.

<a name="billing-portal"></a>

<!-- ### Billing Portal -->
### Billing Portal

<!-- Stripe offers [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) so that your customer can manage their subscription, payment methods, and view their billing history. You can redirect your users to the billing portal by invoking the `redirectToBillingPortal` method on the billable model from a controller or route: -->
Stripe는 [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 이를 통해 고객이 구독, 결제 수단, 결제 내역을 직접 관리할 수 있습니다. 컨트롤러나 라우트에서 과금 가능한(billable) 모델의 `redirectToBillingPortal` 메서드를 호출하면 Stripe 빌링 포털로 사용자를 리디렉션할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

<!-- By default, when the user is finished managing their subscription, they will be able to return to the `home` route of your application via a link within the Stripe billing portal. You may provide a custom URL that the user should return to by passing the URL as an argument to the `redirectToBillingPortal` method: -->
기본적으로 사용자가 구독 관리를 마치면, Stripe 빌링 포털 내의 링크를 통해 애플리케이션의 `home` 라우트로 돌아올 수 있습니다. 사용자가 돌아올 URL을 직접 지정하려면, 해당 URL을 `redirectToBillingPortal` 메서드의 인수로 전달하면 됩니다.

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

<!-- If you would like to generate the URL to the billing portal without generating an HTTP redirect response, you may invoke the `billingPortalUrl` method: -->
HTTP 리디렉션 응답 없이 빌링 포털의 URL만 생성하고 싶다면, `billingPortalUrl` 메서드를 사용할 수 있습니다.

```
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>

<!-- ## Payment Methods -->
## Payment Methods

<a name="storing-payment-methods"></a>

<!-- ### Storing Payment Methods -->
### Storing Payment Methods

<!-- In order to create subscriptions or perform "one-off" charges with Stripe, you will need to store a payment method and retrieve its identifier from Stripe. The approach used to accomplish this differs based on whether you plan to use the payment method for subscriptions or single charges, so we will examine both below. -->
Stripe에서 구독을 생성하거나 단일(one-off) 결제 작업을 수행하려면 결제 수단을 저장하고 Stripe에서 그 식별자를 가져와야 합니다. 결제 수단을 저장하는 방식은 구독에 사용할 것인지 단일 결제에 사용할 것인지에 따라 다르므로, 두 가지 경우를 각각 살펴봅니다.

<a name="payment-methods-for-subscriptions"></a>

<!-- #### Payment Methods for Subscriptions -->
#### Payment Methods for Subscriptions

<!-- When storing a customer's credit card information for future use by a subscription, the Stripe "Setup Intents" API must be used to securely gather the customer's payment method details. A "Setup Intent" indicates to Stripe the intention to charge a customer's payment method. Cashier's `Billable` trait includes the `createSetupIntent` method to easily create a new Setup Intent. You should invoke this method from the route or controller that will render the form which gathers your customer's payment method details: -->
구독을 위해 고객의 신용카드 정보를 저장할 때는 Stripe의 "Setup Intents" API를 사용하여 안전하게 결제 수단을 수집해야 합니다. "Setup Intent"는 Stripe에게 해당 결제 수단을 나중에 사용할 예정임을 알립니다. Cashier의 `Billable` 트레잇에서는 `createSetupIntent` 메서드를 제공하므로, 새로운 Setup Intent를 쉽게 생성할 수 있습니다. 다음과 같이 결제 수단 정보를 입력받을 폼을 렌더링하는 라우트나 컨트롤러에서 이 메서드를 호출합니다.

```
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

<!-- After you have created the Setup Intent and passed it to the view, you should attach its secret to the element that will gather the payment method. For example, consider this "update payment method" form: -->
Setup Intent를 생성해 뷰로 전달했다면, 이 secret 값을 결제 수단 입력 폼의 엘리먼트에 붙여줘야 합니다. 예를 들어, 다음과 같은 "결제 수단 업데이트" 폼을 생각해볼 수 있습니다.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

<!-- Next, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
다음으로, Stripe.js 라이브러리를 사용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 연결하고, 고객의 결제 정보를 안전하게 수집합니다.

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
이후, [Stripe's `confirmCardSetup` method](https://stripe.com/docs/js/setup_intents/confirm_card_setup)를 이용해 카드를 확인하고 Stripe에서 "결제 수단 식별자"를 안전하게 받아올 수 있습니다.

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
카드 정보가 Stripe에서 성공적으로 인증되면, 반환받은 `setupIntent.payment_method` 식별자를 Laravel 애플리케이션에 전달해 고객에 연결할 수 있습니다. 받은 결제 수단은 바로 [added as a new payment method](#adding-payment-methods)하거나, [used to update the default payment method](#updating-the-default-payment-method)할 수도 있습니다. 또는 결제 수단 식별자를 즉시 사용해 [create a new subscription](#creating-subscriptions)할 수도 있습니다.

> [!NOTE]
> Setup Intents 및 고객 결제 정보 수집에 대한 자세한 내용은 [review this overview provided by Stripe](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>

<!-- #### Payment Methods for Single Charges -->
#### Payment Methods for Single Charges

<!-- Of course, when making a single charge against a customer's payment method, we will only need to use a payment method identifier once. Due to Stripe limitations, you may not use the stored default payment method of a customer for single charges. You must allow the customer to enter their payment method details using the Stripe.js library. For example, consider the following form: -->
고객의 결제 수단으로 단 한 번 결제(single charge)를 할 경우, 결제 수단 식별자를 한 번만 사용하면 됩니다. Stripe의 제한 때문에 단일 결제에는 저장된 기본 결제 수단을 사용할 수 없습니다. 고객이 Stripe.js 라이브러리를 통해 결제 정보를 직접 입력하도록 해야 합니다. 예를 들어, 다음과 같은 폼을 사용할 수 있습니다.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

<!-- After defining such a form, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
위와 같이 폼을 정의한 후, Stripe.js 라이브러리를 사용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 연결하고, 고객 결제 정보를 안전하게 수집하십시오.

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
다음으로, [Stripe's `createPaymentMethod` method](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method)를 이용해 카드를 인증하고 Stripe에서 안전한 "결제 수단 식별자"를 받아올 수 있습니다.

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
카드 인증이 성공하면 `paymentMethod.id`를 Laravel 애플리케이션에 전달한 뒤, [single charge](#simple-charge)를 처리할 수 있습니다.

<a name="retrieving-payment-methods"></a>

<!-- ### Retrieving Payment Methods -->
### Retrieving Payment Methods

<!-- The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances: -->
빌링 모델 인스턴스의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스의 컬렉션을 반환합니다.

```
$paymentMethods = $user->paymentMethods();
```

<!-- By default, this method will return payment methods of every type. To retrieve payment methods of a specific type, you may pass the `type` as an argument to the method: -->
이 메서드는 기본적으로 모든 타입의 결제 수단을 반환합니다. 특정 타입의 결제 수단만 조회하려면 `type`을 인수로 전달하세요.

```
$paymentMethods = $user->paymentMethods('sepa_debit');
```

<!-- To retrieve the customer's default payment method, the `defaultPaymentMethod` method may be used: -->
고객의 기본 결제 수단을 가져오려면 `defaultPaymentMethod` 메서드를 사용할 수 있습니다.

```
$paymentMethod = $user->defaultPaymentMethod();
```

<!-- You can retrieve a specific payment method that is attached to the billable model using the `findPaymentMethod` method: -->
빌링 가능한 모델에 연결된 특정 결제 수단을 조회하려면 `findPaymentMethod` 메서드를 사용하면 됩니다.

```
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>

<!-- ### Payment Method Presence -->
### Payment Method Presence

<!-- To determine if a billable model has a default payment method attached to their account, invoke the `hasDefaultPaymentMethod` method: -->
과금 가능한 모델이 기본 결제 수단을 가지고 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 호출할 수 있습니다.

```
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

<!-- You may use the `hasPaymentMethod` method to determine if a billable model has at least one payment method attached to their account: -->
또는, 최소 하나라도 결제 수단이 연결되어 있는지를 확인하려면 `hasPaymentMethod` 메서드를 사용할 수 있습니다.

```
if ($user->hasPaymentMethod()) {
    // ...
}
```

<!-- This method will determine if the billable model has any payment method at all. To determine if a payment method of a specific type exists for the model, you may pass the `type` as an argument to the method: -->
이 메서드는 해당 모델이 어떠한 결제 수단이라도 보유하고 있는지 확인합니다. 만약 특정 타입의 결제 수단이 있는지 확인하려면, 인수로 `type`을 전달하세요.

```
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>

<!-- ### Updating the Default Payment Method -->
### Updating the Default Payment Method

<!-- The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method: -->
`updateDefaultPaymentMethod` 메서드를 이용하면 고객의 기본 결제 수단 정보를 업데이트할 수 있습니다. 이 메서드는 Stripe 결제 수단 식별자를 받아, 해당 결제 수단을 기본 청구 수단으로 지정합니다.

```
$user->updateDefaultPaymentMethod($paymentMethod);
```

<!-- To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method: -->
Stripe에 저장된 고객의 기본 결제 수단 정보를 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용할 수 있습니다.

```
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 고객의 기본 결제 수단은 인보이스 처리 및 신규 구독 생성에만 사용할 수 있습니다. Stripe의 제한 때문에 단일 결제에는 사용이 불가합니다.

<a name="adding-payment-methods"></a>

<!-- ### Adding Payment Methods -->
### Adding Payment Methods

<!-- To add a new payment method, you may call the `addPaymentMethod` method on the billable model, passing the payment method identifier: -->
새로운 결제 수단을 추가하려면, 과금 가능한 모델에서 `addPaymentMethod` 메서드를 호출하고 결제 수단 식별자를 전달하세요.

```
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 식별자를 얻는 방법은 [payment method storage documentation](#storing-payment-methods)를 참고하세요.

<a name="deleting-payment-methods"></a>

<!-- ### Deleting Payment Methods -->
### Deleting Payment Methods

<!-- To delete a payment method, you may call the `delete` method on the `Laravel\Cashier\PaymentMethod` instance you wish to delete: -->
결제 수단을 삭제하려면, 삭제하고자 하는 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```
$paymentMethod->delete();
```

<!-- The `deletePaymentMethod` method will delete a specific payment method from the billable model: -->
특정 결제 수단 하나를 빌링 모델에서 삭제하려면, `deletePaymentMethod` 메서드를 사용할 수 있습니다.

```
$user->deletePaymentMethod('pm_visa');
```

<!-- The `deletePaymentMethods` method will delete all of the payment method information for the billable model: -->
빌링 모델에 연결된 모든 결제 수단 정보를 삭제하려면, `deletePaymentMethods` 메서드를 사용하세요.

```
$user->deletePaymentMethods();
```

<!-- By default, this method will delete payment methods of every type. To delete payment methods of a specific type you can pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 모든 타입의 결제 수단을 삭제합니다. 특정 타입만 삭제하려면, `type`을 인수로 전달하세요.

```
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 사용자가 활성 구독을 가지고 있다면, 애플리케이션에서 그 사용자의 기본 결제 수단 삭제를 허용해서는 안 됩니다.

<a name="subscriptions"></a>

<!-- ## Subscriptions -->
## Subscriptions

<!-- Subscriptions provide a way to set up recurring payments for your customers. Stripe subscriptions managed by Cashier provide support for multiple subscription prices, subscription quantities, trials, and more. -->
구독은 고객을 대상으로 반복 결제를 설정할 수 있는 방법을 제공합니다. Cashier를 통한 Stripe 구독은 복수 구독 가격, 구독 수량, 체험 기간(trial) 등 다양한 기능을 지원합니다.

<a name="creating-subscriptions"></a>

<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription: -->
구독을 생성하려면, 먼저 과금 가능한 모델 인스턴스를 찾아야 합니다. 일반적으로 이 인스턴스는 `App\Models\User`가 될 것입니다. 모델 인스턴스를 찾은 뒤에는 `newSubscription` 메서드를 사용해 구독을 생성할 수 있습니다.

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

<!-- The first argument passed to the `newSubscription` method should be the internal type of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription type is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument is the specific price the user is subscribing to. This value should correspond to the price's identifier in Stripe. -->
`newSubscription` 메서드의 첫 번째 인수는 구독의 내부 타입입니다. 애플리케이션이 단일 구독만 제공한다면, `default` 또는 `primary`라고 부를 수 있습니다. 이 구독 타입은 내부용으로만 사용하며 사용자에게 노출되지 않습니다. 공백이 없어야 하고, 구독 생성 이후에는 변경해서는 안 됩니다. 두 번째 인수는 사용자가 신청할 구독 가격이며, Stripe의 가격 식별자와 일치해야 합니다.

<!-- The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information. -->
`create` 메서드는 [a Stripe payment method identifier](#storing-payment-methods)나 Stripe `PaymentMethod` 객체를 받아 구독을 시작하고, Stripe 고객 ID 및 관련 결제 정보를 데이터베이스에 저장합니다.

> [!WARNING]
> 결제 수단 식별자를 바로 `create` 구독 메서드에 전달하면, 사용자의 저장된 결제 수단 목록에도 자동으로 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>

<!-- #### Collecting Recurring Payments via Invoice Emails -->
#### Collecting Recurring Payments via Invoice Emails

<!-- Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices: -->
고객의 반복 결제 금액을 자동으로 청구하지 않고, 매번 결제 예정일마다 Stripe가 인보이스 이메일을 보내도록 할 수도 있습니다. 이 경우, 고객은 인보이스 메일을 받은 후 직접 결제를 진행하게 됩니다. 인보이스 이메일로 반복 결제를 받을 때는 미리 결제 수단을 등록할 필요가 없습니다.

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

<!-- The amount of time a customer has to pay their invoice before their subscription is canceled is determined by the `days_until_due` option. By default, this is 30 days; however, you may provide a specific value for this option if you wish: -->
고객이 인보이스를 결제하지 않으면 구독이 취소됩니다. 결제 기한은 `days_until_due` 옵션으로 지정할 수 있으며, 기본값은 30일입니다. 필요하다면 다음과 같이 값을 지정하세요.

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>

<!-- #### Quantities -->
#### Quantities

<!-- If you would like to set a specific [quantity](https://stripe.com/docs/billing/subscriptions/quantities) for the price when creating the subscription, you should invoke the `quantity` method on the subscription builder before creating the subscription: -->
구독 생성 시 특정 [quantity](https://stripe.com/docs/billing/subscriptions/quantities)을 price에 지정하려면, 구독 빌더에서 `quantity` 메서드를 먼저 호출한 뒤 구독을 생성하면 됩니다.

```
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>

<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional [customer](https://stripe.com/docs/api/customers/create) or [subscription](https://stripe.com/docs/api/subscriptions/create) options supported by Stripe, you may do so by passing them as the second and third arguments to the `create` method: -->
Stripe에서 지원하는 [customer](https://stripe.com/docs/api/customers/create) 또는 [subscription](https://stripe.com/docs/api/subscriptions/create) 관련 추가 옵션을 사용할 경우, 해당 옵션을 `create` 메서드의 두 번째, 세 번째 인수로 전달할 수 있습니다.

```
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
구독을 생성할 때 쿠폰을 적용하고 싶다면, `withCoupon` 메서드를 사용하세요.

```
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

<!-- Or, if you would like to apply a [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes), you may use the `withPromotionCode` method: -->
또는, [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 적용하려면 `withPromotionCode` 메서드를 사용할 수 있습니다.

```
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

<!-- The given promotion code ID should be the Stripe API ID assigned to the promotion code and not the customer facing promotion code. If you need to find a promotion code ID based on a given customer facing promotion code, you may use the `findPromotionCode` method: -->
여기에서 전달하는 프로모션 코드 ID는 Stripe API에서 부여한 ID여야 하며, 고객에게 제공하는 코드가 아닙니다. 만약 고객에게 제공하는 코드로부터 Stripe의 프로모션 코드 ID를 찾고 싶다면 `findPromotionCode` 메서드를 사용할 수 있습니다.

```
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

<!-- In the example above, the returned `$promotionCode` object is an instance of `Laravel\Cashier\PromotionCode`. This class decorates an underlying `Stripe\PromotionCode` object. You can retrieve the coupon related to the promotion code by invoking the `coupon` method: -->
위 예시에서 반환된 `$promotionCode` 객체는 `Laravel\Cashier\PromotionCode` 인스턴스이며, 내부적으로 `Stripe\PromotionCode` 객체를 감쌉니다. 프로모션 코드에 연결된 쿠폰을 얻으려면 `coupon` 메서드를 호출할 수 있습니다.

```
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

<!-- The coupon instance allows you to determine the discount amount and whether the coupon represents a fixed discount or percentage based discount: -->
쿠폰 인스턴스를 통해 할인의 고정 금액 또는 비율 할인 여부, 할인 금액 등을 확인할 수 있습니다.

```
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

<!-- You can also retrieve the discounts that are currently applied to a customer or subscription: -->
또한, 현재 고객이나 구독에 적용된 할인 정보를 조회할 수도 있습니다.

```
$discount = $billable->discount();

$discount = $subscription->discount();
```

<!-- The returned `Laravel\Cashier\Discount` instances decorate an underlying `Stripe\Discount` object instance. You may retrieve the coupon related to this discount by invoking the `coupon` method: -->
반환되는 `Laravel\Cashier\Discount` 인스턴스는 내부적으로 `Stripe\Discount` 객체를 감쌉니다. 이 할인에 연결된 쿠폰은 역시 `coupon` 메서드로 얻을 수 있습니다.

```
$coupon = $subscription->discount()->coupon();
```

<!-- If you would like to apply a new coupon or promotion code to a customer or subscription, you may do so via the `applyCoupon` or `applyPromotionCode` methods: -->
고객이나 구독에 새 쿠폰 또는 프로모션 코드를 적용하고 싶다면, `applyCoupon` 또는 `applyPromotionCode` 메서드를 사용할 수 있습니다.

```
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

<!-- Remember, you should use the Stripe API ID assigned to the promotion code and not the customer facing promotion code. Only one coupon or promotion code can be applied to a customer or subscription at a given time. -->
참고로, 반드시 Stripe API에서 할당받은 프로모션 코드 ID를 사용해야 하며, 고객에게 제공되는 코드를 사용해서는 안 됩니다. 고객이나 구독에 한 번에 하나의 쿠폰 또는 프로모션 코드만 적용할 수 있습니다.

<!-- For more info on this subject, please consult the Stripe documentation regarding [coupons](https://stripe.com/docs/billing/subscriptions/coupons) and [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes). -->
자세한 내용은 Stripe의 [coupons](https://stripe.com/docs/billing/subscriptions/coupons) 및 [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes) 설명서를 참고하세요.

<a name="adding-subscriptions"></a>

<!-- #### Adding Subscriptions -->
#### Adding Subscriptions

<!-- If you would like to add a subscription to a customer who already has a default payment method you may invoke the `add` method on the subscription builder: -->
이미 기본 결제 수단이 등록된 고객에게 구독을 추가하려면, 구독 빌더의 `add` 메서드를 호출하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>

<!-- #### Creating Subscriptions From the Stripe Dashboard -->
#### Creating Subscriptions From the Stripe Dashboard

<!-- You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a type of `default`. To customize the subscription type that is assigned to dashboard created subscriptions, [define webhook event handlers](#defining-webhook-event-handlers). -->
Stripe 대시보드에서 직접 구독을 생성할 수도 있습니다. 이때, Cashier는 새로 추가된 구독을 동기화하며 구독 타입을 `default`로 지정합니다. 대시보드에서 생성된 구독에 부여할 타입을 변경하고 싶다면, [define webhook event handlers](#defining-webhook-event-handlers)하면 됩니다.

<!-- In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different types, only one type of subscription may be added through the Stripe dashboard. -->
또한, Stripe 대시보드에서는 한 종류의 구독만 생성할 수 있으며, 애플리케이션이 여러 개의 구독 타입을 제공한다면 대시보드에서는 한 번에 하나만 추가할 수 있습니다.

<!-- Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If a customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database. -->
항상 애플리케이션에서 제공하는 구독 타입별로 한 개의 활성 구독만 유지해야 합니다. 만약 한 고객이 `default` 타입 구독을 2개 가지고 있다면, Cashier에서는 두 구독을 모두 데이터베이스에 동기화하지만, 가장 최근에 추가된 구독만 사용하게 됩니다.

<a name="checking-subscription-status"></a>

<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the type of the subscription as its first argument: -->
고객이 애플리케이션에 구독하면, 다양한 편의 메서드를 사용해 구독 상태를 쉽게 확인할 수 있습니다. 먼저, `subscribed` 메서드는 고객이 활성화된 구독(체험 기간(trial) 포함)을 가지고 있으면 `true`를 반환합니다. `subscribed` 메서드의 첫 번째 인수로 구독 타입을 전달할 수 있습니다.

```
if ($user->subscribed('default')) {
    // ...
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/11.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` 메서드는 [route middleware](/docs/11.x/middleware)로도 활용할 수 있어, 사용자의 구독 여부에 따라 특정 라우트나 컨트롤러 접근을 제어할 수 있습니다.

```
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
사용자가 체험 기간(trial) 내에 있는지 확인하려면, `onTrial` 메서드를 사용할 수 있습니다. 예를 들어, 사용자가 아직 체험 기간일 때 경고 메시지를 표시하고 싶을 수 있습니다.

```
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

<!-- The `subscribedToProduct` method may be used to determine if the user is subscribed to a given product based on a given Stripe product's identifier. In Stripe, products are collections of prices. In this example, we will determine if the user's `default` subscription is actively subscribed to the application's "premium" product. The given Stripe product identifier should correspond to one of your product's identifiers in the Stripe dashboard: -->
`subscribedToProduct` 메서드는 사용자가 주어진 Stripe 상품 식별자에 해당하는 구독을 보유 중인지 확인할 때 사용합니다. Stripe에서는 상품(Product)이 여러 가격(Price)의 집합입니다. 아래 예시에서는 사용자의 `default` 구독이 애플리케이션의 "premium" 상품에 실제로 가입되어 있는지 확인합니다. 인수로 전달하는 Stripe 상품 식별자는 Stripe 대시보드의 상품 식별자와 일치해야 합니다.

```
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

<!-- By passing an array to the `subscribedToProduct` method, you may determine if the user's `default` subscription is actively subscribed to the application's "basic" or "premium" product: -->
`subscribedToProduct` 메서드에 배열을 전달하면, 사용자의 `default` 구독이 애플리케이션의 "basic" 또는 "premium" 상품에 가입되어 있는지 확인할 수 있습니다.

```
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

<!-- The `subscribedToPrice` method may be used to determine if a customer's subscription corresponds to a given price ID: -->
특정 가격 ID에 대한 구독 여부를 확인하려면, `subscribedToPrice` 메서드를 사용할 수 있습니다.

```
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
현재 구독이 활성화되어 있으며 체험 기간을 이미 지난 상태인지 확인하려면 `recurring` 메서드를 사용하세요.

```
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> 동일한 타입의 구독을 2개 가진 사용자의 경우, `subscription` 메서드는 항상 가장 최근의 구독만 반환합니다. 예를 들어, 사용자가 `default` 타입 구독 레코드를 2개 가지고 있다면, 한 개는 과거에 만료(d)된 구독이고, 나머지는 현재 활성 구독일 수 있습니다. 이 경우, 가장 최근에 생성된 구독만 반환되며, 이전 구독은 이력 관리 용도로 데이터베이스에 보관됩니다.

<a name="cancelled-subscription-status"></a>

<!-- #### Canceled Subscription Status -->
#### Canceled Subscription Status

<!-- To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method: -->
사용자가 한때 활성 구독자였다가 구독을 취소했는지 확인하려면 `canceled` 메서드를 사용할 수 있습니다.

```
if ($user->subscription('default')->canceled()) {
    // ...
}
```

<!-- You may also determine if a user has canceled their subscription but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
또한 사용자가 구독을 취소했지만 구독이 완전히 만료되기 전까지 "유예 기간(grace period)"에 있는지 확인할 수 있습니다. 예를 들어, 사용자가 3월 5일에 구독을 취소했는데, 원래 구독 만료일이 3월 10일이라면, 해당 사용자는 3월 10일까지 유예 기간에 머물게 됩니다. 이 기간 동안에는 `subscribed` 메서드가 여전히 `true`를 반환한다는 점에 유의하세요.

```
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

<!-- To determine if the user has canceled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
사용자가 구독을 취소했고 이제 "유예 기간"도 지나 완전히 종료된 상태인지 확인하려면 `ended` 메서드를 사용할 수 있습니다.

```
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>

<!-- #### Incomplete and Past Due Status -->
#### Incomplete and Past Due Status

<!-- If a subscription requires a secondary payment action after creation the subscription will be marked as `incomplete`. Subscription statuses are stored in the `stripe_status` column of Cashier's `subscriptions` database table. -->
구독 생성 후 추가 결제 절차가 필요한 경우, 해당 구독은 `incomplete` 상태로 표시됩니다. 구독 상태는 Cashier의 `subscriptions` 데이터베이스 테이블 내 `stripe_status` 컬럼에 저장됩니다.

<!-- Similarly, if a secondary payment action is required when swapping prices the subscription will be marked as `past_due`. When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Determining if a subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
가격을 변경(swap)할 때 또한 추가 결제 절차가 필요하다면 구독은 `past_due` 상태가 됩니다. 구독이 두 상태 중 하나에 있으면 고객이 결제를 완료(확인)하기 전까지는 활성화되지 않습니다. 구독에 미완료 결제가 있는지 확인하려면 billable 모델이나 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용하면 됩니다.

```
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

<!-- When a subscription has an incomplete payment, you should direct the user to Cashier's payment confirmation page, passing the `latestPayment` identifier. You may use the `latestPayment` method available on subscription instance to retrieve this identifier: -->
구독에 미완료 결제가 있을 경우, 사용자에게 Cashier의 결제 확인 페이지로 이동하도록 안내해야 하며, 이때 `latestPayment` 식별자를 전달하면 됩니다. 이 식별자는 구독 인스턴스의 `latestPayment` 메서드로 가져올 수 있습니다.

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

<!-- If you would like the subscription to still be considered active when it's in a `past_due` or `incomplete` state, you may use the `keepPastDueSubscriptionsActive` and `keepIncompleteSubscriptionsActive` methods provided by Cashier. Typically, these methods should be called in the `register` method of your `App\Providers\AppServiceProvider`: -->
구독이 `past_due` 또는 `incomplete` 상태여도 구독을 활성 상태로 간주하고 싶다면, Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 및 `keepIncompleteSubscriptionsActive` 메서드를 사용할 수 있습니다. 이 메서드는 일반적으로 `App\Providers\AppServiceProvider`의 `register` 메서드에서 호출하는 것이 좋습니다.

```
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
> 구독이 `incomplete` 상태에 있을 때는 결제가 확정될 때까지 구독을 변경할 수 없습니다. 따라서 `swap` 및 `updateQuantity` 메서드는 구독이 `incomplete` 상태일 때 예외를 발생시킵니다.

<a name="subscription-scopes"></a>

<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
대부분의 구독 상태는 쿼리 스코프로도 제공되어, 특정 상태에 있는 구독을 데이터베이스에서 쉽게 조회할 수 있습니다.

```
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

<!-- A complete list of available scopes is available below: -->
아래는 사용 가능한 모든 스코프의 예시입니다.

```
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
고객이 애플리케이션에 구독한 이후, 가끔 더 나은 구독 가격으로 변경하고 싶어질 수 있습니다. Stripe 가격 식별자를 `swap` 메서드에 전달하면 사용자의 구독을 새 가격으로 교체할 수 있습니다. 가격을 교체할 때 사용자가 이전에 구독을 취소했어도 구독이 재활성화된다고 간주합니다. 이때 전달하는 식별자는 Stripe 대시보드에 등록된 가격의 식별자여야 합니다.

```
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

<!-- If the customer is on trial, the trial period will be maintained. Additionally, if a "quantity" exists for the subscription, that quantity will also be maintained. -->
고객이 체험(트라이얼) 중이라면 해당 기간이 그대로 유지됩니다. 또한 구독에 "수량(quantity)" 값이 있다면 그 값도 유지됩니다.

<!-- If you would like to swap prices and cancel any trial period the customer is currently on, you may invoke the `skipTrial` method: -->
현재 체험을 취소하고 가격만 교체하고 싶을 때는 `skipTrial` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

<!-- If you would like to swap prices and immediately invoice the customer instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
가격을 교체하면서 다음 결제 주기를 기다리지 않고 즉시 결제 인보이스를 발행하고 싶다면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>

<!-- #### Prorations -->
#### Prorations

<!-- By default, Stripe prorates charges when swapping between prices. The `noProrate` method may be used to update the subscription's price without prorating the charges: -->
기본적으로 Stripe는 가격을 변경(swap)할 때 금액을 기간에 맞춰 분할 청구(prorate)합니다. 분할 청구 없이 구독 가격만 갱신하고 싶다면 `noProrate` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->noProrate()->swap('price_yearly');
```

<!-- For more information on subscription proration, consult the [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations). -->
구독의 분할 청구에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations)를 참고하세요.

> [!WARNING]
> `swapAndInvoice` 메서드 전에 `noProrate` 메서드를 호출해도 분할 청구에는 영향이 없습니다. 이 경우 항상 인보이스가 발행됩니다.

<a name="subscription-quantity"></a>

<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. You may use the `incrementQuantity` and `decrementQuantity` methods to easily increment or decrement your subscription quantity: -->
구독이 "수량"에 따라 차등 적용되는 경우도 있습니다. 예를 들어, 프로젝트 관리 애플리케이션이 프로젝트 당 월 $10씩 청구한다면, 구독 수량은 프로젝트 수를 의미할 수 있습니다. `incrementQuantity`와 `decrementQuantity` 메서드를 사용하면 구독 수량을 손쉽게 늘리거나 줄일 수 있습니다.

```
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
또는 `updateQuantity` 메서드로 수량을 특정 값으로 직접 설정할 수 있습니다.

```
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
분할 청구 없이 구독 수량을 갱신하려면 `noProrate` 메서드를 함께 사용합니다.

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<!-- For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities). -->
구독 수량에 대한 더 자세한 내용은 [Stripe documentation](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>

<!-- #### Quantities for Subscriptions With Multiple Products -->
#### Quantities for Subscriptions With Multiple Products

<!-- If your subscription is a [subscription with multiple products](#subscriptions-with-multiple-products), you should pass the ID of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods: -->
[subscription with multiple products](#subscriptions-with-multiple-products)일 경우, 인크리먼트(증가)/디크리먼트(감소) 메서드의 두 번째 인수로 수량을 조정할 가격의 ID를 전달해야 합니다.

```
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>

<!-- ### Subscriptions With Multiple Products -->
### Subscriptions With Multiple Products

<!-- [Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products) allow you to assign multiple billing products to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on product for an additional $15 per month. Information for subscriptions with multiple products is stored in Cashier's `subscription_items` database table. -->
[Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products)은 하나의 구독에 여러 개의 과금 상품을 할당할 수 있습니다. 예를 들어, 고객 지원 "헬프데스크" 애플리케이션에 월 $10짜리 기본 구독이 있고, 여기에 월 $15짜리 라이브 챗 추가 상품이 있다면, 이렇게 여러 상품을 하나의 구독에 연결할 수 있습니다. 복수 상품 구독에 대한 정보는 Cashier의 `subscription_items` 데이터베이스 테이블에 저장됩니다.

<!-- You may specify multiple products for a given subscription by passing an array of prices as the second argument to the `newSubscription` method: -->
`newSubscription` 메서드의 두 번째 매개변수로 가격 배열을 전달하여 여러 상품을 설정할 수 있습니다.

```
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
위 예시와 같이 실행하면 사용자의 `default` 구독에는 두 개의 가격이 연결되고, 각 가격마다 개별 청구 주기에 따라 과금됩니다. 필요하다면 `quantity` 메서드를 이용해 특정 가격에만 개별 수량을 지정할 수도 있습니다.

```
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

<!-- If you would like to add another price to an existing subscription, you may invoke the subscription's `addPrice` method: -->
기존 구독에 추가 가격을 추가하고 싶다면, 구독 인스턴스의 `addPrice` 메서드를 호출하세요.

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

<!-- The example above will add the new price and the customer will be billed for it on their next billing cycle. If you would like to bill the customer immediately you may use the `addPriceAndInvoice` method: -->
위 예시에서는 새 가격이 추가되며, 다음 결제 주기에서 과금됩니다. 즉시 결제를 원할 경우에는 `addPriceAndInvoice` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

<!-- If you would like to add a price with a specific quantity, you can pass the quantity as the second argument of the `addPrice` or `addPriceAndInvoice` methods: -->
특정 가격에 대한 수량을 지정하며 추가하려면, `addPrice` 또는 `addPriceAndInvoice` 메서드의 두 번째 인수로 수량 값을 전달하면 됩니다.

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

<!-- You may remove prices from subscriptions using the `removePrice` method: -->
구독에서 가격을 제거할 때는 `removePrice` 메서드를 사용하세요.

```
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> 구독에 마지막으로 남은 가격은 제거할 수 없습니다. 이 경우 구독 전체를 취소해야 합니다.

<a name="swapping-prices"></a>

<!-- #### Swapping Prices -->
#### Swapping Prices

<!-- You may also change the prices attached to a subscription with multiple products. For example, imagine a customer has a `price_basic` subscription with a `price_chat` add-on product and you want to upgrade the customer from the `price_basic` to the `price_pro` price: -->
복수 상품이 연결된 구독이라면, 구독에 연결된 가격 배열도 변경할 수 있습니다. 예를 들어, 고객이 `price_basic` 구독과 `price_chat` 부가 상품을 가지고 있는데, `price_basic`을 `price_pro`로 업그레이드하려면 아래와 같이 합니다.

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

<!-- When executing the example above, the underlying subscription item with the `price_basic` is deleted and the one with the `price_chat` is preserved. Additionally, a new subscription item for the `price_pro` is created. -->
위 예시를 실행하면 기존의 `price_basic` 구독 항목이 삭제되고 `price_chat`은 그대로 유지되며, 새롭게 `price_pro` 항목이 추가됩니다.

<!-- You can also specify subscription item options by passing an array of key / value pairs to the `swap` method. For example, you may need to specify the subscription price quantities: -->
각 구독 항목마다 개별 옵션(예: 수량)을 지정하고 싶다면, `swap` 메서드에 키-값 쌍 배열을 전달할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

<!-- If you want to swap a single price on a subscription, you may do so using the `swap` method on the subscription item itself. This approach is particularly useful if you would like to preserve all of the existing metadata on the subscription's other prices: -->
한 구독 내에서 특정 가격 하나만 교체하고 싶다면 해당 구독 항목에서 `swap` 메서드를 직접 호출할 수도 있습니다. 이 방식은 기존 구독 가격에 설정된 메타데이터를 모두 유지하고자 할 때 특히 유용합니다.

```
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>

<!-- #### Proration -->
#### Proration

<!-- By default, Stripe will prorate charges when adding or removing prices from a subscription with multiple products. If you would like to make a price adjustment without proration, you should chain the `noProrate` method onto your price operation: -->
기본적으로 Stripe는 복수 상품 구독에서 가격을 추가하거나 제거할 때 금액을 기간별로 분할 청구합니다. 분할 청구 없이 가격을 조정하려면 가격 관련 작업에 `noProrate` 메서드를 체이닝하면 됩니다.

```
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>

<!-- #### Quantities -->
#### Quantities

<!-- If you would like to update quantities on individual subscription prices, you may do so using the [existing quantity methods](#subscription-quantity) by passing the ID of the price as an additional argument to the method: -->
특정 구독 가격의 수량을 변경하려면, [existing quantity methods](#subscription-quantity)에서 가격 ID를 추가 인수로 전달하면 됩니다.

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 구독에 복수의 가격이 설정된 경우, `Subscription` 모델의 `stripe_price` 및 `quantity` 속성은 `null`이 됩니다. 각 가격별 속성에 접근하려면 `Subscription` 모델의 `items` 연관관계를 사용해야 합니다.

<a name="subscription-items"></a>

<!-- #### Subscription Items -->
#### Subscription Items

<!-- When a subscription has multiple prices, it will have multiple subscription "items" stored in your database's `subscription_items` table. You may access these via the `items` relationship on the subscription: -->
구독에 여러 가격이 연결되어 있으면, 데이터베이스의 `subscription_items` 테이블에 여러 개의 구독 "항목(item)"이 저장됩니다. 구독의 `items` 연관관계를 통해 각 항목에 접근할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

<!-- You can also retrieve a specific price using the `findItemOrFail` method: -->
특정 가격에 해당하는 구독 항목을 조회할 때는 `findItemOrFail` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>

<!-- ### Multiple Subscriptions -->
### Multiple Subscriptions

<!-- Stripe allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans. -->
Stripe는 한 고객이 여러 구독을 동시에 보유하는 것도 지원합니다. 예를 들어, 체육관 서비스에서 수영 구독과 웨이트 트레이닝 구독을 각각 별도로 갖고, 각 구독마다 다른 가격이 적용될 수 있습니다. 물론 고객은 둘 중 하나 혹은 모두에 가입할 수 있습니다.

<!-- When your application creates subscriptions, you may provide the type of the subscription to the `newSubscription` method. The type may be any string that represents the type of subscription the user is initiating: -->
애플리케이션에서 구독을 생성할 때 `newSubscription` 메서드에 구독의 유형(type)을 전달할 수 있습니다. 이 type 값은 사용자가 시작하는 구독을 구분해줄 수 있는 아무 문자열이나 사용할 수 있습니다.

```
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- In this example, we initiated a monthly swimming subscription for the customer. However, they may want to swap to a yearly subscription at a later time. When adjusting the customer's subscription, we can simply swap the price on the `swimming` subscription: -->
위 예시에서는 고객이 월간 수영 구독을 시작합니다. 이후 연간 구독으로 전환하고 싶을 수 있는데, 고객의 구독을 조정할 때는 `swimming` 구독의 가격만 교체하면 됩니다.

```
$user->subscription('swimming')->swap('price_swimming_yearly');
```

<!-- Of course, you may also cancel the subscription entirely: -->
물론, 구독 전체를 취소할 수도 있습니다.

```
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>

<!-- ### Usage Based Billing -->
### Usage Based Billing

<!-- [Usage based billing](https://stripe.com/docs/billing/subscriptions/metered-billing) allows you to charge customers based on their product usage during a billing cycle. For example, you may charge customers based on the number of text messages or emails they send per month. -->
[Usage based billing](https://stripe.com/docs/billing/subscriptions/metered-billing)를 활용하면 고객의 상품 사용량에 따라 매 결제 주기마다 비용을 청구할 수 있습니다. 예를 들어, 매월 보낸 문자 또는 이메일 건수에 따라 고객에게 비용을 청구할 수 있습니다.

<!-- To start using usage billing, you will first need to create a new product in your Stripe dashboard with a [usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) and a [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter). After creating the meter, store the associated event name and meter ID, which you will need to report and retrieve usage. Then, use the `meteredPrice` method to add the metered price ID to a customer subscription: -->
사용량 기반 청구를 시작하려면, Stripe 대시보드에서 [usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide)과 [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter)가 적용된 새 상품을 생성하세요. Meter를 만든 뒤에는 연동에 필요한 이벤트 이름과 meter ID를 저장해 두세요. 그 다음, `meteredPrice` 메서드로 고객 구독에 해당 metered 가격 ID를 추가하면 됩니다.

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- You may also start a metered subscription via [Stripe Checkout](#checkout): -->
또는 [Stripe Checkout](#checkout)을 통해서도 사용량 기반 구독을 시작할 수 있습니다.

```
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
고객이 애플리케이션을 사용할 때마다 Stripe에 사용량을 보고하여, 올바른 비용이 청구될 수 있도록 해야 합니다. 사용량을 보고하려면, `Billable` 모델에서 `reportMeterEvent` 메서드를 사용하세요.

```
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

<!-- By default, a "usage quantity" of 1 is added to the billing period. Alternatively, you may pass a specific amount of "usage" to add to the customer's usage for the billing period: -->
기본적으로 "사용량 수량(usage quantity)" 1이 해당 청구 주기에 추가됩니다. 또는, 한 번에 특정 사용량만큼 추가하고 싶다면 두 번째 인수로 사용량을 전달하세요.

```
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

<!-- To retrieve a customer's event summary for a meter, you may use a `Billable` instance's `meterEventSummaries` method: -->
특정 meter에 대한 고객의 이벤트 요약을 조회하려면 `Billable` 인스턴스의 `meterEventSummaries` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

<!-- Please refer to Stripe's [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object) for more information on meter event summaries. -->
meter 이벤트 요약에 대한 더 자세한 정보는 Stripe [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object)를 참고하세요.

<!-- To [list all meters](https://docs.stripe.com/api/billing/meter/list), you may use a `Billable` instance's `meters` method: -->
[list all meters](https://docs.stripe.com/api/billing/meter/list)하려면 `Billable` 인스턴스의 `meters` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>

<!-- ### Subscription Taxes -->
### Subscription Taxes

> [!WARNING]
> 세율(Tax Rate)을 직접 계산하는 대신, [automatically calculate taxes using Stripe Tax](#tax-configuration)을 사용할 수 있습니다.

<!-- To specify the tax rates a user pays on a subscription, you should implement the `taxRates` method on your billable model and return an array containing the Stripe tax rate IDs. You can define these tax rates in [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates): -->
구독에 적용할 세율을 지정하려면 billable 모델에 `taxRates` 메서드를 구현하고, Stripe 세율 ID가 담긴 배열을 반환하세요. 해당 세율은 [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates)에서 미리 생성할 수 있습니다.

```
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
`taxRates` 메서드를 활용하면 개별 고객별로 다른 세율을 적용할 수 있습니다. 고객별로 국가별 세율 등을 다르게 적용해야 할 때 유용합니다.

<!-- If you're offering subscriptions with multiple products, you may define different tax rates for each price by implementing a `priceTaxRates` method on your billable model: -->
복수 상품 구독을 제공하는 경우, 각 가격 별로 별도의 세율을 부여하고 싶다면 billable 모델에서 `priceTaxRates` 메서드를 구현하세요.

```
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
> `taxRates` 메서드는 구독요금에만 적용됩니다. Cashier를 사용해 단건(one-off) 결제를 진행할 경우, 결제 시점에 수동으로 세율을 지정해야 합니다.

<a name="syncing-tax-rates"></a>

<!-- #### Syncing Tax Rates -->
#### Syncing Tax Rates

<!-- When changing the hard-coded tax rate IDs returned by the `taxRates` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the new `taxRates` values, you should call the `syncTaxRates` method on the user's subscription instance: -->
`taxRates` 메서드에서 반환하는 세율 ID를 변경해도 기존 구독의 세율 설정은 그대로 유지됩니다. 기존 구독에 대해 새로운 `taxRates` 값으로 갱신하려면, 사용자 구독 인스턴스에서 `syncTaxRates` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->syncTaxRates();
```

<!-- This will also sync any item tax rates for a subscription with multiple products. If your application is offering subscriptions with multiple products, you should ensure that your billable model implements the `priceTaxRates` method [discussed above](#subscription-taxes). -->
이 작업은 복수 상품 구독의 각 항목(item) 세율도 함께 동기화합니다. 복수 상품 구독을 제공하는 경우, [discussed above](#subscription-taxes) `priceTaxRates` 메서드 구현을 반드시 확인하세요.

<a name="tax-exemption"></a>

<!-- #### Tax Exemption -->
#### Tax Exemption

<!-- Cashier also offers the `isNotTaxExempt`, `isTaxExempt`, and `reverseChargeApplies` methods to determine if the customer is tax exempt. These methods will call the Stripe API to determine a customer's tax exemption status: -->
Cashier에서는 고객이 세금 면제 대상인지 확인하는 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드도 제공합니다. 이 메서드들은 Stripe API를 호출하여 고객의 세금 면제 여부를 판단합니다.

```
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]
> 이 메서드들은 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있습니다. 단, `Invoice` 객체에서 호출할 경우, 인보이스 발행 시점의 면제 상태를 기준으로 결과를 반환합니다.

<a name="subscription-anchor-date"></a>

<!-- ### Subscription Anchor Date -->
### Subscription Anchor Date

<!-- By default, the billing cycle anchor is the date the subscription was created or, if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method: -->
기본적으로 청구 주기의 기준(anchor)은 구독이 생성된 날짜(체험 기간이 있다면 체험 종료일)입니다. 이 기준일을 바꾸고 싶다면 `anchorBillingCycleOn` 메서드를 사용할 수 있습니다.

```
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
구독 청구 주기 관리에 대한 자세한 내용은 [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>

<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
구독을 취소하려면, 사용자의 구독 인스턴스에서 `cancel` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->cancel();
```

<!-- When a subscription is canceled, Cashier will automatically set the `ends_at` column in your `subscriptions` database table. This column is used to know when the `subscribed` method should begin returning `false`. -->
구독이 취소되면 Cashier는 자동으로 `subscriptions` 테이블의 `ends_at` 컬럼 값을 설정합니다. 이 값은 `subscribed` 메서드가 언제부터 `false`를 반환해야 하는지 판단하는 데 사용됩니다.

<!-- For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
예를 들어, 3월 1일에 사용자가 구독을 취소했지만, 실제 만료 예정일이 3월 5일이라면, `subscribed` 메서드는 3월 5일까지 계속 `true`를 반환하게 됩니다. 즉, 보통 고객이 결제 주기 마지막 날까지는 계속 애플리케이션을 이용할 수 있도록 처리됩니다.

<!-- You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
구독이 취소됐지만 여전히 유예 기간에 있는지 확인하려면 `onGracePeriod` 메서드를 사용하세요.

```
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

<!-- If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription: -->
즉시 구독을 취소하고 싶다면, 해당 구독에서 `cancelNow` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->cancelNow();
```

<!-- If you wish to cancel a subscription immediately and invoice any remaining un-invoiced metered usage or new / pending proration invoice items, call the `cancelNowAndInvoice` method on the user's subscription: -->
현재 미청구된 사용량 또는 남아 있는 프레이션 항목(proration invoice item)에 대해 즉시 인보이스 발행까지 함께 처리하려면 `cancelNowAndInvoice` 메서드를 사용하세요.

```
$user->subscription('default')->cancelNowAndInvoice();
```

<!-- You may also choose to cancel the subscription at a specific moment in time: -->
특정 시점에 구독이 취소되도록 예약할 수도 있습니다.

```
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

<!-- Finally, you should always cancel user subscriptions before deleting the associated user model: -->
마지막으로, 관련 사용자 모델을 삭제하기 전에 반드시 해당 사용자의 구독도 함께 취소해야 합니다.

```
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>

<!-- ### Resuming Subscriptions -->
### Resuming Subscriptions

<!-- If a customer has canceled their subscription and you wish to resume it, you may invoke the `resume` method on the subscription. The customer must still be within their "grace period" in order to resume a subscription: -->
고객이 구독을 취소했다가 다시 재개하고 싶을 때는 해당 구독 인스턴스에서 `resume` 메서드를 호출하면 됩니다. 단, 구독을 재개하려면 고객이 아직 "유예 기간(grace period)" 내에 있어야 합니다.

```
$user->subscription('default')->resume();
```

<!-- If the customer cancels a subscription and then resumes that subscription before the subscription has fully expired the customer will not be billed immediately. Instead, their subscription will be re-activated and they will be billed on the original billing cycle. -->
고객이 구독을 취소한 후, 해당 구독이 완전히 만료되기 전에 다시 재개하면 고객은 즉시 결제되지 않습니다. 대신, 구독이 다시 활성화되고 원래 청구 주기에 따라 결제됩니다.

<a name="subscription-trials"></a>

<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>

<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions: -->
고객의 결제 정보를 미리 받아두고 체험 기간을 제공하고 싶다면, 구독을 생성할 때 `trialDays` 메서드를 사용하면 됩니다.

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- This method will set the trial period ending date on the subscription record within the database and instruct Stripe to not begin billing the customer until after this date. When using the `trialDays` method, Cashier will overwrite any default trial period configured for the price in Stripe. -->
이 메서드는 구독 레코드의 데이터베이스에 체험 기간 종료일을 지정하고, Stripe에 지정된 날짜 이후부터 청구를 시작하라고 지시합니다. `trialDays` 메서드를 사용하면, Cashier가 Stripe의 가격(Price)에 기본 설정된 체험 기간 값은 무시합니다.

> [!WARNING]
> 만약 고객이 체험 기간 종료 전에 구독을 취소하지 않으면, 체험이 끝나는 즉시 청구가 발생합니다. 체험 종료일을 반드시 사용자에게 안내해 주시기 바랍니다.

<!-- The `trialUntil` method allows you to provide a `DateTime` instance that specifies when the trial period should end: -->
`trialUntil` 메서드를 사용하면 체험 기간이 끝나는 시점을 직접 `DateTime` 인스턴스로 지정할 수 있습니다.

```
use Carbon\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->addDays(10))
    ->create($paymentMethod);
```

<!-- You may determine if a user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
사용자가 현재 체험 기간 내에 있는지 확인하려면, 사용자 인스턴스의 `onTrial` 메서드 또는 구독 인스턴스의 `onTrial` 메서드를 사용할 수 있습니다. 아래 두 예시는 동일하게 동작합니다.

```
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

<!-- You may use the `endTrial` method to immediately end a subscription trial: -->
`endTrial` 메서드를 사용하면 구독 체험 기간을 즉시 종료할 수도 있습니다.

```
$user->subscription('default')->endTrial();
```

<!-- To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods: -->
기존 체험 기간이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용할 수 있습니다.

```
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
Stripe 대시보드에서 가격(Price)별로 체험 일수를 지정하거나, Cashier를 통해 체험 일수를 명시적으로 전달할 수 있습니다. Stripe에서 가격의 체험 일수를 정의한 경우, 과거에 구독 이력이 있었던 고객을 포함한 모든 신규 구독에 대해 항상 체험 기간이 부여됩니다. 단, `skipTrial()` 메서드를 명시적으로 호출하면 체험 기간 없이 바로 가입할 수 있습니다.

<a name="without-payment-method-up-front"></a>

<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration: -->
사용자로부터 결제 정보를 미리 받지 않고도 체험 기간을 제공하고 싶다면, 사용자 레코드의 `trial_ends_at` 컬럼에 원하는 체험 기간 종료일을 설정하면 됩니다. 일반적으로 회원 가입 시 아래와 같이 처리합니다.

```
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!WARNING]
> 반드시 청구 관련 모델 클래스에서 `trial_ends_at` 속성(attribute)에 대해 [date cast](/docs/11.x/eloquent-mutators#date-casting)를 추가해야 합니다.

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the billable model instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
Cashier에서는 이러한 유형의 체험 기간을 "일반(Generic) 체험"이라고 부릅니다. 이는 실제 구독에 연결되지 않은 체험 기간이기 때문입니다. 청구가 가능한 모델 인스턴스에서 `onTrial` 메서드를 호출하면, 현재 날짜가 `trial_ends_at` 값 이전이라면 `true`를 반환합니다.

```
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
이후 실제 구독을 생성할 준비가 되면, 평소처럼 `newSubscription` 메서드를 사용하시면 됩니다.

```
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription type parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
사용자의 체험 기간 종료일을 확인하려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 체험 기간 중이라면 Carbon 날짜 인스턴스를 반환하고, 그렇지 않을 경우 `null`을 반환합니다. 기본 구독 외에 특정 구독의 체험 종료일을 확인하려면 선택적으로 인자를 전달할 수도 있습니다.

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not yet created an actual subscription: -->
또한, 사용자가 실제 구독을 생성하기 전 "일반(Generic) 체험" 기간 내에 있는지 명확하게 알고 싶다면 `onGenericTrial` 메서드를 사용할 수 있습니다.

```
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>

<!-- ### Extending Trials -->
### Extending Trials

<!-- The `extendTrial` method allows you to extend the trial period of a subscription after the subscription has been created. If the trial has already expired and the customer is already being billed for the subscription, you can still offer them an extended trial. The time spent within the trial period will be deducted from the customer's next invoice: -->
`extendTrial` 메서드를 사용하면, 구독을 생성한 후에도 체험 기간을 연장할 수 있습니다. 이미 체험이 만료되어 고객이 청구를 받는 상태라도 추가 체험을 제공할 수 있습니다. 체험 기간에 추가로 머문 만큼, 다음 청구서에서 해당 일 수만큼 차감됩니다.

```
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// End the trial 7 days from now...
$subscription->extendTrial(
    now()->addDays(7)
);

// Add an additional 5 days to the trial...
$subscription->extendTrial(
    $subscription->trial_ends_at->addDays(5)
);
```

<a name="handling-stripe-webhooks"></a>

<!-- ## Handling Stripe Webhooks -->
## Handling Stripe Webhooks

> [!NOTE]
> 로컬 개발 환경에서 웹훅 테스트를 돕기 위해 [the Stripe CLI](https://stripe.com/docs/stripe-cli)를 사용할 수 있습니다.

<!-- Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Stripe는 웹훅(Webhook)을 통해 다양한 이벤트를 애플리케이션에 알릴 수 있습니다. 기본적으로, Cashier 서비스 프로바이더가 Cashier의 웹훅 컨트롤러로 연결되는 라우트를 자동으로 등록합니다. 이 컨트롤러가 모든 웹훅 요청을 처리하게 됩니다.

<!-- By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like. -->
Cashier 웹훅 컨트롤러는 기본적으로 Stripe 설정에서 지정된 실패 결제가 너무 많을 때 구독을 취소하는 것, 고객 정보 업데이트, 고객 삭제, 구독 업데이트, 결제 수단 변경 등 여러 일반적인 Stripe 웹훅 이벤트를 자동으로 처리합니다. 하지만 곧 자세히 설명하겠지만, 이 컨트롤러를 확장해 원하는 Stripe 웹훅 이벤트를 직접 처리할 수도 있습니다.

<!-- To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are: -->
애플리케이션이 Stripe 웹훅을 정상적으로 처리할 수 있도록, Stripe 관리자 패널에서 웹훅 URL을 반드시 설정해야 합니다. Cashier 웹훅 컨트롤러는 기본적으로 `/stripe/webhook` 경로에서 요청을 받습니다. Stripe 관리 패널에서 반드시 활성화해야 하는 전체 웹훅 목록은 아래와 같습니다.

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
편의를 위해, Cashier는 `cashier:webhook` Artisan 명령어를 제공합니다. 이 명령어는 Cashier가 요구하는 이벤트를 모두 리슨하는 Stripe 웹훅을 생성해줍니다.

```shell
php artisan cashier:webhook
```

<!-- By default, the created webhook will point to the URL defined by the `APP_URL` environment variable and the `cashier.webhook` route that is included with Cashier. You may provide the `--url` option when invoking the command if you would like to use a different URL: -->
기본적으로 생성된 웹훅은 `APP_URL` 환경 변수와 Cashier에 포함된 `cashier.webhook` 라우트가 지정된 URL로 연결됩니다. 다른 URL을 사용하고 싶다면 명령어 실행 시 `--url` 옵션을 사용할 수 있습니다.

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

<!-- The webhook that is created will use the Stripe API version that your version of Cashier is compatible with. If you would like to use a different Stripe version, you may provide the `--api-version` option: -->
생성되는 웹훅은 현재 Cashier 버전과 호환되는 Stripe API 버전을 사용합니다. 만약 다른 Stripe 버전을 사용하고 싶다면, `--api-version` 옵션을 지정할 수 있습니다.

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

<!-- After creation, the webhook will be immediately active. If you wish to create the webhook but have it disabled until you're ready, you may provide the `--disabled` option when invoking the command: -->
이렇게 생성된 웹훅은 즉시 활성화됩니다. 만약 생성은 하되 준비될 때까지 비활성화 상태로 두고 싶다면, `--disabled` 옵션을 추가하면 됩니다.

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Stripe에서 보내는 웹훅 요청이 Cashier에 포함된 [webhook signature verification](#verifying-webhook-signatures) 미들웨어로 보호되고 있는지 반드시 확인하십시오.

<a name="webhooks-csrf-protection"></a>

<!-- #### Webhooks and CSRF Protection -->
#### Webhooks and CSRF Protection

<!-- Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/11.x/csrf), you should ensure that Laravel does not attempt to validate the CSRF token for incoming Stripe webhooks. To accomplish this, you should exclude `stripe/*` from CSRF protection in your application's `bootstrap/app.php` file: -->
Stripe 웹훅 요청은 Laravel의 [CSRF protection](/docs/11.x/csrf)를 우회해야 하므로, 해당 웹훅에 대해서는 CSRF 토큰 검증을 수행하지 않도록 설정해야 합니다. 이를 위해 애플리케이션의 `bootstrap/app.php` 파일에서 `stripe/*` 경로를 CSRF 보호에서 제외하십시오.

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>

<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancellations for failed charges and other common Stripe webhook events. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier는 결제 실패로 인한 구독 취소, 기타 일부 일반적인 Stripe 웹훅 이벤트를 자동으로 처리합니다. 하지만 추가로 처리하고 싶은 웹훅 이벤트가 있다면, Cashier가 발생시키는 아래와 같은 이벤트를 리슨해서 직접 처리할 수 있습니다.

<!--
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`
-->
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

<!-- Both events contain the full payload of the Stripe webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/11.x/events#defining-listeners) that will handle the event: -->
이 두 이벤트는 Stripe 웹훅의 전체 페이로드(payload)를 포함합니다. 예를 들어, `invoice.payment_succeeded` 웹훅을 처리하려면 다음과 같이 [listener](/docs/11.x/events#defining-listeners)를 등록할 수 있습니다.

```
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
웹훅의 보안을 위해 [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures)을 사용할 수 있습니다. Cashier는 Stripe 웹훅 요청의 유효성을 자동으로 검증해 주는 미들웨어를 기본 포함합니다.

<!-- To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is set in your application's `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard. -->
웹훅 검증을 활성화하려면, 애플리케이션의 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경 변수를 반드시 설정해야 합니다. Stripe 관리자 대시보드에서 웹훅 `secret` 값을 확인할 수 있습니다.

<a name="single-charges"></a>

<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>

<!-- ### Simple Charge -->
### Simple Charge

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance. You will need to [provide a payment method identifier](#payment-methods-for-single-charges) as the second argument to the `charge` method: -->
고객에게 단 한 번만 결제(일시불 결제)를 진행하고 싶을 때는, 청구가 가능한 모델 인스턴스에서 `charge` 메서드를 사용하세요. 이때 [provide a payment method identifier](#payment-methods-for-single-charges)를 `charge` 메서드의 두 번째 인수로 전달해야 합니다.

```
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

<!-- The `charge` method accepts an array as its third argument, allowing you to pass any options you wish to the underlying Stripe charge creation. More information regarding the options available to you when creating charges may be found in the [Stripe documentation](https://stripe.com/docs/api/charges/create): -->
`charge` 메서드는 세 번째 인수로 배열을 받을 수 있습니다. 이 배열을 통해 Stripe 결제 생성 시 다양한 옵션을 지정할 수 있습니다. 사용 가능한 옵션에 대한 자세한 정보는 [Stripe documentation](https://stripe.com/docs/api/charges/create)에서 확인하세요.

```
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

<!-- You may also use the `charge` method without an underlying customer or user. To accomplish this, invoke the `charge` method on a new instance of your application's billable model: -->
사용자나 고객이 생성된 상태가 아니어도 `charge` 메서드를 사용할 수 있습니다. 해당 모델의 새 인스턴스에서 `charge` 메서드를 호출하면 됩니다.

```
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

<!-- The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method: -->
만약 결제에 실패하면 `charge` 메서드는 예외를 발생시킵니다. 결제가 성공하면, `Laravel\Cashier\Payment` 인스턴스를 반환합니다.

```
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]
> `charge` 메서드는 결제 금액을 해당 통화의 최소 단위(최소 분할 단위)로 입력받습니다. 예를 들어 미국 달러(USD)로 결제한다면 금액은 "센트" 단위로 전달해야 합니다.

<a name="charge-with-invoice"></a>

<!-- ### Charge With Invoice -->
### Charge With Invoice

<!-- Sometimes you may need to make a one-time charge and offer a PDF invoice to your customer. The `invoicePrice` method lets you do just that. For example, let's invoice a customer for five new shirts: -->
고객에게 일회성 결제를 하면서 동시에 PDF 청구서를 제공하고 싶을 때는, `invoicePrice` 메서드를 사용할 수 있습니다. 예를 들어, 티셔츠 5벌에 대한 청구서를 생성하려면 아래와 같이 작성합니다.

```
$user->invoicePrice('price_tshirt', 5);
```

<!-- The invoice will be immediately charged against the user's default payment method. The `invoicePrice` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array which should contain the billing options for the invoice itself: -->
이 청구서는 즉시 사용자의 기본 결제 수단으로 결제됩니다. `invoicePrice` 메서드는 세 번째 인수로 옵션 설정을 위한 배열도 받을 수 있습니다. 이 배열에는 청구 항목(item)에 대한 결제 옵션을 넣으며, 네 번째 인수 역시 배열로 전달하여 실제 청구서(invoice) 자체에 대한 결제 옵션을 추가할 수 있습니다.

```
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

<!-- Similarly to `invoicePrice`, you may use the `tabPrice` method to create a one-time charge for multiple items (up to 250 items per invoice) by adding them to the customer's "tab" and then invoicing the customer. For example, we may invoice a customer for five shirts and two mugs: -->
`invoicePrice`와 비슷하게, `tabPrice` 메서드를 사용하면 여러 항목(인보이스당 최대 250개)을 고객의 "탭(tab)"에 추가한 뒤 한 번에 청구하는 일회성 결제를 만들 수 있습니다. 예를 들어, 티셔츠 5개와 머그컵 2개를 한꺼번에 청구할 수 있습니다.

```
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

<!-- Alternatively, you may use the `invoiceFor` method to make a "one-off" charge against the customer's default payment method: -->
또는, `invoiceFor` 메서드를 사용하여 고객의 기본 결제 수단으로 "일회성" 결제를 할 수도 있습니다.

```
$user->invoiceFor('One Time Fee', 500);
```

<!-- Although the `invoiceFor` method is available for you to use, it is recommended that you use the `invoicePrice` and `tabPrice` methods with pre-defined prices. By doing so, you will have access to better analytics and data within your Stripe dashboard regarding your sales on a per-product basis. -->
비록 `invoiceFor` 메서드를 사용할 수 있지만, 사전에 정의된 가격(Price) 기반의 `invoicePrice` 및 `tabPrice` 메서드 활용을 권장합니다. 이렇게 하면 Stripe 대시보드에서 상품별로 판매 데이터를 더 정확하게 분석할 수 있습니다.

> [!WARNING]
> `invoice`, `invoicePrice`, `invoiceFor` 메서드는 Stripe 인보이스를 생성하며, 결제 실패가 발생하면 Stripe가 자동으로 재시도할 수 있습니다. 만약 실패 시 인보이스가 다시 시도되는 것을 원하지 않는다면, 첫 결제 실패 후 Stripe API를 통해 인보이스를 직접 닫아야 합니다.

<a name="creating-payment-intents"></a>

<!-- ### Creating Payment Intents -->
### Creating Payment Intents

<!-- You can create a new Stripe payment intent by invoking the `pay` method on a billable model instance. Calling this method will create a payment intent that is wrapped in a `Laravel\Cashier\Payment` instance: -->
청구가 가능한 모델 인스턴스에서 `pay` 메서드를 호출하면 Stripe 결제 의도(Payment Intent)를 생성할 수 있습니다. 이 메서드는 결제 의도가 래핑된 `Laravel\Cashier\Payment` 인스턴스를 반환합니다.

```
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

<!-- After creating the payment intent, you can return the client secret to your application's frontend so that the user can complete the payment in their browser. To read more about building entire payment flows using Stripe payment intents, please consult the [Stripe documentation](https://stripe.com/docs/payments/accept-a-payment?platform=web). -->
결제 의도 생성 후, client secret을 프론트엔드로 반환해 사용자 브라우저상에서 결제가 완료되도록 할 수 있습니다. Stripe 결제 의도를 활용한 전체 결제 플로우 구축 방법은 [Stripe documentation](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참고하세요.

<!-- When using the `pay` method, the default payment methods that are enabled within your Stripe dashboard will be available to the customer. Alternatively, if you only want to allow for some specific payment methods to be used, you may use the `payWith` method: -->
`pay` 메서드를 사용할 때는 Stripe 대시보드에서 활성화된 기본 결제 수단이 모두 제공됩니다. 한편, 특정 결제 수단만 허용하고 싶다면 `payWith` 메서드를 사용할 수 있습니다.

```
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->payWith(
        $request->get('amount'), ['card', 'bancontact']
    );

    return $payment->client_secret;
});
```

> [!WARNING]
> `pay`, `payWith` 메서드 역시 결제 금액을 해당 화폐의 최소 단위(예: USD는 센트)로 입력받아야 합니다.

<a name="refunding-charges"></a>

<!-- ### Refunding Charges -->
### Refunding Charges

<!-- If you need to refund a Stripe charge, you may use the `refund` method. This method accepts the Stripe [payment intent ID](#payment-methods-for-single-charges) as its first argument: -->
Stripe 결제 건을 환불해야 한다면 `refund` 메서드를 사용할 수 있습니다. 이때 첫 번째 인수로 Stripe [payment intent ID](#payment-methods-for-single-charges)를 전달합니다.

```
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
청구가 가능한 모델의 인보이스 배열을 쉽게 조회하려면 `invoices` 메서드를 사용합니다. `invoices` 메서드는 `Laravel\Cashier\Invoice` 인스턴스의 컬렉션을 반환합니다.

```
$invoices = $user->invoices();
```

<!-- If you would like to include pending invoices in the results, you may use the `invoicesIncludingPending` method: -->
대기 중(pending)인 인보이스까지 결과에 포함하고 싶다면 `invoicesIncludingPending` 메서드를 사용할 수 있습니다.

```
$invoices = $user->invoicesIncludingPending();
```

<!-- You may use the `findInvoice` method to retrieve a specific invoice by its ID: -->
특정 ID의 인보이스만 조회하고 싶다면, `findInvoice` 메서드를 사용하세요.

```
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>

<!-- #### Displaying Invoice Information -->
#### Displaying Invoice Information

<!-- When listing the invoices for the customer, you may use the invoice's methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them: -->
고객의 인보이스를 목록으로 표시할 때, 각 인보이스의 메서드를 이용해 주요 정보를 출력할 수 있습니다. 예를 들어, 모든 인보이스를 표로 나열하여 사용자가 다운로드할 수 있도록 할 수 있습니다.

```
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
고객의 예정된(next) 인보이스를 조회하려면 `upcomingInvoice` 메서드를 사용하세요.

```
$invoice = $user->upcomingInvoice();
```

<!-- Similarly, if the customer has multiple subscriptions, you can also retrieve the upcoming invoice for a specific subscription: -->
고객이 여러 구독을 보유하고 있다면, 특정 구독의 예정 인보이스만 조회할 수도 있습니다.

```
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>

<!-- ### Previewing Subscription Invoices -->
### Previewing Subscription Invoices

<!-- Using the `previewInvoice` method, you can preview an invoice before making price changes. This will allow you to determine what your customer's invoice will look like when a given price change is made: -->
`previewInvoice` 메서드를 사용하면, 가격(Price) 변경 전 인보이스가 어떻게 표시될지 미리 확인할 수 있습니다. 이를 통해 고객의 인보이스가 해당 가격 변경으로 어떻게 계산되는지 미리 파악할 수 있습니다.

```
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

<!-- You may pass an array of prices to the `previewInvoice` method in order to preview invoices with multiple new prices: -->
`previewInvoice` 메서드에 가격 배열을 전달하면, 여러 새로운 가격이 반영된 인보이스를 미리 확인할 수도 있습니다.

```
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>

<!-- ### Generating Invoice PDFs -->
### Generating Invoice PDFs

<!-- Before generating invoice PDFs, you should use Composer to install the Dompdf library, which is the default invoice renderer for Cashier: -->
인보이스 PDF를 생성하려면 우선 Composer로 Dompdf 라이브러리를 설치해야 합니다. Dompdf는 Cashier의 기본 인보이스 렌더러입니다.

```shell
composer require dompdf/dompdf
```

<!-- From within a route or controller, you may use the `downloadInvoice` method to generate a PDF download of a given invoice. This method will automatically generate the proper HTTP response needed to download the invoice: -->
라우트나 컨트롤러에서 `downloadInvoice` 메서드를 사용해 해당 인보이스 PDF 다운로드를 구현할 수 있습니다. 이 메서드는 인보이스 다운로드를 위한 적절한 HTTP 응답을 자동으로 생성합니다.

```
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

<!-- By default, all data on the invoice is derived from the customer and invoice data stored in Stripe. The filename is based on your `app.name` config value. However, you can customize some of this data by providing an array as the second argument to the `downloadInvoice` method. This array allows you to customize information such as your company and product details: -->
기본적으로, 인보이스에 표시되는 모든 정보는 Stripe에 저장된 고객 및 인보이스 데이터를 기반으로 합니다. 파일명은 `app.name` 구성 값을 기반으로 합니다. 회사나 상품 정보 등 일부 데이터를 커스터마이즈하려면 `downloadInvoice` 메서드의 두 번째 인수로 배열을 전달하세요.

```
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
`downloadInvoice` 메서드는 세 번째 인수로 커스텀 파일명을 지정할 수도 있으며, 해당 파일명 뒤에 `.pdf`가 자동으로 붙습니다.

```
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>

<!-- #### Custom Invoice Renderer -->
#### Custom Invoice Renderer

<!-- Cashier also makes it possible to use a custom invoice renderer. By default, Cashier uses the `DompdfInvoiceRenderer` implementation, which utilizes the [dompdf](https://github.com/dompdf/dompdf) PHP library to generate Cashier's invoices. However, you may use any renderer you wish by implementing the `Laravel\Cashier\Contracts\InvoiceRenderer` interface. For example, you may wish to render an invoice PDF using an API call to a third-party PDF rendering service: -->
Cashier는 커스텀 인보이스 렌더러도 지원합니다. 기본적으로 Cashier는 [dompdf](https://github.com/dompdf/dompdf) PHP 라이브러리를 활용하는 `DompdfInvoiceRenderer` 구현체를 사용합니다. 하지만, 직접 구현한 렌더러도 사용할 수 있는데, `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현하면 됩니다. 예를 들어, 외부 PDF 렌더링 서비스(API 호출 등)를 통해 인보이스 PDF를 생성할 수 있습니다.

```
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
커스텀 렌더러 구현이 완료되면, 애플리케이션의 `config/cashier.php` 설정 파일에서 `cashier.invoices.renderer` 값을 해당 커스텀 렌더러 클래스명으로 변경해 주십시오.

<a name="checkout"></a>

<!-- ## Checkout -->
## Checkout

<!-- Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page. -->
Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout)도 지원합니다. Stripe Checkout은 결제 페이지를 따로 개발하지 않아도, Stripe에서 미리 만들어 제공하는 호스팅 결제 페이지를 사용할 수 있게 해줍니다.

<!-- The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout). -->
아래는 Cashier로 Stripe Checkout을 시작하는 방법에 대한 안내입니다. Stripe Checkout에 관한 더 자세한 정보가 필요하다면 [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout)도 참고하세요.

<a name="product-checkouts"></a>

<!-- ### Product Checkouts -->
### Product Checkouts

<!-- You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID: -->
Stripe 대시보드 내에 생성해 둔 상품에 대해 `checkout` 메서드를 사용하여 결제 과정을 진행할 수 있습니다. `checkout` 메서드는 Stripe Checkout 세션을 새로 시작합니다. 기본적으로 Stripe Price ID를 인수로 전달해야 합니다.

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

<!-- If needed, you may also specify a product quantity: -->
상품 수량을 지정하고 싶을 때는 아래와 같이 작성할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

<!-- When a customer visits this route they will be redirected to Stripe's Checkout page. By default, when a user successfully completes or cancels a purchase they will be redirected to your `home` route location, but you may specify custom callback URLs using the `success_url` and `cancel_url` options: -->
고객이 이 경로를 방문하면 Stripe의 Checkout 페이지로 자동 리디렉션됩니다. 기본적으로 사용자가 결제를 완료하거나 결제를 취소하면 `home` 경로로 리디렉션되지만, 옵션을 통해 `success_url` 및 `cancel_url`을 커스터마이즈할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

<!-- When defining your `success_url` checkout option, you may instruct Stripe to add the checkout session ID as a query string parameter when invoking your URL. To do so, add the literal string `{CHECKOUT_SESSION_ID}` to your `success_url` query string. Stripe will replace this placeholder with the actual checkout session ID: -->
`success_url` 체크아웃 옵션을 지정할 때, Stripe가 세션 ID를 쿼리 문자열 파라미터로 전달하도록 할 수 있습니다. 이를 위해 `success_url`의 쿼리 문자열에 `{CHECKOUT_SESSION_ID}`라는 리터럴 문자열을 포함시키면, Stripe가 해당 부분을 실제 체크아웃 세션 ID로 대체합니다.

```
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
기본적으로 Stripe Checkout은 [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 지원하지 않습니다. 다행히도 Checkout 페이지에서 이를 활성화할 수 있는 간단한 방법이 있습니다. 이를 위해서는 `allowPromotionCodes` 메서드를 호출하면 됩니다.

```
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
Stripe 대시보드에 미리 생성하지 않은 임시 제품에 대해서도 간단한 결제를 수행할 수 있습니다. 이를 위해 결제가 가능한 모델에서 `checkoutCharge` 메서드를 사용하고, 결제 금액, 상품명, 선택적으로 수량을 전달하면 됩니다. 고객이 이 라우트에 접근하면 Stripe의 Checkout 페이지로 리다이렉트됩니다.

```
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` 메서드를 사용하면 Stripe는 항상 Stripe 대시보드에 새로운 제품과 가격을 생성합니다. 따라서, Stripe 대시보드에 미리 제품을 생성해두고 `checkout` 메서드를 사용하는 것을 권장합니다.

<a name="subscription-checkouts"></a>

<!-- ### Subscription Checkouts -->
### Subscription Checkouts

> [!WARNING]
> 구독을 위해 Stripe Checkout을 사용하는 경우 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 활성화해야 합니다. 이 웹훅은 데이터베이스에 구독 레코드를 생성하고 모든 관련 구독 아이템을 저장합니다.

<!-- You may also use Stripe Checkout to initiate subscriptions. After defining your subscription with Cashier's subscription builder methods, you may call the `checkout `method. When a customer visits this route they will be redirected to Stripe's Checkout page: -->
Stripe Checkout을 통해 구독을 시작할 수도 있습니다. Cashier의 구독 빌더 메서드로 구독을 정의한 뒤, `checkout `메서드를 호출하면 됩니다. 고객이 해당 라우트에 방문하면 Stripe Checkout 페이지로 이동합니다.

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

<!-- Just as with product checkouts, you may customize the success and cancellation URLs: -->
제품 결제와 마찬가지로 성공 및 취소 URL도 커스터마이즈할 수 있습니다.

```
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
물론, 구독 결제에서도 프로모션 코드를 활성화할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->allowPromotionCodes()
        ->checkout();
});
```

> [!WARNING]
> Stripe Checkout을 사용해 구독을 시작할 때는 모든 구독 요금 옵션이 지원되지 않습니다. 구독 빌더에서 `anchorBillingCycleOn` 메서드를 사용하거나, 비례 배분(proration) 또는 결제 행동(payment behavior)을 설정해도 Stripe Checkout 세션에서 적용되지 않습니다. 어떤 파라미터가 사용 가능한지 확인하려면 [the Stripe Checkout Session API documentation](https://stripe.com/docs/api/checkout/sessions/create)를 참고하십시오.

<a name="stripe-checkout-trial-periods"></a>

<!-- #### Stripe Checkout and Trial Periods -->
#### Stripe Checkout and Trial Periods

<!-- Of course, you can define a trial period when building a subscription that will be completed using Stripe Checkout: -->
Stripe Checkout을 통해 마무리되는 구독을 생성할 때도 체험 기간을 정의할 수 있습니다.

```
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<!-- However, the trial period must be at least 48 hours, which is the minimum amount of trial time supported by Stripe Checkout. -->
단, Stripe Checkout에서 지원하는 최소 체험 기간은 48시간 이상이어야 합니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>

<!-- #### Subscriptions and Webhooks -->
#### Subscriptions and Webhooks

<!-- Remember, Stripe and Cashier update subscription statuses via webhooks, so there's a possibility a subscription might not yet be active when the customer returns to the application after entering their payment information. To handle this scenario, you may wish to display a message informing the user that their payment or subscription is pending. -->
Stripe와 Cashier는 웹훅을 통해 구독 상태를 업데이트합니다. 따라서 결제 정보를 입력한 고객이 애플리케이션으로 돌아올 때 구독이 아직 활성화되지 않았을 수 있습니다. 이런 경우, 사용자에게 결제 또는 구독이 보류 중임을 알리는 메시지를 표시하는 것이 좋습니다.

<a name="collecting-tax-ids"></a>

<!-- ### Collecting Tax IDs -->
### Collecting Tax IDs

<!-- Checkout also supports collecting a customer's Tax ID. To enable this on a checkout session, invoke the `collectTaxIds` method when creating the session: -->
Checkout은 고객의 세금 ID도 수집할 수 있습니다. 이를 위해 체크아웃 세션을 생성할 때 `collectTaxIds` 메서드를 호출하면 됩니다.

```
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

<!-- When this method is invoked, a new checkbox will be available to the customer that allows them to indicate if they're purchasing as a company. If so, they will have the opportunity to provide their Tax ID number. -->
이 메서드를 호출하면, 고객이 회사로 구매하는지 여부를 표시할 수 있는 체크박스가 생기며, 회사인 경우 세금 ID를 입력할 수 있게 됩니다.

> [!WARNING]
> 애플리케이션의 서비스 프로바이더에서 [automatic tax collection](#tax-configuration)을 이미 구성했다면 이 기능이 자동으로 활성화되므로, `collectTaxIds` 메서드를 따로 호출할 필요가 없습니다.

<a name="guest-checkouts"></a>

<!-- ### Guest Checkouts -->
### Guest Checkouts

<!-- Using the `Checkout::guest` method, you may initiate checkout sessions for guests of your application that do not have an "account": -->
`Checkout::guest` 메서드를 사용하면 "계정"이 없는 비회원 고객을 위해 체크아웃 세션을 생성할 수 있습니다.

```
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
기존 사용자와 동일하게, `Laravel\Cashier\CheckoutBuilder` 인스턴스의 다양한 메서드를 활용해 비회원 체크아웃 세션도 커스터마이즈할 수 있습니다.

```
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

<!-- After a guest checkout has been completed, Stripe can dispatch a `checkout.session.completed` webhook event, so make sure to [configure your Stripe webhook](https://dashboard.stripe.com/webhooks) to actually send this event to your application. Once the webhook has been enabled within the Stripe dashboard, you may [handle the webhook with Cashier](#handling-stripe-webhooks). The object contained in the webhook payload will be a [`checkout` object](https://stripe.com/docs/api/checkout/sessions/object) that you may inspect in order to fulfill your customer's order. -->
비회원 체크아웃이 완료된 후에 Stripe는 `checkout.session.completed` 웹훅 이벤트를 보낼 수 있습니다. 따라서 반드시 [configure your Stripe webhook](https://dashboard.stripe.com/webhooks)하여 해당 이벤트가 애플리케이션으로 전송되도록 해야 합니다. Stripe 대시보드에서 웹훅을 활성화한 뒤에는 [handle the webhook with Cashier](#handling-stripe-webhooks)할 수 있습니다. 웹훅 페이로드에 담기는 객체는 [`checkout` object](https://stripe.com/docs/api/checkout/sessions/object) 형태이므로, 고객 주문을 처리하기 위해 해당 객체를 참고할 수 있습니다.

<a name="handling-failed-payments"></a>

<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed. -->
때로는 구독이나 단일 결제가 실패할 수 있습니다. 이런 상황이 발생하면 Cashier는 이를 알리는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이 예외를 잡은 후에는 두 가지 방식으로 대응할 수 있습니다.

<!-- First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page: -->
첫 번째로, 고객을 Cashier에 포함된 전용 결제 인증 페이지로 리다이렉트할 수 있습니다. 이 페이지에는 이미 이름이 지정된 라우트가 Cashier의 서비스 프로바이더를 통해 등록되어 있습니다. 따라서 `IncompletePayment` 예외를 캐치해서 사용자를 결제 인증 페이지로 리다이렉트하면 됩니다.

```
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
결제 인증 페이지에서는 고객에게 신용카드 정보를 다시 입력하거나 Stripe에서 요구하는 "3D Secure" 인증 등 추가 절차를 진행하도록 안내됩니다. 결제 인증이 완료되면, 위에 설정한 `redirect` 파라미터의 URL로 사용자가 이동하게 됩니다. 이때 URL에는 `message`(문자열)와 `success`(정수) 쿼리스트링 변수가 추가됩니다. 결제 페이지는 현재 다음과 같은 결제 방식들을 지원합니다.

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
- 알리페이(Alipay)
- 반컨택트(Bancontact)
- BECS 자동이체
- EPS
- GiroPay
- iDEAL
- SEPA 자동이체

<!-- </div> -->
</div>

<!-- Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions. -->
또는 Stripe가 결제 인증 절차를 자체적으로 처리하도록 할 수도 있습니다. 이 경우, 결제 인증 페이지로 리다이렉트하는 대신 Stripe 대시보드에서 [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic)을 설정할 수 있습니다. 다만, `IncompletePayment` 예외가 발생하면 사용자에게 추가 결제 인증을 위한 이메일이 발송됨을 반드시 안내해야 합니다.

<!-- Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions. -->
결제 예외는 `Billable` 트레이트를 사용하는 모델의 `charge`, `invoiceFor`, `invoice` 메서드를 사용할 때 발생할 수 있습니다. 구독과 관련해서는, `SubscriptionBuilder`의 `create` 메서드, 그리고 `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice`, `swapAndInvoice` 메서드도 결제 미완료 예외를 발생시킬 수 있습니다.

<!-- Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
기존 구독에 미완료 결제가 있는지 확인하려면, 결제 가능한 모델 또는 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용하면 됩니다.

```
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

<!-- You can derive the specific status of an incomplete payment by inspecting the `payment` property on the exception instance: -->
미완료 결제의 구체적인 상태는 예외 인스턴스의 `payment` 속성을 확인해서 파악할 수 있습니다.

```
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
일부 결제 방식은 결제 인증을 위해 추가 정보가 필요합니다. 예를 들어, SEPA 결제 방식은 결제 과정 중에 "mandate" 정보가 더 요구됩니다. 이러한 데이터를 Cashier에 전달하려면 `withPaymentConfirmationOptions` 메서드를 사용하면 됩니다.

```
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

<!-- You may consult the [Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm) to review all of the options accepted when confirming payments. -->
결제 인증에 필요한 모든 옵션은 [Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm)에서 확인할 수 있습니다.

<a name="strong-customer-authentication"></a>

<!-- ## Strong Customer Authentication -->
## Strong Customer Authentication

<!-- If your business or one of your customers is based in Europe you will need to abide by the EU's Strong Customer Authentication (SCA) regulations. These regulations were imposed in September 2019 by the European Union to prevent payment fraud. Luckily, Stripe and Cashier are prepared for building SCA compliant applications. -->
귀하의 비즈니스 또는 고객이 유럽에 기반해 있다면, EU의 강력한 고객 인증(SCA) 규정을 반드시 준수해야 합니다. 이 규정은 2019년 9월부터 유럽연합에서 결제 사기를 방지하기 위해 의무화되었습니다. Stripe와 Cashier는 SCA 준수 애플리케이션 개발에 이미 대비되어 있습니다.

> [!WARNING]
> 시작 전에 [Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication)와 [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication)를 반드시 참고하십시오.

<a name="payments-requiring-additional-confirmation"></a>

<!-- ### Payments Requiring Additional Confirmation -->
### Payments Requiring Additional Confirmation

<!-- SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions be found can be found in the documentation on [handling failed payments](#handling-failed-payments). -->
SCA 규정에 따라 결제 과정에서 추가 인증이 요구되는 경우가 많습니다. 이때 Cashier는 추가 인증이 필요하다는 것을 알려주는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이 예외를 처리하는 방법에 대해서는 [handling failed payments](#handling-failed-payments) 문장에서 자세히 다룹니다.

<!-- Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
Stripe 또는 Cashier가 제공하는 결제 인증 화면은 은행 또는 카드 발급사의 결제 방식에 맞춰 커스터마이즈될 수 있으며, 추가 카드 인증, 임시 소액 결제, 별도의 장치 인증 등 다양한 인증 절차가 포함될 수 있습니다.

<a name="incomplete-and-past-due-state"></a>

<!-- #### Incomplete and Past Due State -->
#### Incomplete and Past Due State

<!-- When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion. -->
추가 인증이 필요한 결제의 경우, 구독은 데이터베이스의 `stripe_status` 컬럼에서 `incomplete` 또는 `past_due` 상태로 남아 있게 됩니다. 결제 인증이 완료되고 Stripe 웹훅을 통해 애플리케이션에 통지가 오면 Cashier가 자동으로 고객의 구독을 활성화합니다.

<!-- For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status). -->
`incomplete`와 `past_due` 상태에 대한 자세한 내용은 [our additional documentation on these states](#incomplete-and-past-due-status)를 참고하세요.

<a name="off-session-payment-notifications"></a>

<!-- ### Off-Session Payment Notifications -->
### Off-Session Payment Notifications

<!-- Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to a notification class. By default, this notification is disabled. Of course, Cashier includes a notification class you may use for this purpose, but you are free to provide your own notification class if desired: -->
SCA 규정으로 인해 구독이 활성 상태이더라도, 고객이 간혹 결제 정보를 다시 인증해야 하는 경우가 있습니다. 예를 들어, 구독이 갱신될 때 등이 해당합니다. Cashier에서는 이런 오프세션 결제 인증이 필요할 때 고객에게 알림을 보낼 수 있습니다. 이를 위해 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수에 알림 클래스를 지정하면 됩니다. 기본적으로 이 알림은 비활성화되어 있습니다. Cashier에서 제공하는 알림 클래스를 사용할 수도 있고, 직접 만든 클래스를 사용할 수도 있습니다.

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

<!-- To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait. -->
오프세션 결제 인증 알림이 정상적으로 전달되려면, 애플리케이션에 [Stripe webhooks are configured](#handling-stripe-webhooks)되어 있고, Stripe 대시보드에서 `invoice.payment_action_required` 웹훅도 활성화되어 있어야 합니다. 또한, `Billable` 모델은 Laravel의 `Illuminate\Notifications\Notifiable` 트레이트를 반드시 사용해야 합니다.

> [!WARNING]
> 고객이 직접 결제를 진행하더라도(수동 결제), 추가 인증이 필요하다면 알림이 발송됩니다. Stripe는 해당 결제가 수동인지, 오프세션(off-session)인지를 구분할 수 없습니다. 그러나 고객이 결제 인증 페이지에 이미 성공한 뒤 재접속하더라도 "결제 성공" 메시지로 안내되며, 실수로 같은 결제를 두 번 인증하여 중복 청구가 발생하는 일은 없습니다.

<a name="stripe-sdk"></a>

<!-- ## Stripe SDK -->
## Stripe SDK

<!-- Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method: -->
Cashier에서 제공하는 다양한 객체들은 Stripe SDK 객체를 래핑한 형태입니다. Stripe 객체를 직접 다루고 싶다면 `asStripe` 메서드로 쉽게 가져올 수 있습니다.

```
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

<!-- You may also use the `updateStripeSubscription` method to update a Stripe subscription directly: -->
또한 `updateStripeSubscription` 메서드를 사용해 Stripe 구독 정보를 직접 업데이트할 수도 있습니다.

```
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

<!-- You may invoke the `stripe` method on the `Cashier` class if you would like to use the `Stripe\StripeClient` client directly. For example, you could use this method to access the `StripeClient` instance and retrieve a list of prices from your Stripe account: -->
`Stripe\StripeClient` 객체를 직접 사용하려면 `Cashier` 클래스의 `stripe` 메서드를 호출하면 됩니다. 예를 들어, 이 메서드로 `StripeClient` 인스턴스에 접근해 Stripe 계정에서 가격 목록을 가져올 수 있습니다.

```
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>

<!-- ## Testing -->
## Testing

<!-- When testing an application that uses Cashier, you may mock the actual HTTP requests to the Stripe API; however, this requires you to partially re-implement Cashier's own behavior. Therefore, we recommend allowing your tests to hit the actual Stripe API. While this is slower, it provides more confidence that your application is working as expected and any slow tests may be placed within their own Pest / PHPUnit testing group. -->
Cashier를 사용하는 애플리케이션을 테스트할 때 Stripe API로의 실제 HTTP 요청을 mocking(가짜로 대체)할 수도 있지만, 이 경우 Cashier의 동작을 일부 재현해야 하므로 권장하지 않습니다. 대신, 실제 Stripe API를 테스트 환경에서 직접 호출하는 것을 추천합니다. 비록 속도가 다소 느릴 수 있지만, 이를 통해 애플리케이션이 올바르게 동작하는지 더 신뢰할 수 있고, 느린 테스트는 별도의 Pest / PHPUnit 테스트 그룹에 분리해 관리할 수 있습니다.

<!-- When testing, remember that Cashier itself already has a great test suite, so you should only focus on testing the subscription and payment flow of your own application and not every underlying Cashier behavior. -->
테스트 시에는 Cashier 자체가 이미 훌륭한 테스트 스위트를 갖추고 있으므로, 직접 개발한 애플리케이션의 구독 및 결제 흐름만을 중점적으로 테스트하면 충분합니다. Cashier 내부의 모든 동작까지 테스트할 필요는 없습니다.

<!-- To get started, add the **testing** version of your Stripe secret to your `phpunit.xml` file: -->
테스트를 시작하려면, `phpunit.xml` 파일에 Stripe secret의 **테스트용** 버전을 추가합니다.

```
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

<!-- Now, whenever you interact with Cashier while testing, it will send actual API requests to your Stripe testing environment. For convenience, you should pre-fill your Stripe testing account with subscriptions / prices that you may use during testing. -->
이제 Cashier와 상호작용하는 테스트를 실행할 때는 실제 Stripe 테스트 환경으로 API 요청이 전송됩니다. 편의를 위해, Stripe 테스트 계정에 미리 구독/가격 정보를 세팅해 두는 것이 좋습니다.

> [!NOTE]
> 결제 거부나 실패 등 다양한 결제 상황을 테스트하려면 Stripe에서 제공하는 [testing card numbers and tokens](https://stripe.com/docs/testing)을 활용할 수 있습니다.
