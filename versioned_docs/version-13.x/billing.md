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
[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe's](https://stripe.com)의 구독 청구 서비스를 표현력 있고 유창한 인터페이스로 사용할 수 있게 해줍니다. 직접 작성하기 부담스러운 구독 청구 관련 반복 코드를 거의 모두 처리합니다. 기본적인 구독 관리뿐만 아니라 Cashier는 쿠폰, 구독 변경, 구독 "수량", 취소 유예 기간을 처리할 수 있으며, 인보이스 PDF까지 생성할 수 있습니다.

<a name="upgrading-cashier"></a>
<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md). -->
Cashier의 새 버전으로 업그레이드할 때는 [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

> [!WARNING]
> 호환성이 깨지는 변경을 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 16은 Stripe API 버전 `2025-06-30.basil`을 사용합니다. 새로운 Stripe 기능과 개선 사항을 활용할 수 있도록 Stripe API 버전은 마이너 릴리스에서 업데이트됩니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Stripe using the Composer package manager: -->
먼저 Composer 패키지 매니저를 사용해 Stripe용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier
```

<!-- After installing the package, publish Cashier's migrations using the `vendor:publish` Artisan command: -->
패키지를 설치한 후 `vendor:publish` Artisan 명령어를 사용해 Cashier의 마이그레이션을 게시합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- Then, migrate your database: -->
그다음 데이터베이스를 마이그레이션합니다.

```shell
php artisan migrate
```

<!-- Cashier's migrations will add several columns to your `users` table. They will also create a new `subscriptions` table to hold all of your customer's subscriptions and a `subscription_items` table for subscriptions with multiple prices. -->
Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가합니다. 또한 고객의 모든 구독을 저장할 새 `subscriptions` 테이블과 여러 가격을 포함하는 구독을 위한 `subscription_items` 테이블도 생성합니다.

<!-- If you wish, you can also publish Cashier's configuration file using the `vendor:publish` Artisan command: -->
원한다면 `vendor:publish` Artisan 명령어를 사용해 Cashier의 설정 파일도 게시할 수 있습니다.

```shell
php artisan vendor:publish --tag="cashier-config"
```

<!-- Lastly, to ensure Cashier properly handles all Stripe events, remember to [configure Cashier's webhook handling](#handling-stripe-webhooks). -->
마지막으로 Cashier가 모든 Stripe 이벤트를 올바르게 처리하도록 [configure Cashier's webhook handling](#handling-stripe-webhooks)을 구성해야 합니다.

> [!WARNING]
> Stripe는 Stripe 식별자를 저장하는 데 사용되는 모든 컬럼이 대소문자를 구분해야 한다고 권장합니다. 따라서 MySQL을 사용할 때는 `stripe_id` 컬럼의 컬럼 collation이 `utf8_bin`으로 설정되어 있는지 확인해야 합니다. 이에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인할 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>
<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, add the `Billable` trait to your billable model definition. Typically, this will be the `App\Models\User` model. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information: -->
Cashier를 사용하기 전에 결제 가능 모델 정의에 `Billable` trait을 추가합니다. 일반적으로 이는 `App\Models\User` 모델입니다. 이 trait은 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트와 같은 일반적인 청구 작업을 수행할 수 있는 다양한 메서드를 제공합니다.

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- Cashier assumes your billable model will be the `App\Models\User` class that ships with Laravel. If you wish to change this you may specify a different model via the `useCustomerModel` method. This method should typically be called in the `boot` method of your `AppServiceProvider` class: -->
Cashier는 결제 가능 모델이 Laravel에 포함되어 제공되는 `App\Models\User` 클래스라고 가정합니다. 이를 변경하려면 `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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
> Laravel이 제공하는 `App\Models\User` 모델이 아닌 다른 모델을 사용하는 경우, 대체 모델의 테이블 이름에 맞도록 제공된 [Cashier migrations](#installation)을 게시하고 수정해야 합니다.

<a name="api-keys"></a>
<!-- ### API Keys -->
### API Keys

<!-- Next, you should configure your Stripe API keys in your application's `.env` file. You can retrieve your Stripe API keys from the Stripe control panel: -->
다음으로 애플리케이션의 `.env` 파일에 Stripe API 키를 설정해야 합니다. Stripe 제어판에서 Stripe API 키를 가져올 수 있습니다.

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 정의되어 있는지 확인해야 합니다. 이 변수는 수신되는 Webhook이 실제로 Stripe에서 온 것인지 확인하는 데 사용됩니다.

<a name="currency-configuration"></a>
<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
Cashier의 기본 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정하여 기본 통화를 변경할 수 있습니다.

```ini
CASHIER_CURRENCY=eur
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
Cashier의 통화를 설정하는 것 외에도, 인보이스에 표시할 금액 값을 포맷할 때 사용할 locale을 지정할 수 있습니다. 내부적으로 Cashier는 통화 locale을 설정하기 위해 [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 locale을 사용하려면 서버에 `ext-intl` PHP 확장이 설치되고 설정되어 있는지 확인하십시오.

<a name="tax-configuration"></a>
<!-- ### Tax Configuration -->
### Tax Configuration

<!-- Thanks to [Stripe Tax](https://stripe.com/tax), it's possible to automatically calculate taxes for all invoices generated by Stripe. You can enable automatic tax calculation by invoking the `calculateTaxes` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
[Stripe Tax](https://stripe.com/tax)를 사용하면 Stripe가 생성하는 모든 인보이스의 세금을 자동으로 계산할 수 있습니다. 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출해 자동 세금 계산을 활성화할 수 있습니다.

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
세금 계산이 활성화되면 새 구독과 생성되는 모든 일회성 인보이스에 자동 세금 계산이 적용됩니다.

<!-- For this feature to work properly, your customer's billing details, such as the customer's name, address, and tax ID, need to be synced to Stripe. You may use the [customer data synchronization](#syncing-customer-data-with-stripe) and [Tax ID](#tax-ids) methods offered by Cashier to accomplish this. -->
이 기능이 제대로 동작하려면 고객 이름, 주소, 세금 ID와 같은 고객의 청구 정보가 Stripe에 동기화되어 있어야 합니다. 이를 위해 Cashier가 제공하는 [customer data synchronization](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 메서드를 사용할 수 있습니다.

<a name="logging"></a>
<!-- ### Logging -->
### Logging

<!-- Cashier allows you to specify the log channel to be used when logging fatal Stripe errors. You may specify the log channel by defining the `CASHIER_LOGGER` environment variable within your application's `.env` file: -->
Cashier는 치명적인 Stripe 오류를 기록할 때 사용할 로그 채널을 지정할 수 있게 해줍니다. 애플리케이션의 `.env` 파일에서 `CASHIER_LOGGER` 환경 변수를 정의해 로그 채널을 지정할 수 있습니다.

```ini
CASHIER_LOGGER=stack
```

<!-- Exceptions that are generated by API calls to Stripe will be logged through your application's default log channel. -->
Stripe에 대한 API 호출에서 생성되는 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
<!-- ### Using Custom Models -->
### Using Custom Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
자체 모델을 정의하고 해당 Cashier 모델을 확장하여 Cashier가 내부적으로 사용하는 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Cashier\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
모델을 정의한 후에는 `Laravel\Cashier\Cashier` 클래스를 통해 Cashier가 사용자 정의 모델을 사용하도록 지시할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 Cashier에 사용자 정의 모델을 알려야 합니다.

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
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에서 고정 가격이 있는 Products를 정의해야 합니다. 또한 [configure Cashier's webhook handling](#handling-stripe-webhooks)을 구성해야 합니다.

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations. -->
애플리케이션에서 제품 및 구독 청구를 제공하는 일은 부담스럽게 느껴질 수 있습니다. 하지만 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 사용하면 현대적이고 견고한 결제 연동을 쉽게 구축할 수 있습니다.

<!-- To charge customers for non-recurring, single-charge products, we'll utilize Cashier to direct customers to Stripe Checkout, where they will provide their payment details and confirm their purchase. Once the payment has been made via Checkout, the customer will be redirected to a success URL of your choosing within your application: -->
반복 결제가 아닌 단건 결제 제품에 대해 고객에게 청구하려면, Cashier를 사용해 고객을 Stripe Checkout으로 안내합니다. 그곳에서 고객은 결제 정보를 입력하고 구매를 확인합니다. Checkout을 통해 결제가 완료되면 고객은 애플리케이션 내에서 사용자가 선택한 성공 URL로 리디렉션됩니다.

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
위 예제에서 볼 수 있듯이, Cashier가 제공하는 `checkout` 메서드를 사용해 특정 "가격 식별자"에 대한 Stripe Checkout으로 고객을 리디렉션합니다. Stripe에서 "prices"는 [defined prices for specific products](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

<!-- If necessary, the `checkout` method will automatically create a customer in Stripe and connect that Stripe customer record to the corresponding user in your application's database. After completing the checkout session, the customer will be redirected to a dedicated success or cancellation page where you can display an informational message to the customer. -->
필요한 경우 `checkout` 메서드는 Stripe에 고객을 자동으로 생성하고, 해당 Stripe 고객 레코드를 애플리케이션 데이터베이스의 해당 사용자와 연결합니다. Checkout 세션을 완료한 후 고객은 전용 성공 또는 취소 페이지로 리디렉션되며, 여기에서 고객에게 안내 메시지를 표시할 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
<!-- #### Providing Meta Data to Stripe Checkout -->
#### Providing Meta Data to Stripe Checkout

<!-- When selling products, it's common to keep track of completed orders and purchased products via `Cart` and `Order` models defined by your own application. When redirecting customers to Stripe Checkout to complete a purchase, you may need to provide an existing order identifier so that you can associate the completed purchase with the corresponding order when the customer is redirected back to your application. -->
제품을 판매할 때는 애플리케이션에서 정의한 `Cart` 및 `Order` 모델을 통해 완료된 주문과 구매한 제품을 추적하는 경우가 많습니다. 고객을 Stripe Checkout으로 리디렉션해 구매를 완료하게 할 때, 고객이 애플리케이션으로 다시 리디렉션되었을 때 완료된 구매를 해당 주문과 연결할 수 있도록 기존 주문 식별자를 제공해야 할 수 있습니다.

<!-- To accomplish this, you may provide an array of `metadata` to the `checkout` method. Let's imagine that a pending `Order` is created within our application when a user begins the checkout process. Remember, the `Cart` and `Order` models in this example are illustrative and not provided by Cashier. You are free to implement these concepts based on the needs of your own application: -->
이를 위해 `checkout` 메서드에 `metadata` 배열을 제공할 수 있습니다. 사용자가 Checkout 프로세스를 시작할 때 애플리케이션 안에서 대기 중인 `Order`가 생성된다고 가정해 보겠습니다. 이 예제의 `Cart` 및 `Order` 모델은 설명을 위한 것이며 Cashier가 제공하지 않는다는 점을 기억하십시오. 이러한 개념은 애플리케이션의 필요에 맞게 자유롭게 구현할 수 있습니다.

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
위 예제에서 볼 수 있듯이, 사용자가 Checkout 프로세스를 시작하면 장바구니 / 주문에 연결된 모든 Stripe 가격 식별자를 `checkout` 메서드에 제공합니다. 물론 고객이 항목을 추가할 때 이러한 항목을 "shopping cart" 또는 주문과 연결하는 책임은 애플리케이션에 있습니다. 또한 `metadata` 배열을 통해 주문의 ID를 Stripe Checkout 세션에 제공합니다. 마지막으로 Checkout 성공 route에 `CHECKOUT_SESSION_ID` 템플릿 변수를 추가했습니다. Stripe가 고객을 애플리케이션으로 다시 리디렉션할 때 이 템플릿 변수는 Checkout 세션 ID로 자동 채워집니다.

<!-- Next, let's build the Checkout success route. This is the route that users will be redirected to after their purchase has been completed via Stripe Checkout. Within this route, we can retrieve the Stripe Checkout session ID and the associated Stripe Checkout instance in order to access our provided meta data and update our customer's order accordingly: -->
다음으로 Checkout 성공 route를 만들어 보겠습니다. 이 route는 고객의 구매가 Stripe Checkout을 통해 완료된 후 사용자가 리디렉션되는 route입니다. 이 route 안에서는 Stripe Checkout 세션 ID와 관련 Stripe Checkout 인스턴스를 조회해, 제공한 메타데이터에 접근하고 고객의 주문을 그에 맞게 업데이트할 수 있습니다.

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
[data contained by the Checkout session object](https://stripe.com/docs/api/checkout/sessions/object)에 대한 자세한 내용은 Stripe 문서를 참고하십시오.

<a name="quickstart-selling-subscriptions"></a>
<!-- ### Selling Subscriptions -->
### Selling Subscriptions

> [!NOTE]
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에서 고정 가격이 있는 Products를 정의해야 합니다. 또한 [configure Cashier's webhook handling](#handling-stripe-webhooks)을 구성해야 합니다.

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations. -->
애플리케이션에서 제품 및 구독 청구를 제공하는 일은 부담스럽게 느껴질 수 있습니다. 하지만 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 사용하면 현대적이고 견고한 결제 연동을 쉽게 구축할 수 있습니다.

<!-- To learn how to sell subscriptions using Cashier and Stripe Checkout, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Stripe dashboard. In addition, our subscription service might offer an Expert plan as `pro_expert`. -->
Cashier와 Stripe Checkout을 사용해 구독을 판매하는 방법을 알아보기 위해, 기본 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 플랜이 있는 단순한 구독 서비스 시나리오를 살펴보겠습니다. 이 두 가격은 Stripe 대시보드에서 "Basic" 제품(`pro_basic`) 아래에 묶을 수 있습니다. 또한 구독 서비스는 `pro_expert`라는 Expert 플랜을 제공할 수도 있습니다.

<!-- First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button or link should direct the user to a Laravel route which creates the Stripe Checkout session for their chosen plan: -->
먼저 고객이 어떻게 서비스에 구독할 수 있는지 살펴보겠습니다. 예를 들어 고객이 애플리케이션의 가격 페이지에서 Basic 플랜의 "subscribe" 버튼을 클릭한다고 생각할 수 있습니다. 이 버튼 또는 링크는 사용자가 선택한 플랜에 대한 Stripe Checkout 세션을 생성하는 Laravel route로 사용자를 안내해야 합니다.

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
위 예제에서 볼 수 있듯이, 고객이 Basic 플랜에 구독할 수 있도록 Stripe Checkout 세션으로 리디렉션합니다. Checkout이 성공하거나 취소된 후 고객은 `checkout` 메서드에 제공한 URL로 다시 리디렉션됩니다. 일부 결제 수단은 처리에 몇 초가 필요하므로 구독이 실제로 시작된 시점을 알기 위해서는 [configure Cashier's webhook handling](#handling-stripe-webhooks)도 구성해야 합니다.

<!-- Now that customers can start subscriptions, we need to restrict certain portions of our application so that only subscribed users can access them. Of course, we can always determine a user's current subscription status via the `subscribed` method provided by Cashier's `Billable` trait: -->
이제 고객이 구독을 시작할 수 있으므로, 구독한 사용자만 접근할 수 있도록 애플리케이션의 특정 영역을 제한해야 합니다. 물론 Cashier의 `Billable` trait이 제공하는 `subscribed` 메서드를 통해 사용자의 현재 구독 상태를 언제든지 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

<!-- We can even easily determine if a user is subscribed to specific product or price: -->
특정 제품이나 가격에 사용자가 구독되어 있는지도 쉽게 확인할 수 있습니다.

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

<!-- For convenience, you may wish to create a [middleware](/docs/13.x/middleware) which determines if the incoming request is from a subscribed user. Once this middleware has been defined, you may easily assign it to a route to prevent users that are not subscribed from accessing the route: -->
편의를 위해 들어오는 요청이 구독한 사용자로부터 온 것인지 판단하는 [middleware](/docs/13.x/middleware)를 만들 수 있습니다. 이 Middleware를 정의한 후에는 route에 쉽게 할당하여 구독하지 않은 사용자가 해당 route에 접근하지 못하도록 할 수 있습니다.

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
Middleware를 정의한 후에는 route에 할당할 수 있습니다:

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
물론 고객은 구독 플랜을 다른 제품이나 "tier(등급)"로 변경하고 싶을 수 있습니다. 이를 허용하는 가장 쉬운 방법은 고객을 Stripe의 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)로 안내하는 것입니다. 이 포털은 고객이 인보이스를 다운로드하고, 결제 수단을 업데이트하며, 구독 플랜을 변경할 수 있는 호스팅 사용자 인터페이스를 제공합니다.

<!-- First, define a link or button within your application that directs users to a Laravel route which we will utilize to initiate a Billing Portal session: -->
먼저, Billing Portal 세션을 시작하는 데 사용할 Laravel 라우트로 사용자를 안내하는 링크나 버튼을 애플리케이션 안에 정의합니다.

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

<!-- Next, let's define the route that initiates a Stripe Customer Billing Portal session and redirects the user to the Portal. The `redirectToBillingPortal` method accepts the URL that users should be returned to when exiting the Portal: -->
다음으로, Stripe Customer Billing Portal 세션을 시작하고 사용자를 포털로 리다이렉트하는 라우트를 정의해 보겠습니다. `redirectToBillingPortal` 메서드는 사용자가 포털을 나갈 때 돌아와야 할 URL을 인수로 받습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 webhook 처리를 설정해 두었다면, Cashier는 Stripe에서 들어오는 webhook을 검사하여 애플리케이션의 Cashier 관련 데이터베이스 테이블을 자동으로 동기화합니다. 예를 들어 사용자가 Stripe의 Customer Billing Portal을 통해 구독을 취소하면, Cashier는 해당 webhook을 수신하고 애플리케이션 데이터베이스에서 그 구독을 "canceled"로 표시합니다.

<a name="customers"></a>
<!-- ## Customers -->
## Customers

<a name="retrieving-customers"></a>
<!-- ### Retrieving Customers -->
### Retrieving Customers

<!-- You can retrieve a customer by their Stripe ID using the `Cashier::findBillable` method. This method will return an instance of the billable model: -->
`Cashier::findBillable` 메서드를 사용하면 Stripe ID로 고객을 조회할 수 있습니다. 이 메서드는 결제 가능 모델의 인스턴스를 반환합니다.

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
<!-- ### Creating Customers -->
### Creating Customers

<!-- Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method: -->
때로는 구독을 시작하지 않고 Stripe 고객을 생성하고 싶을 수 있습니다. 이 작업은 `createAsStripeCustomer` 메서드를 사용해 수행할 수 있습니다.

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

<!-- Once the customer has been created in Stripe, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create): -->
Stripe에 고객이 생성되면 나중에 구독을 시작할 수 있습니다. Stripe API에서 지원하는 추가 [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create)를 전달하려면 선택적으로 `$options` 배열을 제공할 수 있습니다.

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

<!-- You may use the `asStripeCustomer` method if you want to return the Stripe customer object for a billable model: -->
결제 가능 모델에 대한 Stripe 고객 객체를 반환하고 싶다면 `asStripeCustomer` 메서드를 사용할 수 있습니다.

```php
$stripeCustomer = $user->asStripeCustomer();
```

<!-- The `createOrGetStripeCustomer` method may be used if you would like to retrieve the Stripe customer object for a given billable model but are not sure whether the billable model is already a customer within Stripe. This method will create a new customer in Stripe if one does not already exist: -->
특정 결제 가능 모델에 대한 Stripe 고객 객체를 조회하고 싶지만, 해당 결제 가능 모델이 이미 Stripe의 고객인지 확실하지 않은 경우 `createOrGetStripeCustomer` 메서드를 사용할 수 있습니다. 이 메서드는 기존 고객이 없으면 Stripe에 새 고객을 생성합니다.

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
<!-- ### Updating Customers -->
### Updating Customers

<!-- Occasionally, you may wish to update the Stripe customer directly with additional information. You may accomplish this using the `updateStripeCustomer` method. This method accepts an array of [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update): -->
때로는 추가 정보를 사용해 Stripe 고객을 직접 업데이트하고 싶을 수 있습니다. 이 작업은 `updateStripeCustomer` 메서드를 사용해 수행할 수 있습니다. 이 메서드는 Stripe API에서 지원하는 [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update)의 배열을 받습니다.

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
<!-- ### Balances -->
### Balances

<!-- Stripe allows you to credit or debit a customer's "balance". Later, this balance will be credited or debited on new invoices. To check the customer's total balance you may use the `balance` method that is available on your billable model. The `balance` method will return a formatted string representation of the balance in the customer's currency: -->
Stripe에서는 고객의 "balance(잔액)"를 credit(입금)하거나 debit(차감)할 수 있습니다. 이후 새 인보이스에서 이 잔액이 입금 또는 차감됩니다. 고객의 총 잔액을 확인하려면 결제 가능 모델에서 사용할 수 있는 `balance` 메서드를 사용하면 됩니다. `balance` 메서드는 고객의 통화로 형식화된 잔액 문자열을 반환합니다.

```php
$balance = $user->balance();
```

<!-- To credit a customer's balance, you may provide a value to the `creditBalance` method. If you wish, you may also provide a description: -->
고객의 잔액에 credit을 추가하려면 `creditBalance` 메서드에 값을 제공하면 됩니다. 원한다면 설명도 함께 제공할 수 있습니다.

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

<!-- Providing a value to the `debitBalance` method will debit the customer's balance: -->
`debitBalance` 메서드에 값을 제공하면 고객의 잔액에서 debit이 차감됩니다.

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

<!-- The `applyBalance` method will create new customer balance transactions for the customer. You may retrieve these transaction records using the `balanceTransactions` method, which may be useful in order to provide a log of credits and debits for the customer to review: -->
`applyBalance` 메서드는 고객에 대한 새 고객 잔액 트랜잭션을 생성합니다. `balanceTransactions` 메서드를 사용해 이러한 트랜잭션 기록을 조회할 수 있으며, 이는 고객이 검토할 수 있는 credit 및 debit 로그를 제공할 때 유용합니다.

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
Cashier는 고객의 세금 ID를 쉽게 관리할 수 있는 방법을 제공합니다. 예를 들어 `taxIds` 메서드를 사용하면 고객에게 할당된 모든 [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션으로 조회할 수 있습니다.

```php
$taxIds = $user->taxIds();
```

<!-- You can also retrieve a specific tax ID for a customer by its identifier: -->
식별자를 사용해 고객의 특정 세금 ID를 조회할 수도 있습니다.

```php
$taxId = $user->findTaxId('txi_belgium');
```

<!-- You may create a new Tax ID by providing a valid [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) and value to the `createTaxId` method: -->
유효한 [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 `createTaxId` 메서드에 제공하여 새 Tax ID를 생성할 수 있습니다.

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

<!-- The `createTaxId` method will immediately add the VAT ID to the customer's account. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); however, this is an asynchronous process. You can be notified of verification updates by subscribing to the `customer.tax_id.updated` webhook event and inspecting [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). For more information on handling webhooks, please consult the [documentation on defining webhook handlers](#handling-stripe-webhooks). -->
`createTaxId` 메서드는 VAT ID를 고객 계정에 즉시 추가합니다. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation)하지만, 이 과정은 비동기적으로 처리됩니다. `customer.tax_id.updated` webhook 이벤트를 구독하고 [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 검사하면 검증 업데이트 알림을 받을 수 있습니다. webhook 처리에 대한 자세한 내용은 [documentation on defining webhook handlers](#handling-stripe-webhooks)를 참고하십시오.

<!-- You may delete a tax ID using the `deleteTaxId` method: -->
`deleteTaxId` 메서드를 사용해 세금 ID를 삭제할 수 있습니다.

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
<!-- ### Syncing Customer Data With Stripe -->
### Syncing Customer Data With Stripe

<!-- Typically, when your application's users update their name, email address, or other information that is also stored by Stripe, you should inform Stripe of the updates. By doing so, Stripe's copy of the information will be in sync with your application's. -->
일반적으로 애플리케이션의 사용자가 이름, 이메일 주소 또는 Stripe에도 저장되는 기타 정보를 업데이트하면, 해당 업데이트를 Stripe에 알려야 합니다. 이렇게 하면 Stripe에 저장된 정보 사본이 애플리케이션과 동기화됩니다.

<!-- To automate this, you may define an event listener on your billable model that reacts to the model's `updated` event. Then, within your event listener, you may invoke the `syncStripeCustomerDetails` method on the model: -->
이를 자동화하려면 모델의 `updated` 이벤트에 반응하는 이벤트 리스너를 결제 가능 모델에 정의할 수 있습니다. 그런 다음 이벤트 리스너 안에서 모델의 `syncStripeCustomerDetails` 메서드를 호출하면 됩니다.

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
Cashier가 제공하는 여러 메서드를 오버라이드하여 고객 정보를 Stripe에 동기화할 때 사용할 컬럼을 사용자 지정할 수 있습니다. 예를 들어 `stripeName` 메서드를 오버라이드하면 Cashier가 고객 정보를 Stripe에 동기화할 때 고객의 "name"으로 간주할 속성을 사용자 지정할 수 있습니다.

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
마찬가지로 `stripeEmail`, `stripePhone`(최대 20자), `stripeAddress`, `stripePreferredLocales` 메서드를 오버라이드할 수 있습니다. 이 메서드들은 [updating the Stripe customer object](https://stripe.com/docs/api/customers/update)할 때 각각 대응되는 고객 매개변수로 정보를 동기화합니다. 고객 정보 동기화 과정을 완전히 제어하고 싶다면 `syncStripeCustomerDetails` 메서드를 오버라이드할 수 있습니다.

<a name="billing-portal"></a>
<!-- ### Billing Portal -->
### Billing Portal

<!-- Stripe offers [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) so that your customer can manage their subscription, payment methods, and view their billing history. You can redirect your users to the billing portal by invoking the `redirectToBillingPortal` method on the billable model from a controller or route: -->
Stripe는 고객이 자신의 구독, 결제 수단을 관리하고 결제 이력을 확인할 수 있도록 [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 컨트롤러나 라우트에서 결제 가능 모델의 `redirectToBillingPortal` 메서드를 호출하여 사용자를 결제 포털로 리다이렉트할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

<!-- By default, when the user is finished managing their subscription, they will be able to return to the `home` route of your application via a link within the Stripe billing portal. You may provide a custom URL that the user should return to by passing the URL as an argument to the `redirectToBillingPortal` method: -->
기본적으로 사용자가 구독 관리를 마치면 Stripe 결제 포털 안의 링크를 통해 애플리케이션의 `home` 라우트로 돌아올 수 있습니다. 사용자가 돌아와야 할 사용자 지정 URL을 제공하려면 해당 URL을 `redirectToBillingPortal` 메서드의 인수로 전달하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

<!-- If you would like to generate the URL to the billing portal without generating an HTTP redirect response, you may invoke the `billingPortalUrl` method: -->
HTTP 리다이렉트 응답을 생성하지 않고 결제 포털 URL만 생성하고 싶다면 `billingPortalUrl` 메서드를 호출할 수 있습니다.

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
Stripe로 구독을 생성하거나 "one-off(일회성)" 결제를 수행하려면 결제 수단을 저장하고 Stripe에서 해당 식별자를 조회해야 합니다. 이를 수행하는 방식은 결제 수단을 구독에 사용할지, 단일 결제에 사용할지에 따라 달라집니다. 아래에서 두 경우를 모두 살펴보겠습니다.

<a name="payment-methods-for-subscriptions"></a>
<!-- #### Payment Methods for Subscriptions -->
#### Payment Methods for Subscriptions

<!-- When storing a customer's credit card information for future use by a subscription, the Stripe "Setup Intents" API must be used to securely gather the customer's payment method details. A "Setup Intent" indicates to Stripe the intention to charge a customer's payment method. Cashier's `Billable` trait includes the `createSetupIntent` method to easily create a new Setup Intent. You should invoke this method from the route or controller that will render the form which gathers your customer's payment method details: -->
나중에 구독에서 사용할 고객의 신용카드 정보를 저장할 때는 고객의 결제 수단 세부 정보를 안전하게 수집하기 위해 Stripe의 "Setup Intents" API를 사용해야 합니다. "Setup Intent"는 고객의 결제 수단에 청구하려는 의도를 Stripe에 알려 줍니다. Cashier의 `Billable` trait에는 새 Setup Intent를 쉽게 생성할 수 있는 `createSetupIntent` 메서드가 포함되어 있습니다. 고객의 결제 수단 세부 정보를 수집하는 폼을 렌더링할 라우트나 컨트롤러에서 이 메서드를 호출해야 합니다.

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

<!-- After you have created the Setup Intent and passed it to the view, you should attach its secret to the element that will gather the payment method. For example, consider this "update payment method" form: -->
Setup Intent를 생성하고 뷰에 전달한 뒤에는 결제 수단을 수집할 요소에 해당 secret을 연결해야 합니다. 예를 들어 다음 "결제 수단 업데이트" 폼을 살펴보십시오.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

<!-- Next, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
다음으로 Stripe.js 라이브러리를 사용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 연결하고 고객의 결제 세부 정보를 안전하게 수집할 수 있습니다.

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
다음으로 카드를 검증하고 [Stripe's `confirmCardSetup` method](https://stripe.com/docs/js/setup_intents/confirm_card_setup)를 사용해 Stripe에서 안전한 "결제 수단 식별자"를 조회할 수 있습니다.

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
Stripe에서 카드가 검증되면 결과로 받은 `setupIntent.payment_method` 식별자를 Laravel 애플리케이션으로 전달할 수 있으며, 여기에서 고객에게 연결할 수 있습니다. 결제 수단은 [added as a new payment method](#adding-payment-methods)하거나 [used to update the default payment method](#updating-the-default-payment-method)하는 데 사용할 수 있습니다. 또한 결제 수단 식별자를 즉시 사용해 [create a new subscription](#creating-subscriptions)할 수도 있습니다.

> [!NOTE]
> Setup Intents와 고객 결제 세부 정보 수집에 대해 더 알고 싶다면 [review this overview provided by Stripe](https://stripe.com/docs/payments/save-and-reuse#php)를 검토하십시오.

<a name="payment-methods-for-single-charges"></a>
<!-- #### Payment Methods for Single Charges -->
#### Payment Methods for Single Charges

<!-- Of course, when making a single charge against a customer's payment method, we will only need to use a payment method identifier once. Due to Stripe limitations, you may not use the stored default payment method of a customer for single charges. You must allow the customer to enter their payment method details using the Stripe.js library. For example, consider the following form: -->
물론 고객의 결제 수단에 단일 결제를 청구할 때는 결제 수단 식별자를 한 번만 사용하면 됩니다. Stripe의 제한으로 인해, 단일 결제에는 고객의 저장된 기본 결제 수단을 사용할 수 없습니다. 고객이 Stripe.js 라이브러리를 사용해 결제 수단 세부 정보를 입력할 수 있도록 해야 합니다. 예를 들어 다음 폼을 살펴보십시오.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

<!-- After defining such a form, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
이러한 폼을 정의한 뒤에는 Stripe.js 라이브러리를 사용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 연결하고 고객의 결제 세부 정보를 안전하게 수집할 수 있습니다.

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
다음으로 카드를 검증하고 [Stripe's `createPaymentMethod` method](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method)를 사용해 Stripe에서 안전한 "결제 수단 식별자"를 조회할 수 있습니다.

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
카드가 성공적으로 검증되면 `paymentMethod.id`를 Laravel 애플리케이션으로 전달하고 [single charge](#simple-charge)를 처리할 수 있습니다.

<a name="retrieving-payment-methods"></a>
<!-- ### Retrieving Payment Methods -->
### Retrieving Payment Methods

<!-- The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances: -->
결제 가능 모델 인스턴스의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다.

```php
$paymentMethods = $user->paymentMethods();
```

<!-- By default, this method will return payment methods of every type. To retrieve payment methods of a specific type, you may pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 모든 유형의 결제 수단을 반환합니다. 특정 유형의 결제 수단을 조회하려면 `type`을 메서드의 인수로 전달할 수 있습니다.

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

<!-- To retrieve the customer's default payment method, the `defaultPaymentMethod` method may be used: -->
고객의 기본 결제 수단을 조회하려면 `defaultPaymentMethod` 메서드를 사용할 수 있습니다.

```php
$paymentMethod = $user->defaultPaymentMethod();
```

<!-- You can retrieve a specific payment method that is attached to the billable model using the `findPaymentMethod` method: -->
`findPaymentMethod` 메서드를 사용하면 결제 가능 모델에 연결된 특정 결제 수단을 조회할 수 있습니다.

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
<!-- ### Payment Method Presence -->
### Payment Method Presence

<!-- To determine if a billable model has a default payment method attached to their account, invoke the `hasDefaultPaymentMethod` method: -->
결제 가능 모델의 계정에 기본 결제 수단이 연결되어 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 호출합니다.

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

<!-- You may use the `hasPaymentMethod` method to determine if a billable model has at least one payment method attached to their account: -->
결제 가능 모델의 계정에 결제 수단이 하나 이상 연결되어 있는지 확인하려면 `hasPaymentMethod` 메서드를 사용할 수 있습니다.

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```

<!-- This method will determine if the billable model has any payment method at all. To determine if a payment method of a specific type exists for the model, you may pass the `type` as an argument to the method: -->
이 메서드는 결제 가능 모델에 결제 수단이 하나라도 있는지 확인합니다. 모델에 특정 유형의 결제 수단이 존재하는지 확인하려면 `type`을 메서드의 인수로 전달할 수 있습니다.

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```
<a name="updating-the-default-payment-method"></a>
<!-- ### Updating the Default Payment Method -->
### Updating the Default Payment Method

<!-- The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method: -->
`updateDefaultPaymentMethod` 메서드를 사용하여 고객의 기본 결제 수단 정보를 업데이트할 수 있습니다. 이 메서드는 Stripe 결제 수단 식별자를 받아 새 결제 수단을 기본 청구 결제 수단으로 지정합니다.

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

<!-- To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method: -->
기본 결제 수단 정보를 Stripe에 저장된 고객의 기본 결제 수단 정보와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용할 수 있습니다.

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 고객의 기본 결제 수단은 인보이스 발행과 새 구독 생성에만 사용할 수 있습니다. Stripe의 제한으로 인해 단건 결제에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
<!-- ### Adding Payment Methods -->
### Adding Payment Methods

<!-- To add a new payment method, you may call the `addPaymentMethod` method on the billable model, passing the payment method identifier: -->
새 결제 수단을 추가하려면 청구 가능 모델에서 `addPaymentMethod` 메서드를 호출하면서 결제 수단 식별자를 전달하면 됩니다.

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 식별자를 가져오는 방법을 알아보려면 [payment method storage documentation](#storing-payment-methods)를 확인하십시오.

<a name="deleting-payment-methods"></a>
<!-- ### Deleting Payment Methods -->
### Deleting Payment Methods

<!-- To delete a payment method, you may call the `delete` method on the `Laravel\Cashier\PaymentMethod` instance you wish to delete: -->
결제 수단을 삭제하려면 삭제하려는 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```php
$paymentMethod->delete();
```

<!-- The `deletePaymentMethod` method will delete a specific payment method from the billable model: -->
`deletePaymentMethod` 메서드는 청구 가능 모델에서 특정 결제 수단을 삭제합니다.

```php
$user->deletePaymentMethod('pm_visa');
```

<!-- The `deletePaymentMethods` method will delete all of the payment method information for the billable model: -->
`deletePaymentMethods` 메서드는 청구 가능 모델의 모든 결제 수단 정보를 삭제합니다.

```php
$user->deletePaymentMethods();
```

<!-- By default, this method will delete payment methods of every type. To delete payment methods of a specific type you can pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 모든 유형의 결제 수단을 삭제합니다. 특정 유형의 결제 수단을 삭제하려면 메서드에 `type`을 인수로 전달할 수 있습니다.

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 사용자에게 활성 구독이 있는 경우, 애플리케이션은 해당 사용자가 기본 결제 수단을 삭제하지 못하도록 해야 합니다.

<a name="subscriptions"></a>
<!-- ## Subscriptions -->
## Subscriptions

<!-- Subscriptions provide a way to set up recurring payments for your customers. Stripe subscriptions managed by Cashier provide support for multiple subscription prices, subscription quantities, trials, and more. -->
구독은 고객에게 반복 결제를 설정할 수 있는 방법을 제공합니다. Cashier가 관리하는 Stripe 구독은 여러 구독 가격, 구독 수량, 체험 기간 등을 지원합니다.

<a name="creating-subscriptions"></a>
<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription: -->
구독을 생성하려면 먼저 청구 가능 모델 인스턴스를 가져와야 하며, 일반적으로 이는 `App\Models\User` 인스턴스입니다. 모델 인스턴스를 가져온 뒤에는 `newSubscription` 메서드를 사용하여 모델의 구독을 생성할 수 있습니다.

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
`newSubscription` 메서드에 전달하는 첫 번째 인수는 구독의 내부 유형이어야 합니다. 애플리케이션에서 하나의 구독만 제공한다면 이를 `default` 또는 `primary`라고 부를 수 있습니다. 이 구독 유형은 애플리케이션 내부에서만 사용하기 위한 것이며 사용자에게 표시하기 위한 값이 아닙니다. 또한 공백을 포함해서는 안 되며, 구독을 생성한 뒤에는 절대 변경해서는 안 됩니다. 두 번째 인수는 사용자가 구독할 특정 가격입니다. 이 값은 Stripe의 가격 식별자와 일치해야 합니다.

<!-- The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information. -->
`create` 메서드는 [a Stripe payment method identifier](#storing-payment-methods) 또는 Stripe `PaymentMethod` 객체를 받으며, 구독을 시작하고 청구 가능 모델의 Stripe 고객 ID 및 기타 관련 청구 정보를 데이터베이스에 업데이트합니다.

> [!WARNING]
> 결제 수단 식별자를 `create` 구독 메서드에 직접 전달하면 해당 결제 수단이 사용자의 저장된 결제 수단에도 자동으로 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
<!-- #### Collecting Recurring Payments via Invoice Emails -->
#### Collecting Recurring Payments via Invoice Emails

<!-- Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices: -->
고객의 반복 결제를 자동으로 수집하는 대신, 반복 결제 기한이 될 때마다 Stripe가 고객에게 인보이스를 이메일로 보내도록 지시할 수 있습니다. 그러면 고객은 인보이스를 받은 뒤 직접 결제할 수 있습니다. 인보이스를 통해 반복 결제를 수집하는 경우 고객은 처음부터 결제 수단을 제공할 필요가 없습니다.

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

<!-- The amount of time a customer has to pay their invoice before their subscription is canceled is determined by the `days_until_due` option. By default, this is 30 days; however, you may provide a specific value for this option if you wish: -->
구독이 취소되기 전까지 고객이 인보이스를 결제할 수 있는 기간은 `days_until_due` 옵션으로 결정됩니다. 기본값은 30일입니다. 하지만 원한다면 이 옵션에 특정 값을 지정할 수 있습니다.

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
<!-- #### Quantities -->
#### Quantities

<!-- If you would like to set a specific [quantity](https://stripe.com/docs/billing/subscriptions/quantities) for the price when creating the subscription, you should invoke the `quantity` method on the subscription builder before creating the subscription: -->
구독을 생성할 때 가격에 특정 [quantity](https://stripe.com/docs/billing/subscriptions/quantities)을 설정하려면, 구독을 생성하기 전에 구독 빌더에서 `quantity` 메서드를 호출해야 합니다.

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional [customer](https://stripe.com/docs/api/customers/create) or [subscription](https://stripe.com/docs/api/subscriptions/create) options supported by Stripe, you may do so by passing them as the second and third arguments to the `create` method: -->
Stripe가 지원하는 추가 [customer](https://stripe.com/docs/api/customers/create) 또는 [subscription](https://stripe.com/docs/api/subscriptions/create) 옵션을 지정하려면, `create` 메서드의 두 번째 및 세 번째 인수로 전달하면 됩니다.

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
전달하는 프로모션 코드 ID는 고객에게 표시되는 프로모션 코드가 아니라, 프로모션 코드에 할당된 Stripe API ID여야 합니다. 고객에게 표시되는 프로모션 코드를 기준으로 프로모션 코드 ID를 찾아야 한다면 `findPromotionCode` 메서드를 사용할 수 있습니다.

```php
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

<!-- In the example above, the returned `$promotionCode` object is an instance of `Laravel\Cashier\PromotionCode`. This class decorates an underlying `Stripe\PromotionCode` object. You can retrieve the coupon related to the promotion code by invoking the `coupon` method: -->
위 예제에서 반환되는 `$promotionCode` 객체는 `Laravel\Cashier\PromotionCode`의 인스턴스입니다. 이 클래스는 내부의 `Stripe\PromotionCode` 객체를 감싸는 래퍼입니다. `coupon` 메서드를 호출하여 프로모션 코드와 관련된 쿠폰을 가져올 수 있습니다.

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

<!-- The coupon instance allows you to determine the discount amount and whether the coupon represents a fixed discount or percentage based discount: -->
쿠폰 인스턴스를 사용하면 할인 금액과 해당 쿠폰이 고정 금액 할인인지, 비율 기반 할인인지 확인할 수 있습니다.

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

<!-- You can also retrieve the discounts that are currently applied to a customer or subscription: -->
현재 고객 또는 구독에 적용된 할인도 가져올 수 있습니다.

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

<!-- The returned `Laravel\Cashier\Discount` instances decorate an underlying `Stripe\Discount` object instance. You may retrieve the coupon related to this discount by invoking the `coupon` method: -->
반환되는 `Laravel\Cashier\Discount` 인스턴스는 내부의 `Stripe\Discount` 객체 인스턴스를 감싸는 래퍼입니다. `coupon` 메서드를 호출하여 이 할인과 관련된 쿠폰을 가져올 수 있습니다.

```php
$coupon = $subscription->discount()->coupon();
```

<!-- If you would like to apply a new coupon or promotion code to a customer or subscription, you may do so via the `applyCoupon` or `applyPromotionCode` methods: -->
고객 또는 구독에 새 쿠폰이나 프로모션 코드를 적용하려면 `applyCoupon` 또는 `applyPromotionCode` 메서드를 사용할 수 있습니다.

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

<!-- Remember, you should use the Stripe API ID assigned to the promotion code and not the customer facing promotion code. Only one coupon or promotion code can be applied to a customer or subscription at a given time. -->
프로모션 코드에는 고객에게 표시되는 프로모션 코드가 아니라 Stripe API ID를 사용해야 한다는 점을 기억하십시오. 특정 시점에 고객 또는 구독에는 쿠폰이나 프로모션 코드 중 하나만 적용할 수 있습니다.

<!-- For more info on this subject, please consult the Stripe documentation regarding [coupons](https://stripe.com/docs/billing/subscriptions/coupons) and [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes). -->
이 주제에 대한 자세한 내용은 Stripe 문서의 [coupons](https://stripe.com/docs/billing/subscriptions/coupons) 및 [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes)를 참고하십시오.

<a name="adding-subscriptions"></a>
<!-- #### Adding Subscriptions -->
#### Adding Subscriptions

<!-- If you would like to add a subscription to a customer who already has a default payment method you may invoke the `add` method on the subscription builder: -->
이미 기본 결제 수단이 있는 고객에게 구독을 추가하려면 구독 빌더에서 `add` 메서드를 호출할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
<!-- #### Creating Subscriptions From the Stripe Dashboard -->
#### Creating Subscriptions From the Stripe Dashboard

<!-- You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a type of `default`. To customize the subscription type that is assigned to dashboard created subscriptions, [define webhook event handlers](#defining-webhook-event-handlers). -->
Stripe 대시보드 자체에서도 구독을 생성할 수 있습니다. 이 경우 Cashier는 새로 추가된 구독을 동기화하고 해당 구독에 `default` 유형을 할당합니다. 대시보드에서 생성된 구독에 할당되는 구독 유형을 사용자 지정하려면 [define webhook event handlers](#defining-webhook-event-handlers)하십시오.

<!-- In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different types, only one type of subscription may be added through the Stripe dashboard. -->
또한 Stripe 대시보드를 통해서는 한 가지 유형의 구독만 생성할 수 있습니다. 애플리케이션에서 서로 다른 유형을 사용하는 여러 구독을 제공하는 경우, Stripe 대시보드를 통해 추가할 수 있는 구독 유형은 하나뿐입니다.

<!-- Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If a customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database. -->
마지막으로, 애플리케이션에서 제공하는 각 구독 유형마다 활성 구독은 항상 하나만 추가되도록 해야 합니다. 고객에게 `default` 구독이 두 개 있는 경우, 두 구독이 모두 애플리케이션 데이터베이스와 동기화되더라도 Cashier는 가장 최근에 추가된 구독만 사용합니다.

<a name="checking-subscription-status"></a>
<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the type of the subscription as its first argument: -->
고객이 애플리케이션을 구독하면 여러 편리한 메서드를 사용하여 구독 상태를 쉽게 확인할 수 있습니다. 먼저 `subscribed` 메서드는 고객에게 활성 구독이 있으면 `true`를 반환하며, 구독이 현재 체험 기간 중이어도 마찬가지입니다. `subscribed` 메서드는 첫 번째 인수로 구독 유형을 받습니다.

```php
if ($user->subscribed('default')) {
    // ...
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/13.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` 메서드는 [route middleware](/docs/13.x/middleware)에서 사용하기에도 좋습니다. 이를 통해 사용자의 구독 상태에 따라 라우트와 컨트롤러 접근을 필터링할 수 있습니다.

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
사용자가 아직 체험 기간 중인지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이 메서드는 사용자에게 아직 체험 기간 중이라는 경고를 표시해야 하는지 판단할 때 유용합니다.

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

<!-- The `subscribedToProduct` method may be used to determine if the user is subscribed to a given product based on a given Stripe product's identifier. In Stripe, products are collections of prices. In this example, we will determine if the user's `default` subscription is actively subscribed to the application's "premium" product. The given Stripe product identifier should correspond to one of your product's identifiers in the Stripe dashboard: -->
`subscribedToProduct` 메서드는 주어진 Stripe 제품 식별자를 기준으로 사용자가 특정 제품을 구독 중인지 확인하는 데 사용할 수 있습니다. Stripe에서 제품은 가격들의 컬렉션입니다. 이 예제에서는 사용자의 `default` 구독이 애플리케이션의 "premium" 제품을 활성 구독 중인지 확인합니다. 전달하는 Stripe 제품 식별자는 Stripe 대시보드에 있는 제품 식별자 중 하나와 일치해야 합니다.

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

<!-- By passing an array to the `subscribedToProduct` method, you may determine if the user's `default` subscription is actively subscribed to the application's "basic" or "premium" product: -->
`subscribedToProduct` 메서드에 배열을 전달하면 사용자의 `default` 구독이 애플리케이션의 "basic" 또는 "premium" 제품을 활성 구독 중인지 확인할 수 있습니다.

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

<!-- The `subscribedToPrice` method may be used to determine if a customer's subscription corresponds to a given price ID: -->
`subscribedToPrice` 메서드는 고객의 구독이 특정 가격 ID에 해당하는지 확인하는 데 사용할 수 있습니다.

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
`recurring` 메서드는 사용자가 현재 구독 중이며 더 이상 체험 기간이 아닌지 확인하는 데 사용할 수 있습니다.

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> 사용자에게 같은 유형의 구독이 두 개 있는 경우, `subscription` 메서드는 항상 가장 최근 구독을 반환합니다. 예를 들어 사용자가 `default` 유형의 구독 레코드를 두 개 가지고 있을 수 있습니다. 하지만 하나는 오래되어 만료된 구독이고, 다른 하나는 현재 활성 구독일 수 있습니다. 가장 최근 구독이 항상 반환되며, 이전 구독은 이력 확인을 위해 데이터베이스에 보관됩니다.

<a name="cancelled-subscription-status"></a>
<!-- #### Canceled Subscription Status -->
#### Canceled Subscription Status

<!-- To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method: -->
사용자가 한때 활성 구독자였지만 구독을 취소했는지 확인하려면 `canceled` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

<!-- You may also determine if a user has canceled their subscription but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
사용자가 구독을 취소했지만 구독이 완전히 만료될 때까지 아직 "유예 기간"에 있는지도 확인할 수 있습니다. 예를 들어 사용자가 원래 3월 10일에 만료될 예정이었던 구독을 3월 5일에 취소했다면, 사용자는 3월 10일까지 "유예 기간"에 있는 것입니다. 이 기간 동안에도 `subscribed` 메서드는 여전히 `true`를 반환한다는 점에 유의하십시오.

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

<!-- To determine if the user has canceled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
사용자가 구독을 취소했고 더 이상 "유예 기간"에 있지 않은지 확인하려면 `ended` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
<!-- #### Incomplete and Past Due Status -->
#### Incomplete and Past Due Status

<!-- If a subscription requires a secondary payment action after creation the subscription will be marked as `incomplete`. Subscription statuses are stored in the `stripe_status` column of Cashier's `subscriptions` database table. -->
구독 생성 후 추가 결제 작업이 필요한 경우 해당 구독은 `incomplete`로 표시됩니다. 구독 상태는 Cashier의 `subscriptions` 데이터베이스 테이블에 있는 `stripe_status` 컬럼에 저장됩니다.

<!-- Similarly, if a secondary payment action is required when swapping prices the subscription will be marked as `past_due`. When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Determining if a subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
마찬가지로 가격을 변경할 때 추가 결제 작업이 필요한 경우 구독은 `past_due`로 표시됩니다. 구독이 이 두 상태 중 하나에 있으면 고객이 결제를 확인하기 전까지 활성 상태가 되지 않습니다. 구독에 미완료 결제가 있는지 확인하려면 청구 가능 모델 또는 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용할 수 있습니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

<!-- When a subscription has an incomplete payment, you should direct the user to Cashier's payment confirmation page, passing the `latestPayment` identifier. You may use the `latestPayment` method available on subscription instance to retrieve this identifier: -->
구독에 미완료 결제가 있는 경우 `latestPayment` 식별자를 전달하여 사용자를 Cashier의 결제 확인 페이지로 안내해야 합니다. 구독 인스턴스에서 사용할 수 있는 `latestPayment` 메서드를 사용하여 이 식별자를 가져올 수 있습니다.

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

<!-- If you would like the subscription to still be considered active when it's in a `past_due` or `incomplete` state, you may use the `keepPastDueSubscriptionsActive` and `keepIncompleteSubscriptionsActive` methods provided by Cashier. Typically, these methods should be called in the `register` method of your `App\Providers\AppServiceProvider`: -->
구독이 `past_due` 또는 `incomplete` 상태일 때도 활성 상태로 간주되게 하려면 Cashier가 제공하는 `keepPastDueSubscriptionsActive` 및 `keepIncompleteSubscriptionsActive` 메서드를 사용할 수 있습니다. 일반적으로 이러한 메서드는 `App\Providers\AppServiceProvider`의 `register` 메서드에서 호출해야 합니다.

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
> 구독이 `incomplete` 상태이면 결제가 확인될 때까지 변경할 수 없습니다. 따라서 구독이 `incomplete` 상태일 때 `swap` 및 `updateQuantity` 메서드를 호출하면 예외가 발생합니다.

<a name="subscription-scopes"></a>
<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
대부분의 구독 상태는 쿼리 스코프로도 제공되므로, 특정 상태에 있는 구독을 데이터베이스에서 쉽게 조회할 수 있습니다.

```php
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

<!-- A complete list of available scopes is available below: -->
사용 가능한 전체 스코프 목록은 다음과 같습니다.

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
고객이 애플리케이션에 구독한 후, 가끔 새로운 구독 가격으로 변경하고 싶어 할 수 있습니다. 고객을 새로운 가격으로 전환하려면 Stripe 가격의 식별자를 `swap` 메서드에 전달합니다. 가격을 전환할 때, 이전에 취소된 구독이라면 사용자가 해당 구독을 다시 활성화하려는 것으로 간주합니다. 전달하는 가격 식별자는 Stripe 대시보드에서 사용할 수 있는 Stripe 가격 식별자와 일치해야 합니다.

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

<!-- If the customer is on trial, the trial period will be maintained. Additionally, if a "quantity" exists for the subscription, that quantity will also be maintained. -->
고객이 평가판을 사용 중이라면 평가판 기간은 유지됩니다. 또한 구독에 "수량"이 있다면 해당 수량도 유지됩니다.

<!-- If you would like to swap prices and cancel any trial period the customer is currently on, you may invoke the `skipTrial` method: -->
가격을 전환하면서 고객이 현재 사용 중인 평가판 기간을 취소하고 싶다면 `skipTrial` 메서드를 호출할 수 있습니다.

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

<!-- If you would like to swap prices and immediately invoice the customer instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
가격을 전환하고 다음 청구 주기까지 기다리지 않고 고객에게 즉시 청구서를 발행하고 싶다면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
<!-- #### Prorations -->
#### Prorations

<!-- By default, Stripe prorates charges when swapping between prices. The `noProrate` method may be used to update the subscription's price without prorating the charges: -->
기본적으로 Stripe는 가격을 전환할 때 요금을 일할 계산합니다. `noProrate` 메서드를 사용하면 요금을 일할 계산하지 않고 구독의 가격을 업데이트할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

<!-- For more information on subscription proration, consult the [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations). -->
구독 일할 계산에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations)를 참고하십시오.

> [!WARNING]
> `swapAndInvoice` 메서드 전에 `noProrate` 메서드를 실행해도 일할 계산에는 영향을 주지 않습니다. 청구서는 항상 발행됩니다.

<a name="subscription-quantity"></a>
<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. You may use the `incrementQuantity` and `decrementQuantity` methods to easily increment or decrement your subscription quantity: -->
때로는 구독이 "수량"의 영향을 받습니다. 예를 들어 프로젝트 관리 애플리케이션은 프로젝트당 월 $10를 청구할 수 있습니다. `incrementQuantity`와 `decrementQuantity` 메서드를 사용하면 구독 수량을 쉽게 증가시키거나 감소시킬 수 있습니다.

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
또는 `updateQuantity` 메서드를 사용하여 특정 수량을 설정할 수 있습니다.

```php
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
`noProrate` 메서드를 사용하면 요금을 일할 계산하지 않고 구독 수량을 업데이트할 수 있습니다.

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<!-- For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities). -->
구독 수량에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/subscriptions/quantities)를 참고하십시오.

<a name="quantities-for-subscription-with-multiple-products"></a>
<!-- #### Quantities for Subscriptions With Multiple Products -->
#### Quantities for Subscriptions With Multiple Products

<!-- If your subscription is a [subscription with multiple products](#subscriptions-with-multiple-products), you should pass the ID of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods: -->
구독이 [subscription with multiple products](#subscriptions-with-multiple-products)이라면, 증가 / 감소 메서드의 두 번째 인수로 수량을 증가시키거나 감소시키려는 가격의 ID를 전달해야 합니다.

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
<!-- ### Subscriptions With Multiple Products -->
### Subscriptions With Multiple Products

<!-- [Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products) allow you to assign multiple billing products to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on product for an additional $15 per month. Information for subscriptions with multiple products is stored in Cashier's `subscription_items` database table. -->
[Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products)을 사용하면 여러 청구 제품을 하나의 구독에 할당할 수 있습니다. 예를 들어 월 $10의 기본 구독 가격이 있지만, 월 $15가 추가되는 라이브 채팅 애드온 제품을 제공하는 고객 서비스 "helpdesk" 애플리케이션을 만든다고 가정해 보겠습니다. 여러 제품이 포함된 구독 정보는 Cashier의 `subscription_items` 데이터베이스 테이블에 저장됩니다.

<!-- You may specify multiple products for a given subscription by passing an array of prices as the second argument to the `newSubscription` method: -->
`newSubscription` 메서드의 두 번째 인수로 가격 배열을 전달하여 특정 구독에 여러 제품을 지정할 수 있습니다.

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
위 예제에서 고객은 자신의 `default` 구독에 두 개의 가격을 연결하게 됩니다. 두 가격은 각각의 청구 주기에 따라 청구됩니다. 필요한 경우 `quantity` 메서드를 사용하여 각 가격에 대한 특정 수량을 지정할 수 있습니다.

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

<!-- If you would like to add another price to an existing subscription, you may invoke the subscription's `addPrice` method: -->
기존 구독에 다른 가격을 추가하고 싶다면 구독의 `addPrice` 메서드를 호출할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

<!-- The example above will add the new price and the customer will be billed for it on their next billing cycle. If you would like to bill the customer immediately you may use the `addPriceAndInvoice` method: -->
위 예제는 새 가격을 추가하며, 고객은 다음 청구 주기에 해당 가격에 대해 청구됩니다. 고객에게 즉시 청구하고 싶다면 `addPriceAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

<!-- If you would like to add a price with a specific quantity, you can pass the quantity as the second argument of the `addPrice` or `addPriceAndInvoice` methods: -->
특정 수량과 함께 가격을 추가하고 싶다면 `addPrice` 또는 `addPriceAndInvoice` 메서드의 두 번째 인수로 수량을 전달할 수 있습니다.

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
> 구독의 마지막 가격은 제거할 수 없습니다. 대신 구독을 취소해야 합니다.

<a name="swapping-prices"></a>
<!-- #### Swapping Prices -->
#### Swapping Prices

<!-- You may also change the prices attached to a subscription with multiple products. For example, imagine a customer has a `price_basic` subscription with a `price_chat` add-on product and you want to upgrade the customer from the `price_basic` to the `price_pro` price: -->
여러 제품이 포함된 구독에 연결된 가격도 변경할 수 있습니다. 예를 들어 고객에게 `price_chat` 애드온 제품이 포함된 `price_basic` 구독이 있고, 고객을 `price_basic`에서 `price_pro` 가격으로 업그레이드하려는 상황을 가정해 보겠습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

<!-- When executing the example above, the underlying subscription item with the `price_basic` is deleted and the one with the `price_chat` is preserved. Additionally, a new subscription item for the `price_pro` is created. -->
위 예제를 실행하면 `price_basic`이 있는 내부 구독 항목은 삭제되고, `price_chat`이 있는 항목은 유지됩니다. 또한 `price_pro`에 대한 새 구독 항목이 생성됩니다.

<!-- You can also specify subscription item options by passing an array of key / value pairs to the `swap` method. For example, you may need to specify the subscription price quantities: -->
`swap` 메서드에 키 / 값 쌍의 배열을 전달하여 구독 항목 옵션을 지정할 수도 있습니다. 예를 들어 구독 가격 수량을 지정해야 할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

<!-- If you want to swap a single price on a subscription, you may do so using the `swap` method on the subscription item itself. This approach is particularly useful if you would like to preserve all of the existing metadata on the subscription's other prices: -->
구독에서 단일 가격만 전환하고 싶다면 구독 항목 자체의 `swap` 메서드를 사용하여 처리할 수 있습니다. 이 방식은 구독의 다른 가격에 있는 기존 메타데이터를 모두 유지하고 싶을 때 특히 유용합니다.

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
기본적으로 Stripe는 여러 제품이 포함된 구독에서 가격을 추가하거나 제거할 때 요금을 일할 계산합니다. 일할 계산 없이 가격을 조정하고 싶다면 가격 작업에 `noProrate` 메서드를 체이닝해야 합니다.

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
<!-- #### Quantities -->
#### Quantities

<!-- If you would like to update quantities on individual subscription prices, you may do so using the [existing quantity methods](#subscription-quantity) by passing the ID of the price as an additional argument to the method: -->
개별 구독 가격의 수량을 업데이트하고 싶다면 메서드에 추가 인수로 가격 ID를 전달하여 [existing quantity methods](#subscription-quantity)를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 구독에 여러 가격이 있는 경우 `Subscription` 모델의 `stripe_price`와 `quantity` 속성은 `null`이 됩니다. 개별 가격 속성에 접근하려면 `Subscription` 모델에서 사용할 수 있는 `items` 연관관계를 사용해야 합니다.

<a name="subscription-items"></a>
<!-- #### Subscription Items -->
#### Subscription Items

<!-- When a subscription has multiple prices, it will have multiple subscription "items" stored in your database's `subscription_items` table. You may access these via the `items` relationship on the subscription: -->
구독에 여러 가격이 있는 경우, 데이터베이스의 `subscription_items` 테이블에 저장되는 여러 구독 "항목"이 생깁니다. 구독의 `items` 연관관계를 통해 이 항목에 접근할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

<!-- You can also retrieve a specific price using the `findItemOrFail` method: -->
`findItemOrFail` 메서드를 사용하여 특정 가격을 조회할 수도 있습니다.

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
<!-- ### Multiple Subscriptions -->
### Multiple Subscriptions

<!-- Stripe allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans. -->
Stripe는 고객이 동시에 여러 구독을 가질 수 있도록 허용합니다. 예를 들어 수영 구독과 웨이트 트레이닝 구독을 제공하는 헬스장을 운영할 수 있으며, 각 구독은 서로 다른 가격을 가질 수 있습니다. 물론 고객은 둘 중 하나 또는 두 플랜 모두에 구독할 수 있어야 합니다.

<!-- When your application creates subscriptions, you may provide the type of the subscription to the `newSubscription` method. The type may be any string that represents the type of subscription the user is initiating: -->
애플리케이션이 구독을 생성할 때 `newSubscription` 메서드에 구독 유형을 제공할 수 있습니다. 유형은 사용자가 시작하는 구독의 종류를 나타내는 임의의 문자열일 수 있습니다.

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
이 예제에서는 고객에 대해 월간 수영 구독을 시작했습니다. 하지만 나중에 연간 구독으로 전환하고 싶어 할 수 있습니다. 고객의 구독을 조정할 때는 `swimming` 구독의 가격을 전환하기만 하면 됩니다.

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
[Usage based billing](https://stripe.com/docs/billing/subscriptions/metered-billing)을 사용하면 청구 주기 동안 고객의 제품 사용량을 기준으로 요금을 청구할 수 있습니다. 예를 들어 고객이 한 달 동안 보낸 문자 메시지나 이메일 수를 기준으로 요금을 청구할 수 있습니다.

<!-- To start using usage billing, you will first need to create a new product in your Stripe dashboard with a [usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) and a [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter). After creating the meter, store the associated event name and meter ID, which you will need to report and retrieve usage. Then, use the `meteredPrice` method to add the metered price ID to a customer subscription: -->
사용량 과금을 시작하려면 먼저 Stripe 대시보드에서 [usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide)과 [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter)가 있는 새 제품을 생성해야 합니다. 미터를 생성한 후에는 사용량을 보고하고 조회하는 데 필요한 관련 이벤트 이름과 미터 ID를 저장합니다. 그런 다음 `meteredPrice` 메서드를 사용하여 고객 구독에 미터링 가격 ID를 추가합니다.

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
[Stripe Checkout](#checkout)을 통해 미터링 구독을 시작할 수도 있습니다.

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
고객이 애플리케이션을 사용하는 동안, 정확히 청구될 수 있도록 고객의 사용량을 Stripe에 보고해야 합니다. 미터링 이벤트의 사용량을 보고하려면 `Billable` 모델에서 `reportMeterEvent` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

<!-- By default, a "usage quantity" of 1 is added to the billing period. Alternatively, you may pass a specific amount of "usage" to add to the customer's usage for the billing period: -->
기본적으로 청구 기간에 "사용량 수량" 1이 추가됩니다. 또는 청구 기간 동안 고객의 사용량에 추가할 특정 "사용량" 값을 전달할 수 있습니다.

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

<!-- To retrieve a customer's event summary for a meter, you may use a `Billable` instance's `meterEventSummaries` method: -->
고객의 특정 미터에 대한 이벤트 요약을 조회하려면 `Billable` 인스턴스의 `meterEventSummaries` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

<!-- Please refer to Stripe's [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object) for more information on meter event summaries. -->
미터 이벤트 요약에 대한 자세한 내용은 Stripe의 [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object)를 참고하십시오.

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
사용자가 구독에 대해 지불하는 세율을 지정하려면 결제 가능 모델에 `taxRates` 메서드를 구현하고 Stripe 세율 ID가 포함된 배열을 반환해야 합니다. 이러한 세율은 [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates)에서 정의할 수 있습니다.

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
`taxRates` 메서드를 사용하면 고객별로 세율을 적용할 수 있습니다. 이는 여러 국가와 세율에 걸쳐 있는 사용자 기반을 가진 경우 유용할 수 있습니다.

<!-- If you're offering subscriptions with multiple products, you may define different tax rates for each price by implementing a `priceTaxRates` method on your billable model: -->
여러 제품이 포함된 구독을 제공한다면 결제 가능 모델에 `priceTaxRates` 메서드를 구현하여 각 가격에 대해 서로 다른 세율을 정의할 수 있습니다.

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
> `taxRates` 메서드는 구독 요금에만 적용됩니다. Cashier를 사용하여 "일회성" 요금을 청구하는 경우, 해당 시점에 세율을 수동으로 지정해야 합니다.

<a name="syncing-tax-rates"></a>
<!-- #### Syncing Tax Rates -->
#### Syncing Tax Rates

<!-- When changing the hard-coded tax rate IDs returned by the `taxRates` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the new `taxRates` values, you should call the `syncTaxRates` method on the user's subscription instance: -->
`taxRates` 메서드가 반환하는 하드 코딩된 세율 ID를 변경해도, 해당 사용자의 기존 구독에 적용된 세금 설정은 그대로 유지됩니다. 기존 구독의 세금 값을 새로운 `taxRates` 값으로 업데이트하고 싶다면 사용자의 구독 인스턴스에서 `syncTaxRates` 메서드를 호출해야 합니다.

```php
$user->subscription('default')->syncTaxRates();
```

<!-- This will also sync any item tax rates for a subscription with multiple products. If your application is offering subscriptions with multiple products, you should ensure that your billable model implements the `priceTaxRates` method [discussed above](#subscription-taxes). -->
이 작업은 여러 제품이 포함된 구독의 항목 세율도 함께 동기화합니다. 애플리케이션이 여러 제품이 포함된 구독을 제공한다면, 결제 가능 모델이 [discussed above](#subscription-taxes) `priceTaxRates` 메서드를 구현하고 있는지 확인해야 합니다.

<a name="tax-exemption"></a>
<!-- #### Tax Exemption -->
#### Tax Exemption

<!-- Cashier also offers the `isNotTaxExempt`, `isTaxExempt`, and `reverseChargeApplies` methods to determine if the customer is tax exempt. These methods will call the Stripe API to determine a customer's tax exemption status: -->
Cashier는 고객이 세금 면제 대상인지 확인하기 위해 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드도 제공합니다. 이 메서드들은 Stripe API를 호출하여 고객의 세금 면제 상태를 확인합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```
> [!WARNING]
> 이 메서드들은 모든 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있습니다. 다만 `Invoice` 객체에서 호출하면, 해당 메서드들은 청구서가 생성된 시점의 면제 상태를 판단합니다.

<a name="subscription-anchor-date"></a>
<!-- ### Subscription Anchor Date -->
### Subscription Anchor Date

<!-- By default, the billing cycle anchor is the date the subscription was created or, if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method: -->
기본적으로 결제 주기 기준일은 구독이 생성된 날짜이거나, 평가판 기간을 사용하는 경우 평가판이 종료되는 날짜입니다. 결제 기준일을 변경하려면 `anchorBillingCycleOn` 메서드를 사용할 수 있습니다.

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
구독 결제 주기 관리에 대한 자세한 내용은 [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하십시오.

<a name="cancelling-subscriptions"></a>
<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
구독을 취소하려면 사용자의 구독에서 `cancel` 메서드를 호출하십시오.

```php
$user->subscription('default')->cancel();
```

<!-- When a subscription is canceled, Cashier will automatically set the `ends_at` column in your `subscriptions` database table. This column is used to know when the `subscribed` method should begin returning `false`. -->
구독이 취소되면 Cashier는 `subscriptions` 데이터베이스 테이블의 `ends_at` 컬럼을 자동으로 설정합니다. 이 컬럼은 `subscribed` 메서드가 언제부터 `false`를 반환해야 하는지 판단하는 데 사용됩니다.

<!-- For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
예를 들어 고객이 3월 1일에 구독을 취소했지만 구독 종료 예정일이 3월 5일이라면, `subscribed` 메서드는 3월 5일까지 계속 `true`를 반환합니다. 일반적으로 사용자는 결제 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있어야 하기 때문입니다.

<!-- You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
사용자가 구독을 취소했지만 아직 "유예 기간" 안에 있는지 확인하려면 `onGracePeriod` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

<!-- If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription: -->
구독을 즉시 취소하려면 사용자의 구독에서 `cancelNow` 메서드를 호출하십시오.

```php
$user->subscription('default')->cancelNow();
```

<!-- If you wish to cancel a subscription immediately and invoice any remaining un-invoiced metered usage or new / pending proration invoice items, call the `cancelNowAndInvoice` method on the user's subscription: -->
구독을 즉시 취소하면서 아직 청구되지 않은 남은 종량제 사용량이나 새로 생성된/대기 중인 비례 배분 청구서 항목도 함께 청구하려면 사용자의 구독에서 `cancelNowAndInvoice` 메서드를 호출하십시오.

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
마지막으로, 관련 사용자 모델을 삭제하기 전에는 항상 사용자 구독을 먼저 취소해야 합니다.

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
<!-- ### Resuming Subscriptions -->
### Resuming Subscriptions

<!-- If a customer has canceled their subscription and you wish to resume it, you may invoke the `resume` method on the subscription. The customer must still be within their "grace period" in order to resume a subscription: -->
고객이 구독을 취소했지만 이를 다시 재개하려면 구독에서 `resume` 메서드를 호출할 수 있습니다. 구독을 재개하려면 고객이 아직 "유예 기간" 안에 있어야 합니다.

```php
$user->subscription('default')->resume();
```

<!-- If the customer cancels a subscription and then resumes that subscription before the subscription has fully expired the customer will not be billed immediately. Instead, their subscription will be re-activated and they will be billed on the original billing cycle. -->
고객이 구독을 취소한 뒤 구독이 완전히 만료되기 전에 다시 재개하면 즉시 청구되지 않습니다. 대신 구독이 다시 활성화되고, 기존 결제 주기에 맞춰 청구됩니다.

<a name="subscription-trials"></a>
<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>
<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions: -->
고객에게 평가판 기간을 제공하면서도 결제 수단 정보를 미리 수집하려면, 구독을 생성할 때 `trialDays` 메서드를 사용해야 합니다.

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
이 메서드는 데이터베이스의 구독 레코드에 평가판 종료일을 설정하고, 해당 날짜가 지나기 전까지 고객에게 청구를 시작하지 않도록 Stripe에 지시합니다. `trialDays` 메서드를 사용하면 Cashier는 Stripe에서 해당 가격에 설정된 기본 평가판 기간을 덮어씁니다.

> [!WARNING]
> 고객의 구독이 평가판 종료일 전에 취소되지 않으면 평가판이 만료되는 즉시 요금이 청구됩니다. 따라서 사용자에게 평가판 종료일을 반드시 알려야 합니다.

<!-- The `trialUntil` method allows you to provide a `DateTime` instance that specifies when the trial period should end: -->
`trialUntil` 메서드를 사용하면 평가판 기간이 언제 종료되어야 하는지 지정하는 `DateTime` 인스턴스를 제공할 수 있습니다.

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->plus(days: 10))
    ->create($paymentMethod);
```

<!-- You may determine if a user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
사용자가 평가판 기간 안에 있는지 확인하려면 사용자 인스턴스의 `onTrial` 메서드나 구독 인스턴스의 `onTrial` 메서드를 사용할 수 있습니다. 아래 두 예제는 동일합니다.

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

<!-- You may use the `endTrial` method to immediately end a subscription trial: -->
구독 평가판을 즉시 종료하려면 `endTrial` 메서드를 사용할 수 있습니다.

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
Stripe 대시보드에서 가격에 적용될 평가판 일수를 정의하거나, Cashier를 사용할 때 항상 명시적으로 전달하도록 선택할 수 있습니다. Stripe에서 가격의 평가판 일수를 정의하는 경우, 과거에 구독한 적이 있는 고객의 새 구독을 포함하여 새 구독은 `skipTrial()` 메서드를 명시적으로 호출하지 않는 한 항상 평가판 기간을 받는다는 점에 유의해야 합니다.

<a name="without-payment-method-up-front"></a>
<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration: -->
사용자의 결제 수단 정보를 미리 수집하지 않고 평가판 기간을 제공하려면, 사용자 레코드의 `trial_ends_at` 컬럼을 원하는 평가판 종료일로 설정할 수 있습니다. 일반적으로 이 작업은 사용자 등록 중에 수행됩니다.

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->plus(days: 10),
]);
```

> [!WARNING]
> 청구 가능 모델 클래스 정의 안에서 `trial_ends_at` 속성에 대한 [date cast](/docs/13.x/eloquent-mutators#date-casting)를 반드시 추가하십시오.

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the billable model instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
Cashier는 이 유형의 평가판을 "일반 평가판"이라고 부릅니다. 기존 구독에 연결되어 있지 않기 때문입니다. 현재 날짜가 `trial_ends_at` 값보다 지나지 않았다면 청구 가능 모델 인스턴스의 `onTrial` 메서드는 `true`를 반환합니다.

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
사용자에 대한 실제 구독을 생성할 준비가 되면 평소처럼 `newSubscription` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription type parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
사용자의 평가판 종료일을 가져오려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 평가판 중이면 Carbon 날짜 인스턴스를 반환하고, 그렇지 않으면 `null`을 반환합니다. 기본 구독이 아닌 특정 구독의 평가판 종료일을 가져오려면 선택적으로 구독 유형 파라미터를 전달할 수도 있습니다.

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not yet created an actual subscription: -->
사용자가 "일반" 평가판 기간 안에 있으며 아직 실제 구독을 생성하지 않았는지 구체적으로 알고 싶다면 `onGenericTrial` 메서드를 사용할 수도 있습니다.

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>
<!-- ### Extending Trials -->
### Extending Trials

<!-- The `extendTrial` method allows you to extend the trial period of a subscription after the subscription has been created. If the trial has already expired and the customer is already being billed for the subscription, you can still offer them an extended trial. The time spent within the trial period will be deducted from the customer's next invoice: -->
`extendTrial` 메서드를 사용하면 구독이 생성된 후 구독의 평가판 기간을 연장할 수 있습니다. 평가판이 이미 만료되어 고객에게 구독 요금이 청구되고 있더라도, 여전히 연장된 평가판을 제공할 수 있습니다. 평가판 기간으로 사용한 시간은 고객의 다음 청구서에서 차감됩니다.

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
> 로컬 개발 중 webhook을 테스트하는 데 [the Stripe CLI](https://stripe.com/docs/stripe-cli)를 사용할 수 있습니다.

<!-- Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Stripe는 webhook을 통해 다양한 이벤트를 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier 서비스 프로바이더는 Cashier의 webhook 컨트롤러를 가리키는 라우트를 자동으로 등록합니다. 이 컨트롤러는 들어오는 모든 webhook 요청을 처리합니다.

<!-- By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like. -->
기본적으로 Cashier webhook 컨트롤러는 실패한 청구가 너무 많은 구독의 취소(Stripe 설정에 따라 정의됨), 고객 업데이트, 고객 삭제, 구독 업데이트, 결제 수단 변경을 자동으로 처리합니다. 하지만 곧 살펴보겠지만, 이 컨트롤러를 확장하여 원하는 Stripe webhook 이벤트를 처리할 수 있습니다.

<!-- To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are: -->
애플리케이션이 Stripe webhook을 처리할 수 있도록 하려면 Stripe 제어판에서 webhook URL을 설정해야 합니다. 기본적으로 Cashier의 webhook 컨트롤러는 `/stripe/webhook` URL 경로에 응답합니다. Stripe 제어판에서 활성화해야 하는 모든 webhook 목록은 다음과 같습니다.

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
편의를 위해 Cashier는 `cashier:webhook` Artisan 명령어를 포함합니다. 이 명령어는 Cashier에 필요한 모든 이벤트를 수신하는 webhook을 Stripe에 생성합니다.

```shell
php artisan cashier:webhook
```

<!-- By default, the created webhook will point to the URL defined by the `APP_URL` environment variable and the `cashier.webhook` route that is included with Cashier. You may provide the `--url` option when invoking the command if you would like to use a different URL: -->
기본적으로 생성된 webhook은 `APP_URL` 환경 변수로 정의된 URL과 Cashier에 포함된 `cashier.webhook` 라우트를 가리킵니다. 다른 URL을 사용하려면 명령어를 호출할 때 `--url` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

<!-- The webhook that is created will use the Stripe API version that your version of Cashier is compatible with. If you would like to use a different Stripe version, you may provide the `--api-version` option: -->
생성되는 webhook은 사용 중인 Cashier 버전과 호환되는 Stripe API 버전을 사용합니다. 다른 Stripe 버전을 사용하려면 `--api-version` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

<!-- After creation, the webhook will be immediately active. If you wish to create the webhook but have it disabled until you're ready, you may provide the `--disabled` option when invoking the command: -->
생성 후 webhook은 즉시 활성화됩니다. webhook을 생성하되 준비될 때까지 비활성화 상태로 두고 싶다면 명령어를 호출할 때 `--disabled` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> 들어오는 Stripe webhook 요청은 Cashier에 포함된 [webhook signature verification](#verifying-webhook-signatures) Middleware로 반드시 보호하십시오.

<a name="webhooks-csrf-protection"></a>
<!-- #### Webhooks and CSRF Protection -->
#### Webhooks and CSRF Protection

<!-- Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/13.x/csrf), you should ensure that Laravel does not attempt to validate the CSRF token for incoming Stripe webhooks. To accomplish this, you should exclude `stripe/*` from CSRF protection in your application's `bootstrap/app.php` file: -->
Stripe webhook은 Laravel의 [CSRF protection](/docs/13.x/csrf)를 우회해야 하므로, 들어오는 Stripe webhook에 대해 Laravel이 CSRF 토큰 검증을 시도하지 않도록 해야 합니다. 이를 위해 애플리케이션의 `bootstrap/app.php` 파일에서 CSRF 보호 대상에서 `stripe/*`를 제외해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancellations for failed charges and other common Stripe webhook events. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier는 실패한 청구로 인한 구독 취소와 그 밖의 일반적인 Stripe webhook 이벤트를 자동으로 처리합니다. 하지만 추가로 처리하고 싶은 webhook 이벤트가 있다면, Cashier가 디스패치하는 다음 이벤트를 수신하여 처리할 수 있습니다.

<!--
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`
-->
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

<!-- Both events contain the full payload of the Stripe webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/13.x/events#defining-listeners) that will handle the event: -->
두 이벤트 모두 Stripe webhook의 전체 페이로드를 포함합니다. 예를 들어 `invoice.payment_succeeded` webhook을 처리하려면 해당 이벤트를 처리할 [listener](/docs/13.x/events#defining-listeners)를 등록할 수 있습니다.

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
webhook을 보호하려면 [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures)을 사용할 수 있습니다. 편의를 위해 Cashier는 들어오는 Stripe webhook 요청이 유효한지 검증하는 Middleware를 자동으로 포함합니다.

<!-- To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is set in your application's `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard. -->
webhook 검증을 활성화하려면 애플리케이션의 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경 변수가 설정되어 있는지 확인하십시오. webhook `secret`은 Stripe 계정 대시보드에서 가져올 수 있습니다.

<a name="single-charges"></a>
<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>
<!-- ### Simple Charge -->
### Simple Charge

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance. You will need to [provide a payment method identifier](#payment-methods-for-single-charges) as the second argument to the `charge` method: -->
고객에게 일회성 청구를 하려면 청구 가능 모델 인스턴스에서 `charge` 메서드를 사용할 수 있습니다. `charge` 메서드의 두 번째 인수로 [provide a payment method identifier](#payment-methods-for-single-charges)를 제공해야 합니다.

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
`charge` 메서드는 세 번째 인수로 배열을 받습니다. 이를 통해 내부 Stripe 청구 생성 과정에 원하는 옵션을 전달할 수 있습니다. 청구를 생성할 때 사용할 수 있는 옵션에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/api/charges/create)에서 확인할 수 있습니다.

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

<!-- You may also use the `charge` method without an underlying customer or user. To accomplish this, invoke the `charge` method on a new instance of your application's billable model: -->
내부 고객이나 사용자 없이도 `charge` 메서드를 사용할 수 있습니다. 이를 위해 애플리케이션의 청구 가능 모델 새 인스턴스에서 `charge` 메서드를 호출하십시오.

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

<!-- The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method: -->
청구에 실패하면 `charge` 메서드는 예외를 던집니다. 청구가 성공하면 메서드에서 `Laravel\Cashier\Payment` 인스턴스가 반환됩니다.

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]
> `charge` 메서드는 애플리케이션에서 사용하는 통화의 최소 단위로 결제 금액을 받습니다. 예를 들어 고객이 미국 달러로 결제한다면 금액은 센트 단위로 지정해야 합니다.

<a name="charge-with-invoice"></a>
<!-- ### Charge With Invoice -->
### Charge With Invoice

<!-- Sometimes you may need to make a one-time charge and offer a PDF invoice to your customer. The `invoicePrice` method lets you do just that. For example, let's invoice a customer for five new shirts: -->
때로는 일회성 청구를 하면서 고객에게 PDF 청구서를 제공해야 할 수 있습니다. `invoicePrice` 메서드는 바로 이 작업을 할 수 있게 해줍니다. 예를 들어 고객에게 새 티셔츠 다섯 장에 대한 청구서를 발행해 보겠습니다.

```php
$user->invoicePrice('price_tshirt', 5);
```

<!-- The invoice will be immediately charged against the user's default payment method. The `invoicePrice` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array which should contain the billing options for the invoice itself: -->
청구서는 사용자의 기본 결제 수단으로 즉시 청구됩니다. `invoicePrice` 메서드는 세 번째 인수로 배열도 받습니다. 이 배열에는 청구서 항목의 결제 옵션이 들어갑니다. 이 메서드가 받는 네 번째 인수 역시 배열이며, 청구서 자체의 결제 옵션을 포함해야 합니다.

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
`invoicePrice`와 비슷하게 `tabPrice` 메서드를 사용하면 여러 항목을 고객의 "탭"에 추가한 뒤 고객에게 청구서를 발행하여 일회성 청구를 생성할 수 있습니다(청구서당 최대 250개 항목). 예를 들어 고객에게 셔츠 다섯 장과 머그컵 두 개에 대한 청구서를 발행할 수 있습니다.

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```
<!-- Alternatively, you may use the `invoiceFor` method to make a "one-off" charge against the customer's default payment method: -->
또는 `invoiceFor` 메서드를 사용하여 고객의 기본 결제 수단에 "일회성" 청구를 할 수 있습니다.

```php
$user->invoiceFor('One Time Fee', 500);
```

<!-- Although the `invoiceFor` method is available for you to use, it is recommended that you use the `invoicePrice` and `tabPrice` methods with pre-defined prices. By doing so, you will have access to better analytics and data within your Stripe dashboard regarding your sales on a per-product basis. -->
`invoiceFor` 메서드를 사용할 수는 있지만, 미리 정의된 가격과 함께 `invoicePrice` 및 `tabPrice` 메서드를 사용하는 것을 권장합니다. 이렇게 하면 제품별 판매와 관련해 Stripe 대시보드에서 더 나은 분석과 데이터를 확인할 수 있습니다.

> [!WARNING]
> `invoice`, `invoicePrice`, `invoiceFor` 메서드는 Stripe 청구서를 생성하며, 실패한 결제 시도를 다시 시도합니다. 청구서가 실패한 청구를 다시 시도하지 않게 하려면, 첫 번째 청구 실패 후 Stripe API를 사용하여 해당 청구서를 종료해야 합니다.

<a name="creating-payment-intents"></a>
<!-- ### Creating Payment Intents -->
### Creating Payment Intents

<!-- You can create a new Stripe payment intent by invoking the `pay` method on a billable model instance. Calling this method will create a payment intent that is wrapped in a `Laravel\Cashier\Payment` instance: -->
청구 가능한 모델 인스턴스에서 `pay` 메서드를 호출하여 새 Stripe 결제 의도를 생성할 수 있습니다. 이 메서드를 호출하면 `Laravel\Cashier\Payment` 인스턴스로 감싼 결제 의도가 생성됩니다.

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
결제 의도를 생성한 후에는 애플리케이션의 프런트엔드로 클라이언트 시크릿을 반환하여 사용자가 브라우저에서 결제를 완료할 수 있게 할 수 있습니다. Stripe 결제 의도를 사용하여 전체 결제 흐름을 구축하는 방법을 더 자세히 알아보려면 [Stripe documentation](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참고하십시오.

<!-- When using the `pay` method, the default payment methods that are enabled within your Stripe dashboard will be available to the customer. Alternatively, if you only want to allow for some specific payment methods to be used, you may use the `payWith` method: -->
`pay` 메서드를 사용할 때는 Stripe 대시보드에서 활성화된 기본 결제 수단이 고객에게 제공됩니다. 또는 특정 결제 수단만 사용할 수 있도록 허용하려면 `payWith` 메서드를 사용할 수 있습니다.

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
> `pay` 및 `payWith` 메서드는 애플리케이션에서 사용하는 통화의 가장 작은 단위로 결제 금액을 받습니다. 예를 들어 고객이 미국 달러로 결제한다면, 금액은 센트 단위로 지정해야 합니다.

<a name="refunding-charges"></a>
<!-- ### Refunding Charges -->
### Refunding Charges

<!-- If you need to refund a Stripe charge, you may use the `refund` method. This method accepts the Stripe [payment intent ID](#payment-methods-for-single-charges) as its first argument: -->
Stripe 청구를 환불해야 하는 경우 `refund` 메서드를 사용할 수 있습니다. 이 메서드는 Stripe [payment intent ID](#payment-methods-for-single-charges)를 첫 번째 인수로 받습니다.

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
`invoices` 메서드를 사용하면 청구 가능한 모델의 청구서 배열을 쉽게 조회할 수 있습니다. `invoices` 메서드는 `Laravel\Cashier\Invoice` 인스턴스의 컬렉션을 반환합니다.

```php
$invoices = $user->invoices();
```

<!-- If you would like to include pending invoices in the results, you may use the `invoicesIncludingPending` method: -->
결과에 보류 중인 청구서도 포함하려면 `invoicesIncludingPending` 메서드를 사용할 수 있습니다.

```php
$invoices = $user->invoicesIncludingPending();
```

<!-- You may use the `findInvoice` method to retrieve a specific invoice by its ID: -->
특정 청구서를 ID로 조회하려면 `findInvoice` 메서드를 사용할 수 있습니다.

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
<!-- #### Displaying Invoice Information -->
#### Displaying Invoice Information

<!-- When listing the invoices for the customer, you may use the invoice's methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them: -->
고객의 청구서를 나열할 때는 청구서의 메서드를 사용하여 관련 청구서 정보를 표시할 수 있습니다. 예를 들어 모든 청구서를 테이블로 나열하여 사용자가 원하는 청구서를 쉽게 다운로드할 수 있게 할 수 있습니다.

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
고객의 예정 청구서를 조회하려면 `upcomingInvoice` 메서드를 사용할 수 있습니다.

```php
$invoice = $user->upcomingInvoice();
```

<!-- Similarly, if the customer has multiple subscriptions, you can also retrieve the upcoming invoice for a specific subscription: -->
마찬가지로 고객에게 여러 구독이 있다면 특정 구독의 예정 청구서도 조회할 수 있습니다.

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
<!-- ### Previewing Subscription Invoices -->
### Previewing Subscription Invoices

<!-- Using the `previewInvoice` method, you can preview an invoice before making price changes. This will allow you to determine what your customer's invoice will look like when a given price change is made: -->
`previewInvoice` 메서드를 사용하면 가격을 변경하기 전에 청구서를 미리 볼 수 있습니다. 이를 통해 특정 가격 변경이 적용되었을 때 고객의 청구서가 어떻게 보일지 확인할 수 있습니다.

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

<!-- You may pass an array of prices to the `previewInvoice` method in order to preview invoices with multiple new prices: -->
여러 새 가격이 적용된 청구서를 미리 보려면 `previewInvoice` 메서드에 가격 배열을 전달할 수 있습니다.

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
<!-- ### Generating Invoice PDFs -->
### Generating Invoice PDFs

<!-- Before generating invoice PDFs, you should use Composer to install the Dompdf library, which is the default invoice renderer for Cashier: -->
청구서 PDF를 생성하기 전에 Composer를 사용하여 Cashier의 기본 청구서 렌더러인 Dompdf 라이브러리를 설치해야 합니다.

```shell
composer require dompdf/dompdf
```

<!-- From within a route or controller, you may use the `downloadInvoice` method to generate a PDF download of a given invoice. This method will automatically generate the proper HTTP response needed to download the invoice: -->
라우트나 컨트롤러 안에서 `downloadInvoice` 메서드를 사용하여 지정된 청구서의 PDF 다운로드를 생성할 수 있습니다. 이 메서드는 청구서 다운로드에 필요한 적절한 HTTP 응답을 자동으로 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

<!-- By default, all data on the invoice is derived from the customer and invoice data stored in Stripe. The filename is based on your `app.name` config value. However, you can customize some of this data by providing an array as the second argument to the `downloadInvoice` method. This array allows you to customize information such as your company and product details: -->
기본적으로 청구서의 모든 데이터는 Stripe에 저장된 고객 및 청구서 데이터에서 가져옵니다. 파일명은 `app.name` 설정 값을 기반으로 합니다. 하지만 `downloadInvoice` 메서드의 두 번째 인수로 배열을 제공하여 이 데이터의 일부를 사용자 지정할 수 있습니다. 이 배열을 사용하면 회사 및 제품 세부 정보와 같은 정보를 사용자 지정할 수 있습니다.

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
`downloadInvoice` 메서드는 세 번째 인수를 통해 사용자 지정 파일명도 허용합니다. 이 파일명에는 자동으로 `.pdf`가 접미사로 붙습니다.

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
<!-- #### Custom Invoice Renderer -->
#### Custom Invoice Renderer

<!-- Cashier also makes it possible to use a custom invoice renderer. By default, Cashier uses the `DompdfInvoiceRenderer` implementation, which utilizes the [dompdf](https://github.com/dompdf/dompdf) PHP library to generate Cashier's invoices. However, you may use any renderer you wish by implementing the `Laravel\Cashier\Contracts\InvoiceRenderer` interface. For example, you may wish to render an invoice PDF using an API call to a third-party PDF rendering service: -->
Cashier는 사용자 지정 청구서 렌더러를 사용할 수도 있게 해줍니다. 기본적으로 Cashier는 [dompdf](https://github.com/dompdf/dompdf) PHP 라이브러리를 사용하여 Cashier의 청구서를 생성하는 `DompdfInvoiceRenderer` 구현을 사용합니다. 하지만 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현하면 원하는 어떤 렌더러든 사용할 수 있습니다. 예를 들어 서드파티 PDF 렌더링 서비스에 API 호출을 보내 청구서 PDF를 렌더링할 수 있습니다.

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
청구서 렌더러 계약을 구현한 후에는 애플리케이션의 `config/cashier.php` 설정 파일에서 `cashier.invoices.renderer` 설정 값을 업데이트해야 합니다. 이 설정 값은 사용자 지정 렌더러 구현의 클래스 이름으로 설정해야 합니다.

<a name="checkout"></a>
<!-- ## Checkout -->
## Checkout

<!-- Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page. -->
Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout)도 지원합니다. Stripe Checkout은 미리 구축되어 호스팅되는 결제 페이지를 제공하여, 결제를 받기 위한 사용자 지정 페이지를 직접 구현해야 하는 부담을 덜어줍니다.

<!-- The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout). -->
다음 문서에는 Cashier와 함께 Stripe Checkout을 시작하는 방법에 대한 정보가 담겨 있습니다. Stripe Checkout에 대해 더 자세히 알아보려면 [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout)도 함께 확인해 보십시오.

<a name="product-checkouts"></a>
<!-- ### Product Checkouts -->
### Product Checkouts

<!-- You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID: -->
청구 가능한 모델에서 `checkout` 메서드를 사용하면 Stripe 대시보드 안에 생성되어 있는 기존 제품에 대해 Checkout을 수행할 수 있습니다. `checkout` 메서드는 새 Stripe Checkout 세션을 시작합니다. 기본적으로 Stripe Price ID를 전달해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

<!-- If needed, you may also specify a product quantity: -->
필요하다면 제품 수량도 지정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

<!-- When a customer visits this route they will be redirected to Stripe's Checkout page. By default, when a user successfully completes or cancels a purchase they will be redirected to your `home` route location, but you may specify custom callback URLs using the `success_url` and `cancel_url` options: -->
고객이 이 라우트에 방문하면 Stripe의 Checkout 페이지로 리디렉션됩니다. 기본적으로 사용자가 구매를 성공적으로 완료하거나 취소하면 `home` 라우트 위치로 리디렉션되지만, `success_url` 및 `cancel_url` 옵션을 사용하여 사용자 지정 콜백 URL을 지정할 수 있습니다.

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
`success_url` Checkout 옵션을 정의할 때 Stripe가 URL을 호출할 때 Checkout 세션 ID를 쿼리 문자열 파라미터로 추가하도록 지시할 수 있습니다. 이렇게 하려면 `success_url` 쿼리 문자열에 리터럴 문자열 `{CHECKOUT_SESSION_ID}`를 추가하십시오. Stripe는 이 플레이스홀더를 실제 Checkout 세션 ID로 대체합니다.

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
기본적으로 Stripe Checkout은 [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 허용하지 않습니다. 다행히 Checkout 페이지에서 이를 쉽게 활성화할 수 있는 방법이 있습니다. 이를 위해 `allowPromotionCodes` 메서드를 호출할 수 있습니다.

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
Stripe 대시보드에 생성되지 않은 임시 제품에 대해 간단한 청구도 수행할 수 있습니다. 이를 위해 청구 가능한 모델에서 `checkoutCharge` 메서드를 사용하고, 청구 금액, 제품명, 선택적인 수량을 전달할 수 있습니다. 고객이 이 라우트에 방문하면 Stripe의 Checkout 페이지로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` 메서드를 사용할 때 Stripe는 항상 Stripe 대시보드에 새 제품과 가격을 생성합니다. 따라서 Stripe 대시보드에서 제품을 미리 생성한 뒤 `checkout` 메서드를 사용하는 것을 권장합니다.

<a name="subscription-checkouts"></a>
<!-- ### Subscription Checkouts -->
### Subscription Checkouts

> [!WARNING]
> 구독에 Stripe Checkout을 사용하려면 Stripe 대시보드에서 `customer.subscription.created` webhook을 활성화해야 합니다. 이 webhook은 데이터베이스에 구독 레코드를 생성하고 관련 구독 항목을 모두 저장합니다.

<!-- You may also use Stripe Checkout to initiate subscriptions. After defining your subscription with Cashier's subscription builder methods, you may call the `checkout `method. When a customer visits this route they will be redirected to Stripe's Checkout page: -->
Stripe Checkout을 사용하여 구독을 시작할 수도 있습니다. Cashier의 구독 빌더 메서드로 구독을 정의한 후 `checkout `메서드를 호출할 수 있습니다. 고객이 이 라우트에 방문하면 Stripe의 Checkout 페이지로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

<!-- Just as with product checkouts, you may customize the success and cancellation URLs: -->
제품 Checkout과 마찬가지로 성공 및 취소 URL을 사용자 지정할 수 있습니다.

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
물론 구독 Checkout에서도 프로모션 코드를 활성화할 수 있습니다.

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
> 안타깝게도 Stripe Checkout은 구독을 시작할 때 모든 구독 청구 옵션을 지원하지 않습니다. 구독 빌더에서 `anchorBillingCycleOn` 메서드를 사용하거나, 일할 계산 동작을 설정하거나, 결제 동작을 설정해도 Stripe Checkout 세션 중에는 아무 효과가 없습니다. 사용할 수 있는 파라미터를 확인하려면 [the Stripe Checkout Session API documentation](https://stripe.com/docs/api/checkout/sessions/create)를 참고하십시오.

<a name="stripe-checkout-trial-periods"></a>
<!-- #### Stripe Checkout and Trial Periods -->
#### Stripe Checkout and Trial Periods

<!-- Of course, you can define a trial period when building a subscription that will be completed using Stripe Checkout: -->
물론 Stripe Checkout으로 완료될 구독을 만들 때 체험 기간을 정의할 수 있습니다.

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<!-- However, the trial period must be at least 48 hours, which is the minimum amount of trial time supported by Stripe Checkout. -->
하지만 체험 기간은 Stripe Checkout에서 지원하는 최소 체험 시간인 48시간 이상이어야 합니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
<!-- #### Subscriptions and Webhooks -->
#### Subscriptions and Webhooks

<!-- Remember, Stripe and Cashier update subscription statuses via webhooks, so there's a possibility a subscription might not yet be active when the customer returns to the application after entering their payment information. To handle this scenario, you may wish to display a message informing the user that their payment or subscription is pending. -->
Stripe와 Cashier는 webhook을 통해 구독 상태를 업데이트한다는 점을 기억하십시오. 따라서 고객이 결제 정보를 입력한 뒤 애플리케이션으로 돌아왔을 때 구독이 아직 활성 상태가 아닐 수 있습니다. 이 상황을 처리하려면 사용자에게 결제 또는 구독이 대기 중임을 알리는 메시지를 표시하는 것이 좋습니다.

<a name="collecting-tax-ids"></a>
<!-- ### Collecting Tax IDs -->
### Collecting Tax IDs

<!-- Checkout also supports collecting a customer's Tax ID. To enable this on a checkout session, invoke the `collectTaxIds` method when creating the session: -->
Checkout은 고객의 Tax ID 수집도 지원합니다. Checkout 세션에서 이를 활성화하려면 세션을 생성할 때 `collectTaxIds` 메서드를 호출하십시오.

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

<!-- When this method is invoked, a new checkbox will be available to the customer that allows them to indicate if they're purchasing as a company. If so, they will have the opportunity to provide their Tax ID number. -->
이 메서드가 호출되면 고객에게 회사로 구매하는지 표시할 수 있는 새 체크박스가 제공됩니다. 회사로 구매하는 경우 Tax ID 번호를 입력할 수 있습니다.

> [!WARNING]
> 애플리케이션의 서비스 프로바이더에서 이미 [automatic tax collection](#tax-configuration)를 설정했다면 이 기능은 자동으로 활성화되며 `collectTaxIds` 메서드를 호출할 필요가 없습니다.

<a name="guest-checkouts"></a>
<!-- ### Guest Checkouts -->
### Guest Checkouts

<!-- Using the `Checkout::guest` method, you may initiate checkout sessions for guests of your application that do not have an "account": -->
`Checkout::guest` 메서드를 사용하면 "계정"이 없는 애플리케이션의 게스트를 위한 Checkout 세션을 시작할 수 있습니다.

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
기존 사용자를 위한 Checkout 세션을 생성할 때와 마찬가지로, `Laravel\Cashier\CheckoutBuilder` 인스턴스에서 사용할 수 있는 추가 메서드를 활용하여 게스트 Checkout 세션을 사용자 지정할 수 있습니다.

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
게스트 체크아웃이 완료되면 Stripe는 `checkout.session.completed` 웹훅 이벤트를 디스패치할 수 있으므로, 이 이벤트가 실제로 애플리케이션으로 전송되도록 [configure your Stripe webhook](https://dashboard.stripe.com/webhooks)해야 합니다. Stripe 대시보드에서 웹훅을 활성화한 뒤에는 [handle the webhook with Cashier](#handling-stripe-webhooks)할 수 있습니다. 웹훅 페이로드에 포함된 객체는 [checkout object](https://stripe.com/docs/api/checkout/sessions/object)이며, 고객의 주문을 처리하기 위해 이 객체를 확인할 수 있습니다.

<a name="handling-failed-payments"></a>
<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed. -->
구독 또는 단일 청구의 결제가 실패하는 경우가 있습니다. 이 경우 Cashier는 이런 상황이 발생했음을 알려주는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이 예외를 잡은 뒤에는 두 가지 방식으로 진행할 수 있습니다.

<!-- First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page: -->
첫 번째로, 고객을 Cashier에 포함된 전용 결제 확인 페이지로 리다이렉트할 수 있습니다. 이 페이지에는 Cashier의 서비스 프로바이더를 통해 등록되는 이름이 지정된 라우트가 이미 연결되어 있습니다. 따라서 `IncompletePayment` 예외를 잡아 사용자를 결제 확인 페이지로 리다이렉트할 수 있습니다.

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
결제 확인 페이지에서 고객은 신용카드 정보를 다시 입력하고, "3D Secure" 확인처럼 Stripe에서 요구하는 추가 작업을 수행하라는 안내를 받습니다. 결제를 확인한 뒤 사용자는 위에서 지정한 `redirect` 파라미터가 제공한 URL로 리다이렉트됩니다. 리다이렉트될 때 `message`(문자열)와 `success`(정수) 쿼리 문자열 변수가 URL에 추가됩니다. 현재 결제 페이지는 다음 결제 수단 유형을 지원합니다.

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
- Alipay
- Bancontact
- BECS 자동 이체
- EPS
- Giropay
- iDEAL
- SEPA 자동 이체

<!-- </div> -->
</div>

<!-- Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions. -->
또는 Stripe가 결제 확인을 대신 처리하도록 할 수도 있습니다. 이 경우 결제 확인 페이지로 리다이렉트하는 대신 Stripe 대시보드에서 [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic)할 수 있습니다. 하지만 `IncompletePayment` 예외가 잡힌 경우에는 추가 결제 확인 안내가 포함된 이메일을 받게 된다는 사실을 사용자에게 알려야 합니다.

<!-- Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions. -->
결제 예외는 `Billable` trait을 사용하는 모델의 `charge`, `invoiceFor`, `invoice` 메서드에서 발생할 수 있습니다. 구독과 상호작용할 때는 `SubscriptionBuilder`의 `create` 메서드와 `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice`, `swapAndInvoice` 메서드가 불완전한 결제 예외를 발생시킬 수 있습니다.

<!-- Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
기존 구독에 불완전한 결제가 있는지 확인하려면 billable 모델 또는 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용할 수 있습니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

<!-- You can derive the specific status of an incomplete payment by inspecting the `payment` property on the exception instance: -->
예외 인스턴스의 `payment` 속성을 확인하면 불완전한 결제의 구체적인 상태를 알 수 있습니다.

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
일부 결제 수단은 결제를 확인하기 위해 추가 데이터가 필요합니다. 예를 들어 SEPA 결제 수단은 결제 과정에서 추가 "mandate" 데이터가 필요합니다. `withPaymentConfirmationOptions` 메서드를 사용하여 이 데이터를 Cashier에 제공할 수 있습니다.

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

<!-- You may consult the [Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm) to review all of the options accepted when confirming payments. -->
결제를 확인할 때 허용되는 모든 옵션을 검토하려면 [Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm)를 참고할 수 있습니다.

<a name="strong-customer-authentication"></a>
<!-- ## Strong Customer Authentication -->
## Strong Customer Authentication

<!-- If your business or one of your customers is based in Europe you will need to abide by the EU's Strong Customer Authentication (SCA) regulations. These regulations were imposed in September 2019 by the European Union to prevent payment fraud. Luckily, Stripe and Cashier are prepared for building SCA compliant applications. -->
비즈니스 또는 고객 중 한 명이 유럽에 기반을 두고 있다면 EU의 Strong Customer Authentication(SCA) 규정을 준수해야 합니다. 이 규정은 결제 사기를 방지하기 위해 유럽연합이 2019년 9월에 도입했습니다. 다행히 Stripe와 Cashier는 SCA를 준수하는 애플리케이션을 구축할 준비가 되어 있습니다.

> [!WARNING]
> 시작하기 전에 [Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication)와 [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication)를 검토하십시오.

<a name="payments-requiring-additional-confirmation"></a>
<!-- ### Payments Requiring Additional Confirmation -->
### Payments Requiring Additional Confirmation

<!-- SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions can be found in the documentation on [handling failed payments](#handling-failed-payments). -->
SCA 규정은 결제를 확인하고 처리하기 위해 추가 검증을 요구하는 경우가 많습니다. 이 경우 Cashier는 추가 검증이 필요하다는 사실을 알려주는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이러한 예외를 처리하는 방법에 대한 자세한 내용은 [handling failed payments](#handling-failed-payments) 문서에서 확인할 수 있습니다.

<!-- Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
Stripe 또는 Cashier가 표시하는 결제 확인 화면은 특정 은행 또는 카드 발급사의 결제 흐름에 맞게 조정될 수 있으며, 추가 카드 확인, 임시 소액 청구, 별도 기기 인증 또는 다른 형태의 검증을 포함할 수 있습니다.

<a name="incomplete-and-past-due-state"></a>
<!-- #### Incomplete and Past Due State -->
#### Incomplete and Past Due State

<!-- When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion. -->
결제에 추가 확인이 필요한 경우 구독은 `stripe_status` 데이터베이스 컬럼에 표시되는 것처럼 `incomplete` 또는 `past_due` 상태로 유지됩니다. 결제 확인이 완료되고 애플리케이션이 Stripe로부터 웹훅을 통해 완료 알림을 받으면 Cashier는 고객의 구독을 자동으로 활성화합니다.

<!-- For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status). -->
`incomplete` 및 `past_due` 상태에 대한 자세한 내용은 [our additional documentation on these states](#incomplete-and-past-due-status)를 참고하십시오.

<a name="off-session-payment-notifications"></a>
<!-- ### Off-Session Payment Notifications -->
### Off-Session Payment Notifications

<!-- Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to a notification class. By default, this notification is disabled. Of course, Cashier includes a notification class you may use for this purpose, but you are free to provide your own notification class if desired: -->
SCA 규정에서는 구독이 활성 상태인 동안에도 고객이 결제 세부 정보를 가끔 검증해야 하므로, 오프 세션 결제 확인이 필요할 때 Cashier가 고객에게 알림을 보낼 수 있습니다. 예를 들어 구독이 갱신될 때 이런 상황이 발생할 수 있습니다. Cashier의 결제 알림은 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수를 알림 클래스로 설정하여 활성화할 수 있습니다. 기본적으로 이 알림은 비활성화되어 있습니다. 물론 Cashier에는 이 용도로 사용할 수 있는 알림 클래스가 포함되어 있지만, 원한다면 직접 만든 알림 클래스를 제공할 수도 있습니다.

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

<!-- To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait. -->
오프 세션 결제 확인 알림이 전달되도록 하려면 애플리케이션에 [Stripe webhooks are configured](#handling-stripe-webhooks)되어 있고 Stripe 대시보드에서 `invoice.payment_action_required` 웹훅이 활성화되어 있는지 확인하십시오. 또한 `Billable` 모델은 Laravel의 `Illuminate\Notifications\Notifiable` trait도 사용해야 합니다.

> [!WARNING]
> 고객이 추가 확인이 필요한 결제를 수동으로 진행하는 경우에도 알림이 전송됩니다. 안타깝게도 Stripe는 결제가 수동으로 이루어졌는지 또는 "오프 세션"으로 이루어졌는지 알 수 없습니다. 하지만 고객이 이미 결제를 확인한 뒤 결제 페이지를 방문하면 단순히 "Payment Successful" 메시지를 보게 됩니다. 고객이 실수로 같은 결제를 두 번 확인하여 의도치 않은 두 번째 청구가 발생하는 일은 허용되지 않습니다.

<a name="stripe-sdk"></a>
<!-- ## Stripe SDK -->
## Stripe SDK

<!-- Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method: -->
Cashier의 많은 객체는 Stripe SDK 객체를 감싸는 래퍼입니다. Stripe 객체와 직접 상호작용하고 싶다면 `asStripe` 메서드를 사용하여 편리하게 가져올 수 있습니다.

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
`Stripe\StripeClient` 클라이언트를 직접 사용하고 싶다면 `Cashier` 클래스에서 `stripe` 메서드를 호출할 수 있습니다. 예를 들어 이 메서드를 사용하여 `StripeClient` 인스턴스에 접근하고 Stripe 계정의 가격 목록을 가져올 수 있습니다.

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- When testing an application that uses Cashier, you may mock the actual HTTP requests to the Stripe API; however, this requires you to partially re-implement Cashier's own behavior. Therefore, we recommend allowing your tests to hit the actual Stripe API. While this is slower, it provides more confidence that your application is working as expected and any slow tests may be placed within their own Pest / PHPUnit testing group. -->
Cashier를 사용하는 애플리케이션을 테스트할 때 Stripe API로 보내는 실제 HTTP 요청을 모킹할 수 있습니다. 하지만 이렇게 하려면 Cashier 자체 동작의 일부를 다시 구현해야 합니다. 따라서 테스트가 실제 Stripe API에 요청을 보내도록 허용하는 것을 권장합니다. 이 방식은 더 느리지만, 애플리케이션이 예상대로 동작한다는 확신을 더 많이 제공하며 느린 테스트는 별도의 Pest / PHPUnit 테스트 그룹에 배치할 수 있습니다.

<!-- When testing, remember that Cashier itself already has a great test suite, so you should only focus on testing the subscription and payment flow of your own application and not every underlying Cashier behavior. -->
테스트할 때는 Cashier 자체에 이미 훌륭한 테스트 스위트가 있다는 점을 기억하십시오. 따라서 내부 Cashier 동작을 모두 테스트하기보다는, 여러분의 애플리케이션에서 사용하는 구독 및 결제 흐름 테스트에만 집중해야 합니다.

<!-- To get started, add the **testing** version of your Stripe secret to your `phpunit.xml` file: -->
시작하려면 Stripe secret의 **테스트용** 버전을 `phpunit.xml` 파일에 추가하십시오.

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

<!-- Now, whenever you interact with Cashier while testing, it will send actual API requests to your Stripe testing environment. For convenience, you should pre-fill your Stripe testing account with subscriptions / prices that you may use during testing. -->
이제 테스트 중 Cashier와 상호작용할 때마다 실제 API 요청이 Stripe 테스트 환경으로 전송됩니다. 편의를 위해 테스트 중 사용할 수 있는 구독 / 가격 정보를 Stripe 테스트 계정에 미리 채워 두는 것이 좋습니다.

> [!NOTE]
> 신용카드 거절 및 실패와 같은 다양한 청구 시나리오를 테스트하려면 Stripe가 제공하는 다양한 [testing card numbers and tokens](https://stripe.com/docs/testing)을 사용할 수 있습니다.
