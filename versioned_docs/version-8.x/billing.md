<!-- # Laravel Cashier (Stripe) -->
# Laravel Cashier (Stripe)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
    - [Database Migrations](#database-migrations)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Currency Configuration](#currency-configuration)
    - [Tax Configuration](#tax-configuration)
    - [Logging](#logging)
    - [Using Custom Models](#using-custom-models)
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
    - [Determining If A User Has A Payment Method](#check-for-a-payment-method)
    - [Updating The Default Payment Method](#updating-the-default-payment-method)
    - [Adding Payment Methods](#adding-payment-methods)
    - [Deleting Payment Methods](#deleting-payment-methods)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Changing Prices](#changing-prices)
    - [Subscription Quantity](#subscription-quantity)
    - [Multiprice Subscriptions](#multiprice-subscriptions)
    - [Metered Billing](#metered-billing)
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
    - [Refunding Charges](#refunding-charges)
- [Checkout](#checkout)
    - [Product Checkouts](#product-checkouts)
    - [Single Charge Checkouts](#single-charge-checkouts)
    - [Subscription Checkouts](#subscription-checkouts)
    - [Collecting Tax IDs](#collecting-tax-ids)
- [Invoices](#invoices)
    - [Retrieving Invoices](#retrieving-invoices)
    - [Upcoming Invoices](#upcoming-invoices)
    - [Previewing Subscription Invoices](#previewing-subscription-invoices)
    - [Generating Invoice PDFs](#generating-invoice-pdfs)
- [Handling Failed Payments](#handling-failed-payments)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [Payments Requiring Additional Confirmation](#payments-requiring-additional-confirmation)
    - [Off-session Payment Notifications](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [Testing](#testing)

<a name="introduction"></a>

<!-- ## Introduction -->
## Introduction

<!-- [Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe) provides an expressive, fluent interface to [Stripe's](https://stripe.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs. -->
[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe's](https://stripe.com)의 구독 청구 서비스와 쉽게 연동할 수 있도록 직관적이고 유연한 인터페이스를 제공합니다. Cashier는 반복적으로 작성해야 하는 구독 청구 관련 코드 대부분을 대신 처리해줍니다. 구독 기본 관리 기능 외에도, Cashier는 쿠폰 적용, 구독 교체, 구독 수량(quantity) 관리, 취소 유예 기간, 인보이스 PDF 생성까지 폭넓게 지원합니다.

<a name="upgrading-cashier"></a>

<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md). -->
Cashier를 새 버전으로 업그레이드할 때는 [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼭 꼼꼼히 확인하시기 바랍니다.

> [!NOTE]
> Cashier는 장애를 유발하는 변경을 막기 위해 Stripe API 버전을 고정해서 사용합니다. Cashier 13 버전은 Stripe API 버전 `2020-08-27`을 활용합니다. Stripe API 버전은 Stripe의 새로운 기능과 개선 사항을 활용하기 위해 마이너 릴리스에서 업데이트될 수 있습니다.

<a name="installation"></a>

<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Stripe using the Composer package manager: -->
먼저, Composer 패키지 매니저를 사용하여 Stripe용 Cashier 패키지를 설치합니다.

```
composer require laravel/cashier
```

> [!NOTE]
> Cashier가 Stripe의 모든 이벤트를 정상적으로 처리하려면 반드시 [set up Cashier's webhook handling](#handling-stripe-webhooks)을 설정해야 합니다.

<a name="database-migrations"></a>

<!-- ### Database Migrations -->
### Database Migrations

<!-- Cashier's service provider registers its own database migration directory, so remember to migrate your database after installing the package. The Cashier migrations will add several columns to your `users` table as well as create a new `subscriptions` table to hold all of your customer's subscriptions: -->
Cashier의 서비스 프로바이더는 자체 데이터베이스 마이그레이션 디렉터리를 등록합니다. 따라서 패키지 설치 후에는 데이터베이스 마이그레이션을 꼭 실행해야 합니다. Cashier 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하고, 모든 고객 구독 정보를 담는 새로운 `subscriptions` 테이블도 생성합니다.

```
php artisan migrate
```

<!-- If you need to overwrite the migrations that ship with Cashier, you can publish them using the `vendor:publish` Artisan command: -->
Cashier에서 제공하는 마이그레이션 파일을 수정하거나 덮어쓰고 싶다면, `vendor:publish` 아티즌 명령어로 마이그레이션 파일을 퍼블리시할 수 있습니다.

```
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- If you would like to prevent Cashier's migrations from running entirely, you may use the `ignoreMigrations` method provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
Cashier의 마이그레이션 자체를 완전히 비활성화하고 싶다면, Cashier에서 제공하는 `ignoreMigrations` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 `AppServiceProvider`의 `register` 메서드에서 호출하는 것이 좋습니다.

```
use Laravel\Cashier\Cashier;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    Cashier::ignoreMigrations();
}
```

> [!NOTE]
> Stripe는 Stripe 식별자를 저장하는 컬럼은 대소문자를 구분하도록 설정할 것을 권장합니다. 따라서 MySQL을 사용할 경우 `stripe_id` 컬럼의 collation을 `utf8_bin`으로 설정해야 합니다. 이에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인할 수 있습니다.

<a name="configuration"></a>

<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>

<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, add the `Billable` trait to your billable model definition. Typically, this will be the `App\Models\User` model. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information: -->
Cashier를 사용하기 전에, 청구가 가능한 모델에 `Billable` 트레이트를 추가해야 합니다. 보통은 `App\Models\User` 모델에 이 트레이트를 추가합니다. 이 트레이트를 통해 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 다양한 청구 관련 메서드를 사용할 수 있습니다.

```
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- Cashier assumes your billable model will be the `App\Models\User` class that ships with Laravel. If you wish to change this you may specify a different model via the `useCustomerModel` method. This method should typically be called in the `boot` method of your `AppServiceProvider` class: -->
Cashier는 기본적으로 Laravel에서 제공하는 `App\Models\User` 클래스를 청구 모델로 사용한다고 가정합니다. 만약 이를 변경하고 싶다면, `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Cashier::useCustomerModel(User::class);
}
```

> [!NOTE]
> Laravel에서 기본 제공하는 `App\Models\User` 모델이 아닌 다른 모델을 사용한다면, 반드시 [Cashier migrations](#installation)을 퍼블리시해서 해당 모델의 테이블명에 맞게 수정해야 합니다.

<a name="api-keys"></a>

<!-- ### API Keys -->
### API Keys

<!-- Next, you should configure your Stripe API keys in your application's `.env` file. You can retrieve your Stripe API keys from the Stripe control panel: -->
다음으로, Stripe API 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Stripe API 키는 Stripe 관리 패널에서 확인할 수 있습니다.

```
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
```

<a name="currency-configuration"></a>

<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
Cashier의 기본 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정해 통화를 변경할 수 있습니다.

```
CASHIER_CURRENCY=eur
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
Cashier의 통화를 설정하는 것 외에도, 인보이스에 금액을 표시할 때 사용할 로케일(locale)도 지정할 수 있습니다. Cashier는 내부적으로 [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php)를 이용해 금액 표시용 로케일을 지정합니다.

```
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!NOTE]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 설정되어 있어야 합니다.

<a name="tax-configuration"></a>

<!-- ### Tax Configuration -->
### Tax Configuration

<!-- Thanks to [Stripe Tax](https://stripe.com/tax), it's possible to automatically calculate taxes for all invoices generated by Stripe. You can enable automatic tax calculation by invoking the `calculateTaxes` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
[Stripe Tax](https://stripe.com/tax) 덕분에 Stripe에서 생성된 모든 인보이스에 대해 자동으로 세금을 계산할 수 있습니다. 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하면 자동 세금 계산이 활성화됩니다.

```
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Cashier::calculateTaxes();
}
```

<!-- Once tax calculation has been enabled, any new subscriptions and any one-off invoices that are generated will receive automatic tax calculation. -->
세금 계산 기능이 활성화되면, 새롭게 생성되는 모든 구독과 1회성 인보이스에 대해 자동으로 세금이 계산됩니다.

<!-- For this feature to work properly, your customer's billing details, such as the customer's name, address, and tax ID, need to be synced to Stripe. You may use the [customer data synchronization](#syncing-customer-data-with-stripe) and [Tax ID](#tax-ids) methods offered by Cashier to accomplish this. -->
이 기능이 제대로 작동하려면 고객의 이름, 주소, 세금 ID와 같은 청구 정보가 Stripe에 동기화되어야 합니다. 이를 위해 Cashier에서 제공하는 [customer data synchronization](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 메서드를 활용할 수 있습니다.

> [!NOTE]
> 아직까지는 [single charges](#single-charges) 또는 [single charge checkouts](#single-charge-checkouts)에는 세금이 계산되지 않습니다. 또한 Stripe Tax는 현재 베타 기간('invite-only')이므로, [Stripe Tax website](https://stripe.com/tax#request-access)에서 액세스를 신청할 수 있습니다.

<a name="logging"></a>

<!-- ### Logging -->
### Logging

<!-- Cashier allows you to specify the log channel to be used when logging fatal Stripe errors. You may specify the log channel by defining the `CASHIER_LOGGER` environment variable within your application's `.env` file: -->
Cashier를 사용하면 Stripe의 치명적 오류가 발생할 때 사용할 로그 채널을 지정할 수 있습니다. 애플리케이션 `.env` 파일에 `CASHIER_LOGGER` 환경 변수를 정의해 로그 채널을 선택할 수 있습니다.

```
CASHIER_LOGGER=stack
```

<!-- Exceptions that are generated by API calls to Stripe will be logged through your application's default log channel. -->
Stripe로의 API 호출에서 발생하는 예외(Exception)는 앱의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>

<!-- ### Using Custom Models -->
### Using Custom Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
Cashier가 내부적으로 사용하는 모델을 확장하고 싶다면, 직접 만든 모델이 Cashier 모델을 상속받도록 구현하면 됩니다.

```
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Cashier\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
모델을 정의한 뒤에는 `Laravel\Cashier\Cashier` 클래스를 통해 Cashier에 커스텀 모델을 사용하도록 지시할 수 있습니다. 일반적으로 이 설정은 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 수행합니다.

```
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```

<a name="customers"></a>

<!-- ## Customers -->
## Customers

<a name="retrieving-customers"></a>

<!-- ### Retrieving Customers -->
### Retrieving Customers

<!-- You can retrieve a customer by their Stripe ID using the `Cashier::findBillable` method. This method will return an instance of the billable model: -->
`Cashier::findBillable` 메서드를 사용해서 Stripe ID로 고객을 조회할 수 있습니다. 이 메서드는 청구가 가능한 모델 인스턴스를 반환합니다.

```
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>

<!-- ### Creating Customers -->
### Creating Customers

<!-- Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method: -->
때로는 구독을 시작하지 않고 Stripe 고객만 먼저 생성하고 싶을 때가 있습니다. 이럴 때 `createAsStripeCustomer` 메서드를 사용하면 됩니다.

```
$stripeCustomer = $user->createAsStripeCustomer();
```

<!-- Once the customer has been created in Stripe, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create): -->
Stripe에 고객 계정이 생성된 후에는 나중에 구독을 시작할 수 있습니다. Stripe에서 지원하는 [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create)를 추가로 전달하고 싶다면, `$options` 배열을 선택적으로 넘길 수 있습니다.

```
$stripeCustomer = $user->createAsStripeCustomer($options);
```

<!-- You may use the `asStripeCustomer` method if you want to return the Stripe customer object for a billable model: -->
청구가 가능한 모델의 Stripe 고객 객체를 직접 받고 싶을 때는 `asStripeCustomer` 메서드를 사용할 수 있습니다.

```
$stripeCustomer = $user->asStripeCustomer();
```

<!-- The `createOrGetStripeCustomer` method may be used if you would like to retrieve the Stripe customer object for a given billable model but are not sure whether the billable model is already a customer within Stripe. This method will create a new customer in Stripe if one does not already exist: -->
청구가 가능한 모델이 이미 Stripe에 고객으로 등록되어 있는지 확실하지 않은 경우, `createOrGetStripeCustomer` 메서드를 사용할 수 있습니다. 이 메서드는 이미 고객이 있으면 해당 고객을 조회하고, 없다면 Stripe에 새롭게 생성합니다.

```
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>

<!-- ### Updating Customers -->
### Updating Customers

<!-- Occasionally, you may wish to update the Stripe customer directly with additional information. You may accomplish this using the `updateStripeCustomer` method. This method accepts an array of [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update): -->
특정 정보를 Stripe의 고객 데이터에 직접 업데이트하고 싶을 때는 `updateStripeCustomer` 메서드를 사용할 수 있습니다. 이 메서드는 Stripe API에서 지원하는 [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update)을 배열로 받아 처리합니다.

```
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>

<!-- ### Balances -->
### Balances

<!-- Stripe allows you to credit or debit a customer's "balance". Later, this balance will be credited or debited on new invoices. To check the customer's total balance you may use the `balance` method that is available on your billable model. The `balance` method will return a formatted string representation of the balance in the customer's currency: -->
Stripe에서는 고객의 "잔액"에 금액을 더하거나 뺄 수 있습니다. 이후 새로 발행되는 인보이스에서 해당 잔액이 차감/증가하게 됩니다. 고객의 전체 잔액을 확인하려면, 청구가 가능한 모델에서 제공하는 `balance` 메서드를 사용할 수 있습니다. `balance` 메서드는 고객의 화폐 단위로 포맷된 문자열을 반환합니다.

```
$balance = $user->balance();
```

<!-- To credit a customer's balance, you may provide a negative value to the `applyBalance` method. If you wish, you may also provide a description: -->
고객의 잔액을 충전하려면(크레딧), `applyBalance` 메서드에 음수 값을 전달합니다. 필요하다면 설명도 추가할 수 있습니다.

```
$user->applyBalance(-500, 'Premium customer top-up.');
```

<!-- Providing a positive value to the `applyBalance` method will debit the customer's balance: -->
`applyBalance` 메서드에 양수 값을 전달하면 고객의 잔액이 차감(데빗)됩니다.

```
$user->applyBalance(300, 'Bad usage penalty.');
```

<!-- The `applyBalance` method will create new customer balance transactions for the customer. You may retrieve these transaction records using the `balanceTransactions` method, which may be useful in order to provide a log of credits and debits for the customer to review: -->
`applyBalance` 메서드는 해당 고객에 대한 새로운 잔액 거래(balance transaction) 기록을 생성합니다. `balanceTransactions` 메서드를 통해 거래 기록을 조회하여, 고객에게 잔액 내역을 제공할 수 있습니다.

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
Cashier에서는 고객의 세금 ID 관리도 쉽게 할 수 있습니다. 예를 들어, `taxIds` 메서드를 사용하면 고객에게 할당된 모든 [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션으로 가져올 수 있습니다.

```
$taxIds = $user->taxIds();
```

<!-- You can also retrieve a specific tax ID for a customer by its identifier: -->
고객의 특정 세금 ID를 식별자를 통해 조회할 수도 있습니다.

```
$taxId = $user->findTaxId('txi_belgium');
```

<!-- You may create a new Tax ID by providing a valid [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) and value to the `createTaxId` method: -->
`createTaxId` 메서드에 유효한 [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 전달해 새로운 세금 ID를 생성할 수 있습니다.

```
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

<!-- The `createTaxId` method will immediately add the VAT ID to the customer's account. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); however, this is an asynchronous process. You can be notified of verification updates by subscribing to the `customer.tax_id.updated` webhook event and inspecting [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). For more information on handling webhooks, please consult the [documentation on defining webhook handlers](#handling-stripe-webhooks). -->
`createTaxId` 메서드를 사용하면 VAT ID가 즉시 고객 계정에 추가됩니다. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation)되는데, 이 과정은 비동기로 처리됩니다. `customer.tax_id.updated` webhook 이벤트를 받아 [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 확인하면 검증 결과를 실시간으로 알릴 수 있습니다. Webhook 처리 방법에 대해서는 [documentation on defining webhook handlers](#handling-stripe-webhooks)를 참고하시기 바랍니다.

<!-- You may delete a tax ID using the `deleteTaxId` method: -->
세금 ID를 삭제하고 싶을 때는 `deleteTaxId` 메서드를 사용하면 됩니다.

```
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>

<!-- ### Syncing Customer Data With Stripe -->
### Syncing Customer Data With Stripe

<!-- Typically, when your application's users update their name, email address, or other information that is also stored by Stripe, you should inform Stripe of the updates. By doing so, Stripe's copy of the information will be in sync with your application's. -->
일반적으로 애플리케이션에서 사용자의 이름, 이메일, 기타 정보가 변경될 때 Stripe에 해당 변경사항도 알려야 합니다. 이렇게 하면 Stripe 쪽의 고객 정보도 항상 앱과 동일하게 유지됩니다.

<!-- To automate this, you may define an event listener on your billable model that reacts to the model's `updated` event. Then, within your event listener, you may invoke the `syncStripeCustomerDetails` method on the model: -->
이를 자동화하려면, 청구가 가능한 모델의 `updated` 이벤트에 리스너를 정의하고, 그 리스너 안에서 `syncStripeCustomerDetails` 메서드를 호출하면 됩니다.

```
use function Illuminate\Events\queueable;

/**
 * The "booted" method of the model.
 *
 * @return void
 */
protected static function booted()
{
    static::updated(queueable(function ($customer) {
        if ($customer->hasStripeId()) {
            $customer->syncStripeCustomerDetails();
        }
    }));
}
```

<!-- Now, every time your customer model is updated, its information will be synced with Stripe. For convenience, Cashier will automatically sync your customer's information with Stripe on the initial creation of the customer. -->
이제 고객 모델이 업데이트될 때마다 Stripe와 정보가 자동으로 동기화됩니다. 참고로, Cashier는 고객이 처음 생성될 때도 Stripe와 정보를 자동으로 동기화합니다.

<!-- You may customize the columns used for syncing customer information to Stripe by overriding a variety of methods provided by Cashier. For example, you may override the `stripeName` method to customize the attribute that should be considered the customer's "name" when Cashier syncs customer information to Stripe: -->
Stripe로 동기화할 고객 컬럼을 커스터마이징하려면 Cashier에서 제공하는 다양한 메서드를 오버라이드할 수 있습니다. 예를 들어, `stripeName` 메서드를 오버라이드해서 Stripe에 동기화할 고객명으로 사용할 속성(attribute)을 지정할 수 있습니다.

```
/**
 * Get the customer name that should be synced to Stripe.
 *
 * @return string|null
 */
public function stripeName()
{
    return $this->company_name;
}
```

<!-- Similarly, you may override the `stripeEmail`, `stripePhone`, and `stripeAddress` methods. These methods will sync information to their corresponding customer parameters when [updating the Stripe customer object](https://stripe.com/docs/api/customers/update). If you wish to take total control over the customer information sync process, you may override the `syncStripeCustomerDetails` method. -->
이와 마찬가지로, `stripeEmail`, `stripePhone`, `stripeAddress` 메서드도 오버라이드할 수 있습니다. 이 메서드들은 [updating the Stripe customer object](https://stripe.com/docs/api/customers/update)할 때 각각 해당 파라미터에 값을 동기화합니다. Stripe와의 동기화 과정을 직접 제어하고 싶다면 `syncStripeCustomerDetails` 메서드 전체를 오버라이드할 수도 있습니다.

<a name="billing-portal"></a>

<!-- ### Billing Portal -->
### Billing Portal

<!-- Stripe offers [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) so that your customer can manage their subscription, payment methods, and view their billing history. You can redirect your users to the billing portal by invoking the `redirectToBillingPortal` method on the billable model from a controller or route: -->
Stripe에서는 [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 고객은 이 포털을 통해 구독 관리, 결제 수단 관리, 결제 내역 조회 등을 직접 할 수 있습니다. 컨트롤러나 라우트에서 청구가 가능한 모델의 `redirectToBillingPortal` 메서드를 호출하면 사용자를 청구 포털로 리다이렉트할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

<!-- By default, when the user is finished managing their subscription, they will be able to return to the `home` route of your application via a link within the Stripe billing portal. You may provide a custom URL that the user should return to by passing the URL as an argument to the `redirectToBillingPortal` method: -->
기본적으로 사용자가 구독 관리를 마치면 Stripe 청구 포털 안의 링크를 통해 앱의 `home` 라우트로 돌아올 수 있습니다. 반환 경로를 커스텀 URL로 지정하고 싶다면, `redirectToBillingPortal` 메서드에 URL을 인수로 전달하면 됩니다.

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

<!-- If you would like to generate the URL to the billing portal without generating an HTTP redirect response, you may invoke the `billingPortalUrl` method: -->
HTTP 리다이렉트 없이 청구 포털의 URL만 생성하고 싶을 때는 `billingPortalUrl` 메서드를 사용할 수 있습니다.

```
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>

<!-- ## Payment Methods -->
## Payment Methods

<a name="storing-payment-methods"></a>

<!-- ### Storing Payment Methods -->
### Storing Payment Methods

<!-- In order to create subscriptions or perform "one off" charges with Stripe, you will need to store a payment method and retrieve its identifier from Stripe. The approach used to accomplish this differs based on whether you plan to use the payment method for subscriptions or single charges, so we will examine both below. -->
Stripe에서 구독을 생성하거나 1회성 결제를 처리하려면, 먼저 결제 수단을 저장하고 해당 결제 수단의 식별자를 Stripe에서 받아와야 합니다. 구독과 1회성 결제에서는 접근 방법이 조금 다르므로, 두 경우를 모두 살펴보겠습니다.

<a name="payment-methods-for-subscriptions"></a>

<!-- #### Payment Methods For Subscriptions -->
#### Payment Methods For Subscriptions

<!-- When storing a customer's credit card information for future use by a subscription, the Stripe "Setup Intents" API must be used to securely gather the customer's payment method details. A "Setup Intent" indicates to Stripe the intention to charge a customer's payment method. Cashier's `Billable` trait includes the `createSetupIntent` method to easily create a new Setup Intent. You should invoke this method from the route or controller that will render the form which gathers your customer's payment method details: -->
구독에서 고객의 신용카드 정보를 안전하게 저장하려면, Stripe의 "Setup Intents" API를 사용하여 결제 수단 정보를 수집해야 합니다. "Setup Intent"는 고객의 결제 수단을 앞으로 결제에 사용할 것임을 Stripe에 알리는 역할을 합니다. Cashier의 `Billable` 트레이트에는 `createSetupIntent` 메서드가 포함되어 있어 Setup Intent를 쉽게 생성할 수 있습니다. 이 메서드는 결제 수단 정보 입력 폼을 그릴 컨트롤러나 라우트에서 호출하면 됩니다.

```
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

<!-- After you have created the Setup Intent and passed it to the view, you should attach its secret to the element that will gather the payment method. For example, consider this "update payment method" form: -->
Setup Intent를 생성한 뒤, 해당 secret 값을 결제 수단 정보를 수집할 폼 요소에 포함시켜야 합니다. 예를 들어, 아래와 같이 "결제 수단 업데이트" 폼이 있다고 가정해 보겠습니다.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

<!-- Next, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
이제 Stripe.js 라이브러리를 활용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 붙여 결제 정보를 안전하게 수집할 수 있습니다.

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
다음으로, 카드 정보를 검증하고 Stripe에서 안전한 "결제 수단 식별자"를 받으려면 [Stripe's `confirmCardSetup` method](https://stripe.com/docs/js/setup_intents/confirm_card_setup)를 사용합니다.

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
카드가 Stripe에서 정상적으로 인증되면, 반환된 `setupIntent.payment_method` 식별자를 Laravel 애플리케이션으로 전송해서 고객에게 연결할 수 있습니다. 이 결제 수단은 [added as a new payment method](#adding-payment-methods)하거나 [used to update the default payment method](#updating-the-default-payment-method)할 수 있고, 결제 수단 식별자로 바로 [create a new subscription](#creating-subscriptions)하는 데 사용할 수도 있습니다.

> [!TIP]
> Setup Intents와 고객 결제 정보 수집 방식에 대해 더 알고 싶다면 [review this overview provided by Stripe](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>

<!-- #### Payment Methods For Single Charges -->
#### Payment Methods For Single Charges

<!-- Of course, when making a single charge against a customer's payment method, we will only need to use a payment method identifier once. Due to Stripe limitations, you may not use the stored default payment method of a customer for single charges. You must allow the customer to enter their payment method details using the Stripe.js library. For example, consider the following form: -->
고객 결제 수단으로 단 한번만 결제를 진행하는 경우에는 결제 수단 식별자를 한 번만 사용하면 됩니다. Stripe의 제한으로 인해, 고객의 저장된 기본 결제 수단은 1회성 결제에 사용할 수 없습니다. 따라서 Stripe.js를 사용해 결제할 때마다 고객에게 직접 결제 정보를 입력받아야 합니다. 예를 들어, 다음과 같은 폼을 만들 수 있습니다.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

<!-- After defining such a form, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
이런 폼을 만든 뒤 Stripe.js 라이브러리를 사용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 연결해 안전하게 결제 정보를 수집합니다.

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
카드 정보를 인증하고 Stripe에서 안전한 "결제 수단 식별자"를 받으려면 [Stripe's `createPaymentMethod` method](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method)를 사용합니다.

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
카드 인증이 성공하면, `paymentMethod.id` 값을 Laravel 애플리케이션에 전달해서 [single charge](#simple-charge)를 진행할 수 있습니다.

<a name="retrieving-payment-methods"></a>

<!-- ### Retrieving Payment Methods -->
### Retrieving Payment Methods

<!-- The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances: -->
Billable 모델 인스턴스에서 `paymentMethods` 메서드를 호출하면 `Laravel\Cashier\PaymentMethod` 인스턴스들의 컬렉션을 반환합니다.

```
$paymentMethods = $user->paymentMethods();
```

<!-- By default, this method will return payment methods of the `card` type. To retrieve payment methods of a different type, you may pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 `card` 타입의 결제 수단만 반환합니다. 만약 다른 타입의 결제 수단을 조회하고 싶다면 `type`을 인수로 전달하면 됩니다.

```
$paymentMethods = $user->paymentMethods('sepa_debit');
```

<!-- To retrieve the customer's default payment method, the `defaultPaymentMethod` method may be used: -->
고객의 기본 결제 수단을 조회하려면 `defaultPaymentMethod` 메서드를 사용할 수 있습니다.

```
$paymentMethod = $user->defaultPaymentMethod();
```

<!-- You can retrieve a specific payment method that is attached to the billable model using the `findPaymentMethod` method: -->
Billable 모델에 연결된 특정 결제 수단을 조회하려면 `findPaymentMethod` 메서드를 사용할 수 있습니다.

```
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="check-for-a-payment-method"></a>

<!-- ### Determining If A User Has A Payment Method -->
### Determining If A User Has A Payment Method

<!-- To determine if a billable model has a default payment method attached to their account, invoke the `hasDefaultPaymentMethod` method: -->
Billable 모델이 계정에 기본 결제 수단을 가지고 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 사용하면 됩니다.

```
if ($user->hasDefaultPaymentMethod()) {
    //
}
```

<!-- You may use the `hasPaymentMethod` method to determine if a billable model has at least one payment method attached to their account: -->
Billable 모델이 최소 하나의 결제 수단을 가지고 있는지 확인하려면 `hasPaymentMethod` 메서드를 사용할 수 있습니다.

```
if ($user->hasPaymentMethod()) {
    //
}
```

<!-- This method will determine if the billable model has payment methods of the `card` type. To determine if a payment method of another type exists for the model, you may pass the `type` as an argument to the method: -->
이 메서드는 기본적으로 `card` 타입의 결제 수단이 있는지 확인합니다. 만약 다른 타입의 결제 수단 존재 여부를 확인하려면 `type`을 인수로 전달하세요.

```
if ($user->hasPaymentMethod('sepa_debit')) {
    //
}
```

<a name="updating-the-default-payment-method"></a>

<!-- ### Updating The Default Payment Method -->
### Updating The Default Payment Method

<!-- The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method: -->
`updateDefaultPaymentMethod` 메서드를 사용하면 고객의 기본 결제 수단 정보를 업데이트할 수 있습니다. 이 메서드는 Stripe 결제 수단 식별자를 인수로 받아, 해당 결제 수단을 기본 결제 수단으로 지정합니다.

```
$user->updateDefaultPaymentMethod($paymentMethod);
```

<!-- To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method: -->
Stripe에 저장된 고객의 기본 결제 수단 정보와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용할 수 있습니다.

```
$user->updateDefaultPaymentMethodFromStripe();
```

> [!NOTE]
> 고객의 기본 결제 수단은 송장 발행 및 새 구독 생성에만 사용할 수 있습니다. Stripe의 정책상, 단일 결제(일회성 청구)에서는 기본 결제 수단을 사용할 수 없습니다.

<a name="adding-payment-methods"></a>

<!-- ### Adding Payment Methods -->
### Adding Payment Methods

<!-- To add a new payment method, you may call the `addPaymentMethod` method on the billable model, passing the payment method identifier: -->
새로운 결제 수단을 추가하려면, billable 모델의 `addPaymentMethod` 메서드에 결제 수단 식별자를 전달하면 됩니다.

```
$user->addPaymentMethod($paymentMethod);
```

> [!TIP]
> 결제 수단 식별자를 조회하는 방법에 대해서는 [payment method storage documentation](#storing-payment-methods)를 참고하세요.

<a name="deleting-payment-methods"></a>

<!-- ### Deleting Payment Methods -->
### Deleting Payment Methods

<!-- To delete a payment method, you may call the `delete` method on the `Laravel\Cashier\PaymentMethod` instance you wish to delete: -->
결제 수단을 삭제하려면, 삭제하고 싶은 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```
$paymentMethod->delete();
```

<!-- The `deletePaymentMethod` method will delete a specific payment method from the billable model: -->
특정 결제 수단을 billable 모델에서 삭제하려면 `deletePaymentMethod` 메서드를 사용하면 됩니다.

```
$user->deletePaymentMethod('pm_visa');
```

<!-- The `deletePaymentMethods` method will delete all of the payment method information for the billable model: -->
모든 결제 수단 정보를 billable 모델에서 삭제하고 싶다면 `deletePaymentMethods` 메서드를 사용합니다.

```
$user->deletePaymentMethods();
```

<!-- By default, this method will delete payment methods of the `card` type. To delete payment methods of a different type you can pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 `card` 타입의 결제 수단만 삭제합니다. 다른 타입의 결제 수단을 삭제하려면, `type`을 인수로 전달하세요.

```
$user->deletePaymentMethods('sepa_debit');
```

> [!NOTE]
> 사용자가 활성화된 구독을 가지고 있는 경우, 애플리케이션에서는 기본 결제 수단을 삭제하지 못하도록 해야 합니다.

<a name="subscriptions"></a>

<!-- ## Subscriptions -->
## Subscriptions

<!-- Subscriptions provide a way to set up recurring payments for your customers. Stripe subscriptions managed by Cashier provide support for multiple subscription prices, subscription quantities, trials, and more. -->
구독 기능을 이용하면 고객에게 반복 결제를 설정할 수 있습니다. Cashier로 관리되는 Stripe 구독은 여러 구독 가격, 구독 수량, 무료 체험 등 다양한 기능을 지원합니다.

<a name="creating-subscriptions"></a>

<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription: -->
구독을 생성하려면, 먼저 billable 모델의 인스턴스를 가져와야 합니다. 일반적으로 이 인스턴스는 `App\Models\User`가 됩니다. 모델 인스턴스를 가져온 후, `newSubscription` 메서드를 사용해 구독을 생성할 수 있습니다.

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

<!-- The first argument passed to the `newSubscription` method should be the internal name of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription name is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument is the specific price the user is subscribing to. This value should correspond to the price's identifier in Stripe. -->
`newSubscription` 메서드의 첫 번째 인수는 구독의 내부 이름입니다. 애플리케이션에서 단일 구독만 제공한다면 `default`나 `primary` 등 의미 있는 이름을 사용할 수 있습니다. 이 구독 이름은 내부적으로만 사용되며 사용자에게 노출하지 않습니다. 또한, 이름에 공백이 없어야 하고, 구독을 생성한 이후에는 변경하지 않는 것이 좋습니다. 두 번째 인수는 사용자가 구독할 Stripe 가격(Price)의 식별자입니다.

<!-- The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information. -->
`create` 메서드는 [a Stripe payment method identifier](#storing-payment-methods) 또는 Stripe `PaymentMethod` 객체를 받아, 구독을 시작하고 billable 모델의 Stripe 고객 ID 및 관련 결제 정보를 데이터베이스에 저장합니다.

> [!NOTE]
> 결제 수단 식별자를 `create` 구독 메서드에 직접 전달하면, 해당 결제 수단이 자동으로 사용자의 저장된 결제 수단 목록에도 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>

<!-- #### Collecting Recurring Payments Via Invoice Emails -->
#### Collecting Recurring Payments Via Invoice Emails

<!-- Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices: -->
고객의 반복 결제를 자동으로 청구하는 대신, 결제 시점마다 Stripe가 고객에게 결제 요청 인보이스 이메일을 보내도록 설정할 수 있습니다. 이 방식에서는 고객이 받은 인보이스를 수동으로 결제하면 됩니다. 인보이스 방식으로 반복 결제를 설정할 때는, 결제 수단을 미리 등록할 필요가 없습니다.

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

<!-- The amount of time a customer has to pay their invoice before their subscription is canceled is determined by your subscription and invoice settings within the [Stripe dashboard](https://dashboard.stripe.com/settings/billing/automatic). -->
고객이 인보이스를 결제하지 않아 구독이 만료되기까지의 유예 기간은 [Stripe dashboard](https://dashboard.stripe.com/settings/billing/automatic) 내 구독 및 인보이스 설정을 통해 관리할 수 있습니다.

<a name="subscription-quantities"></a>

<!-- #### Quantities -->
#### Quantities

<!-- If you would like to set a specific [quantity](https://stripe.com/docs/billing/subscriptions/quantities) for the price when creating the subscription, you should invoke the `quantity` method on the subscription builder before creating the subscription: -->
구독 생성 시, 가격마다 특정 [quantity](https://stripe.com/docs/billing/subscriptions/quantities)을 지정하고 싶다면, 구독 생성 전에 `quantity` 메서드를 사용할 수 있습니다.

```
$user->newSubscription('default', 'price_monthly')
     ->quantity(5)
     ->create($paymentMethod);
```

<a name="additional-details"></a>

<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional [customer](https://stripe.com/docs/api/customers/create) or [subscription](https://stripe.com/docs/api/subscriptions/create) options supported by Stripe, you may do so by passing them as the second and third arguments to the `create` method: -->
Stripe에서 지원하는 [customer](https://stripe.com/docs/api/customers/create) 또는 [subscription](https://stripe.com/docs/api/subscriptions/create) 옵션을 더 지정하고 싶을 때, `create` 메서드의 두 번째 및 세 번째 인수로 전달할 수 있습니다.

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
구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용할 수 있습니다.

```
$user->newSubscription('default', 'price_monthly')
     ->withCoupon('code')
     ->create($paymentMethod);
```

<!-- Or, if you would like to apply a [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes), you may use the `withPromotionCode` method. The given promotion code ID should be the Stripe API ID assigned to the promotion code and not the customer facing promotion code: -->
또는, [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 적용하려면 `withPromotionCode` 메서드를 사용할 수 있습니다. 전달하는 값은 고객이 보는 코드가 아니라 Stripe API ID여야 합니다.

```
$user->newSubscription('default', 'price_monthly')
     ->withPromotionCode('promo_code')
     ->create($paymentMethod);
```

<a name="adding-subscriptions"></a>

<!-- #### Adding Subscriptions -->
#### Adding Subscriptions

<!-- If you would like to add a subscription to a customer who already has a default payment method you may invoke the `add` method on the subscription builder: -->
이미 기본 결제 수단이 등록된 고객에게 구독을 추가하려면(subscription builder에서) `add` 메서드를 사용할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>

<!-- #### Creating Subscriptions From The Stripe Dashboard -->
#### Creating Subscriptions From The Stripe Dashboard

<!-- You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a name of `default`. To customize the subscription name that is assigned to dashboard created subscriptions, [extend the `WebhookController`](/docs/8.x/billing#defining-webhook-event-handlers) and overwrite the `newSubscriptionName` method. -->
Stripe 대시보드에서도 구독을 생성할 수 있습니다. 이 경우, Cashier가 새로 추가된 구독을 동기화하고 구독 이름을 `default`로 지정합니다. 대시보드에서 생성된 구독의 이름을 커스터마이징하려면, [extend the `WebhookController`](/docs/8.x/billing#defining-webhook-event-handlers)하고 `newSubscriptionName` 메서드를 오버라이드해야 합니다.

<!-- In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different names, only one type of subscription may be added through the Stripe dashboard. -->
또한, Stripe 대시보드에서는 한 종류의 구독만 생성할 수 있습니다. 애플리케이션이 여러 구독을 지원하는 경우, 각 이름별로 하나의 구독만 Stripe 대시보드를 통해 추가할 수 있습니다.

<!-- Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database. -->
마지막으로, 애플리케이션에서 제공하는 각 구독 종류별로 항상 활성화된 구독이 하나만 존재하도록 관리해야 합니다. 만약 고객에게 두 개의 `default` 구독이 있을 경우, Cashier에서는 가장 최근에 추가된 구독만을 사용하며, 두 구독 모두 애플리케이션의 데이터베이스와 동기화됩니다.

<a name="checking-subscription-status"></a>

<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the name of the subscription as its first argument: -->
고객이 애플리케이션에 구독하게 되면, 다양한 편의 메서드를 활용해 구독 상태를 쉽게 확인할 수 있습니다. 먼저, `subscribed` 메서드는 사용자가 활성화된 구독을 가지고 있다면(트라이얼 기간 포함) `true`를 반환합니다. `subscribed` 메서드는 첫 번째 인수로 구독 이름을 받습니다.

```
if ($user->subscribed('default')) {
    //
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/8.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
또한, `subscribed` 메서드는 [route middleware](/docs/8.x/middleware)로 사용하여 사용자의 구독 상태에 따라 라우트와 컨트롤러 접근을 제어하는 데 적합합니다.

```
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureUserIsSubscribed
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // This user is not a paying customer...
            return redirect('billing');
        }

        return $next($request);
    }
}
```

<!-- If you would like to determine if a user is still within their trial period, you may use the `onTrial` method. This method can be useful for determining if you should display a warning to the user that they are still on their trial period: -->
사용자가 아직 트라이얼(체험) 기간 내에 있는지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 아직 트라이얼 중임을 사용자에게 알림으로써 안내가 필요할 때 유용합니다.

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- The `subscribedToProduct` method may be used to determine if the user is subscribed to a given product based on a given Stripe product's identifier. In Stripe, products are collections of prices. In this example, we will determine if the user's `default` subscription is actively subscribed to the application's "premium" product. The given Stripe product identifier should correspond to one of your product's identifiers in the Stripe dashboard: -->
`subscribedToProduct` 메서드는 주어진 Stripe 상품(프로덕트) 식별자를 기반으로 사용자가 해당 상품의 구독을 가지고 있는지 확인할 수 있습니다. Stripe에서 상품(Product)은 가격(Price)들의 집합입니다. 아래 예시는 사용자의 `default` 구독이 애플리케이션에서 "premium" 상품에 구독되어 있는지 확인합니다. Stripe 상품 식별자는 대시보드에서 확인할 수 있습니다.

```
if ($user->subscribedToProduct('prod_premium', 'default')) {
    //
}
```

<!-- By passing an array to the `subscribedToProduct` method, you may determine if the user's `default` subscription is actively subscribed to the application's "basic" or "premium" product: -->
`subscribedToProduct` 메서드에 배열을 전달하면, 예를 들어 사용자의 `default` 구독이 "basic" 또는 "premium" 상품에 구독되어 있는지 한 번에 확인할 수 있습니다.

```
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    //
}
```

<!-- The `subscribedToPrice` method may be used to determine if a customer's subscription corresponds to a given price ID: -->
`subscribedToPrice` 메서드는 구독이 특정 가격(Price) ID에 해당하는지 확인할 때 사용합니다.

```
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    //
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
`recurring` 메서드는 사용자가 현재 구독 중이며 더 이상 트라이얼(체험) 기간이 아닌지를 확인합니다.

```
if ($user->subscription('default')->recurring()) {
    //
}
```

> [!NOTE]
> 사용자가 동일한 이름의 구독을 2개 가지고 있을 경우, `subscription` 메서드는 항상 가장 최근의 구독만 반환합니다. 예를 들어, 사용자가 두 개의 `default` 구독 레코드를 가지고 있을 수 있는데, 하나는 만료된 예전 구독이고 다른 하나는 현재 활성 구독일 수 있습니다. 이 경우 항상 가장 최근의 구독이 반환되며, 예전 구독은 이력 조회를 위해 데이터베이스에 남아 있습니다.

<a name="cancelled-subscription-status"></a>

<!-- #### Canceled Subscription Status -->
#### Canceled Subscription Status

<!-- To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method: -->
사용자가 한때 활성 구독자였지만, 구독을 취소했다는 것을 확인하려면 `canceled` 메서드를 사용할 수 있습니다.

```
if ($user->subscription('default')->canceled()) {
    //
}
```

<!-- You may also determine if a user has canceled their subscription but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
또한, 사용자가 구독을 취소했지만 완전히 만료되기 전 "유예 기간(grace period)"에 있는지 확인할 수도 있습니다. 예를 들어, 사용자가 3월 5일에 구독을 취소했고 구독 만료 예정일이 3월 10일인 경우, 사용자는 3월 10일까지 유예 기간 상태가 됩니다. 이 기간 동안 `subscribed` 메서드는 여전히 `true`를 반환합니다.

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- To determine if the user has canceled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
유예 기간이 지나고 구독이 완전히 종료되었는지 확인하려면 `ended` 메서드를 사용하세요.

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="incomplete-and-past-due-status"></a>

<!-- #### Incomplete and Past Due Status -->
#### Incomplete and Past Due Status

<!-- If a subscription requires a secondary payment action after creation the subscription will be marked as `incomplete`. Subscription statuses are stored in the `stripe_status` column of Cashier's `subscriptions` database table. -->
구독 생성 후 추가 결제 처리가 필요한 경우, 해당 구독 상태는 `incomplete`로 표시됩니다. 구독 상태 정보는 Cashier의 `subscriptions` 데이터베이스 테이블의 `stripe_status` 컬럼에 저장됩니다.

<!-- Similarly, if a secondary payment action is required when swapping prices the subscription will be marked as `past_due`. When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Determining if a subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
마찬가지로, 가격 변경 시 추가 결제 처리가 필요한 경우 구독 상태는 `past_due`로 전환됩니다. 구독이 이들 상태에 있을 때는 고객이 결제 절차를 완료하기 전까지 활성 상태가 아니게 됩니다. 구독에 미완료 결제가 있는지 여부는 billable 모델이나 구독 인스턴스에서 `hasIncompletePayment` 메서드로 확인할 수 있습니다.

```
if ($user->hasIncompletePayment('default')) {
    //
}

if ($user->subscription('default')->hasIncompletePayment()) {
    //
}
```

<!-- When a subscription has an incomplete payment, you should direct the user to Cashier's payment confirmation page, passing the `latestPayment` identifier. You may use the `latestPayment` method available on subscription instance to retrieve this identifier: -->
구독에 미완료 결제가 있을 때는, 사용자에게 Cashier의 결제 확인 페이지로 안내하여 `latestPayment` 식별자를 전달하세요. 이 식별자는 구독 인스턴스의 `latestPayment` 메서드로 가져올 수 있습니다.

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

<!-- If you would like the subscription to still be considered active when it's in a `past_due` state, you may use the `keepPastDueSubscriptionsActive` method provided by Cashier. Typically, this method should be called in the `register` method of your `App\Providers\AppServiceProvider`: -->
구독이 `past_due` 상태일 때도 활성 상태로 간주하길 원한다면, Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 메서드를 사용할 수 있습니다. 보통 이 메서드는 `App\Providers\AppServiceProvider`의 `register` 메서드에서 호출하는 것이 일반적입니다.

```
use Laravel\Cashier\Cashier;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!NOTE]
> 구독이 `incomplete` 상태인 경우 결제가 완료되기 전에는 변경할 수 없습니다. 따라서, 구독이 `incomplete` 상태일 때는 `swap` 및 `updateQuantity` 메서드가 예외를 발생시킵니다.

<a name="subscription-scopes"></a>

<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
대부분의 구독 상태는 쿼리 스코프로도 제공되어, 특정 상태의 구독을 DB에서 쉽게 조회할 수 있습니다.

```
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

<!-- A complete list of available scopes is available below: -->
사용 가능한 모든 스코프 목록은 아래와 같습니다.

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
고객이 애플리케이션 구독 중에 가격을 변경하고 싶을 때도 있습니다. Stripe 가격 식별자를 `swap` 메서드에 전달하면 손쉽게 새 가격으로 변경할 수 있습니다. 가격을 변경할 때는 이전에 취소된 구독도 자동으로 다시 활성화된다고 가정합니다. 이때 전달한 식별자는 Stripe 대시보드에 등록된 가격 식별자여야 합니다.

```
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

<!-- If the customer is on trial, the trial period will be maintained. Additionally, if a "quantity" exists for the subscription, that quantity will also be maintained. -->
고객이 트라이얼(체험) 중이라면, 체험 기간이 유지됩니다. 또한 구독에 "수량"이 지정돼 있다면 그 수량도 유지됩니다.

<!-- If you would like to swap prices and cancel any trial period the customer is currently on, you may invoke the `skipTrial` method: -->
가격을 바꿀 때 현재 체험 기간을 같이 종료하려면, `skipTrial` 메서드를 함께 사용할 수 있습니다.

```
$user->subscription('default')
        ->skipTrial()
        ->swap('price_yearly');
```

<!-- If you would like to swap prices and immediately invoice the customer instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
가격을 바꾸고 기다릴 필요 없이 즉시 인보이스를 발행하려면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>

<!-- #### Prorations -->
#### Prorations

<!-- By default, Stripe prorates charges when swapping between prices. The `noProrate` method may be used to update the subscription's price without prorating the charges: -->
Stripe에서는 기본적으로 가격 변경 시 요금을 일할계산(proration)합니다. 일할계산(co)는 하지 않고 가격만 즉시 변경하고 싶다면 `noProrate` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->noProrate()->swap('price_yearly');
```

<!-- For more information on subscription proration, consult the [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations). -->
구독 일할계산에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations)를 참고하세요.

> [!NOTE]
> `swapAndInvoice` 이전에 `noProrate`를 호출하더라도, 일할계산(proration)은 항상 적용됩니다. 즉, 인보이스는 반드시 발행됩니다.

<a name="subscription-quantity"></a>

<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. You may use the `incrementQuantity` and `decrementQuantity` methods to easily increment or decrement your subscription quantity: -->
구독에 "수량" 개념이 도입될 수 있습니다. 예를 들어, 프로젝트 관리 애플리케이션에서 프로젝트 당 월 10달러를 책정할 경우가 이에 해당합니다. `incrementQuantity` 및 `decrementQuantity` 메서드를 통해 구독 수량을 손쉽게 더하거나 뺄 수 있습니다.

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
또는, `updateQuantity` 메서드로 특정 수량을 직접 설정할 수도 있습니다.

```
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
일할계산 없이 구독 수량을 업데이트하고 싶다면 `noProrate` 메서드와 함께 사용하세요.

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<!-- For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities). -->
구독 수량에 대한 자세한 정보는 [Stripe documentation](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="multiprice-subscription-quantities"></a>

<!-- #### Multiprice Subscription Quantities -->
#### Multiprice Subscription Quantities

<!-- If your subscription is a [multiprice subscription](#multiprice-subscriptions), you should pass the name of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods: -->
구독이 [multiprice subscription](#multiprice-subscriptions)인 경우, 수량을 늘리거나 줄이고자 하는 가격 이름을 두 번째 인수로 전달해야 합니다.

```
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="multiprice-subscriptions"></a>

<!-- ### Multiprice Subscriptions -->
### Multiprice Subscriptions

<!-- [Multiprice subscriptions](https://stripe.com/docs/billing/subscriptions/multiple-products) allow you to assign multiple billing prices to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on price for an additional $15 per month. Multiprice subscription information is stored in Cashier's `subscription_items` database table. -->
[Multiprice subscriptions](https://stripe.com/docs/billing/subscriptions/multiple-products)은 한 구독에 여러 결제 가격을 지정할 수 있게 해 줍니다. 예를 들어, 고객지원 헬프데스크 애플리케이션을 만든다고 했을 때, 기본 구독 가격이 월 $10이고, 추가로 라이브 채팅 옵션을 월 $15에 제공하고자 할 때 사용합니다. 멀티프라이스 구독 정보는 Cashier의 `subscription_items` 테이블에 저장됩니다.

<!-- You may specify multiple prices for a given subscription by passing an array of prices as the second argument to the `newSubscription` method: -->
`newSubscription` 메서드의 두 번째 인수로 가격 배열을 전달하면, 한 구독에 여러 가격을 지정할 수 있습니다.

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
위 예제에서는 고객의 `default` 구독에 2가지 가격 항목이 추가되어, 각기 다른 청구 주기로 요금이 부과됩니다. 가격마다 별도의 수량이 필요하면 `quantity` 메서드를 사용해 추가로 지정할 수 있습니다.

```
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

<!-- If you would like to add another price to an existing subscription, you may invoke the subscription's `addPrice` method: -->
기존 구독에 가격 항목을 추가하려면 구독의 `addPrice` 메서드를 사용하세요.

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

<!-- The example above will add the new price and the customer will be billed for it on their next billing cycle. If you would like to bill the customer immediately you may use the `addPriceAndInvoice` method: -->
위 예에서는 새 가격이 추가되고, 다음 결제 주기 시점에 새로운 가격이 함께 청구됩니다. 즉시 고객에게 요금을 부과하고 싶다면 `addPriceAndInvoice` 메서드를 사용하세요.

```
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

<!-- If you would like to add a price with a specific quantity, you can pass the quantity as the second argument of the `addPrice` or `addPriceAndInvoice` methods: -->
특정 수량을 갖는 가격을 추가하려면, 두 번째 인수로 수량을 전달하면 됩니다. 이는 `addPrice`와 `addPriceAndInvoice` 메서드 모두 적용됩니다.

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

<!-- You may remove prices from subscriptions using the `removePrice` method: -->
구독에서 가격을 제거하려면 `removePrice` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->removePrice('price_chat');
```

> [!NOTE]
> 구독의 마지막 가격 항목은 삭제할 수 없습니다. 대신 구독 자체를 취소해야 합니다.

<a name="swapping-prices"></a>

<!-- #### Swapping Prices -->
#### Swapping Prices

<!-- You may also change the prices attached to a multiprice subscription. For example, imagine a customer has a `price_basic` subscription with a `price_chat` add-on price and you want to upgrade the customer from the `price_basic` to the `price_pro` price: -->
멀티프라이스 구독에서도 가격 항목을 쉽게 교체할 수 있습니다. 예를 들어, 고객이 `price_basic` 상품과 `price_chat` 추가상품에 구독 중일 때, `price_basic`을 `price_pro`로 업그레이드하려고 한다면 다음과 같이 할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

<!-- When executing the example above, the underlying subscription item with the `price_basic` is deleted and the one with the `price_chat` is preserved. Additionally, a new subscription item for the `price_pro` is created. -->
위 예제처럼 실행하면, 기존의 `price_basic` 구독 항목이 삭제되고 `price_chat` 항목은 유지됩니다. 그리고 새롭게 `price_pro`에 대한 구독 항목이 생성됩니다.

<!-- You can also specify subscription item options by passing an array of key / value pairs to the `swap` method. For example, you may need to specify the subscription price quantities: -->
구독 항목 옵션을 지정해야 한다면, `swap` 메서드에 키-값 쌍의 배열을 전달할 수 있습니다. 예를 들어 각 가격별 수량을 지정해야 하는 경우가 해당합니다.

```
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

<!-- If you want to swap a single price on a subscription, you may do so using the `swap` method on the subscription item itself. This approach is particularly useful if you would like to preserve all of the existing metadata on the subscription's other prices: -->
구독에서 특정 가격만 바꾸고 나머지 가격의 메타데이터는 그대로 유지하고 싶다면, 구독 항목 자체의 `swap` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')
        ->findItemOrFail('price_basic')
        ->swap('price_pro');
```

<a name="proration"></a>

<!-- #### Proration -->
#### Proration

<!-- By default, Stripe will prorate charges when adding or removing prices from a multiprice subscription. If you would like to make a price adjustment without proration, you should chain the `noProrate` method onto your price operation: -->
기본적으로 Stripe는 멀티 프라이스 구독에서 가격을 추가하거나 제거할 때 요금을 비례 배분하여 부과합니다. 만약 비례 배분 없이 가격을 조정하고자 한다면, 가격 조작 메서드 체이닝에 `noProrate` 메서드를 추가하면 됩니다.

```
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>

<!-- #### Quantities -->
#### Quantities

<!-- If you would like to update quantities on individual subscription prices, you may do so using the [existing quantity methods](#subscription-quantity) by passing the name of the price as an additional argument to the method: -->
개별 구독 가격의 수량을 업데이트하려면, [existing quantity methods](#subscription-quantity)에 가격 이름을 추가 인자로 전달하면 됩니다.

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!NOTE]
> 구독에 여러 가격이 포함되어 있을 때는 `Subscription` 모델의 `stripe_price` 및 `quantity` 속성이 `null`이 됩니다. 개별 가격 속성에 접근하고 싶다면, `Subscription` 모델의 `items` 연관관계를 사용해야 합니다.

<a name="subscription-items"></a>

<!-- #### Subscription Items -->
#### Subscription Items

<!-- When a subscription has multiple prices, it will have multiple subscription "items" stored in your database's `subscription_items` table. You may access these via the `items` relationship on the subscription: -->
구독에 여러 가격이 연결되어 있으면, 데이터베이스의 `subscription_items` 테이블에 여러 개의 구독 "아이템"이 저장됩니다. 이들은 구독의 `items` 연관관계를 통해 접근할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

<!-- You can also retrieve a specific price using the `findItemOrFail` method: -->
특정 가격에 해당하는 정보를 가져오려면 `findItemOrFail` 메서드를 사용할 수도 있습니다.

```
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="metered-billing"></a>

<!-- ### Metered Billing -->
### Metered Billing

<!-- [Metered billing](https://stripe.com/docs/billing/subscriptions/metered-billing) allows you to charge customers based on their product usage during a billing cycle. For example, you may charge customers based on the number of text messages or emails they send per month. -->
[Metered billing](https://stripe.com/docs/billing/subscriptions/metered-billing)을 사용하면, 결제 주기 동안 고객의 상품 사용량에 따라 요금을 부과할 수 있습니다. 예를 들어 고객이 보낸 문자 메시지 수나 이메일 건수 등을 기준으로 매달 과금할 수 있습니다.

<!-- To start using metered billing, you will first need to create a new product in your Stripe dashboard with a metered price. Then, use the `meteredPrice` to add the metered price ID to a customer subscription: -->
측정 기반 과금을 사용하려면 먼저 Stripe 대시보드에서 계량(측정) 가격이 포함된 새 상품을 생성해야 합니다. 그런 다음, `meteredPrice` 메서드를 사용해 해당 측정용 가격 ID를 고객 구독에 추가하면 됩니다.

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
[Stripe Checkout](#checkout)을 통해서도 측정 기반 구독을 시작할 수 있습니다.

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

<!-- As your customer uses your application, you will report their usage to Stripe so that they can be billed accurately. To increment the usage of a metered subscription, you may use the `reportUsage` method: -->
고객이 애플리케이션을 사용하는 만큼 Stripe에 해당 사용량을 보고해야 정확한 청구가 가능합니다. 측정 기반 구독의 사용량을 증가시키려면 `reportUsage` 메서드를 이용하세요.

```
$user = User::find(1);

$user->subscription('default')->reportUsage();
```

<!-- By default, a "usage quantity" of 1 is added to the billing period. Alternatively, you may pass a specific amount of "usage" to add to the customer's usage for the billing period: -->
기본적으로 "사용량" 값 1이 결제 주기에 추가됩니다. 원하는 만큼의 사용량을 추가하려면, 해당 수치를 인자로 전달하면 됩니다.

```
$user = User::find(1);

$user->subscription('default')->reportUsage(15);
```

<!-- If your application offers multiple prices on a single subscription, you will need to use the `reportUsageFor` method to specify the metered price you want to report usage for: -->
만약 하나의 구독에 여러 가격이 있다면, 어떤 측정 가격의 사용량을 보고할지 `reportUsageFor` 메서드로 지정해야 합니다.

```
$user = User::find(1);

$user->subscription('default')->reportUsageFor('price_metered', 15);
```

<!-- Sometimes, you may need to update usage which you have previously reported. To accomplish this, you may pass a timestamp or a `DateTimeInterface` instance as the second parameter to `reportUsage`. When doing so, Stripe will update the usage that was reported at that given time. You can continue to update previous usage records as the given date and time is still within the current billing period: -->
이미 보고한 사용량을 업데이트해야 할 경우, `reportUsage`의 두 번째 인자로 타임스탬프나 `DateTimeInterface` 인스턴스를 넘기면 됩니다. 이 경우, Stripe는 해당 시점에 보고한 사용량을 업데이트합니다. 주어진 날짜 및 시간이 현재 결제 주기 내에 있다면, 계속해서 이전 사용 이력을 수정할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')->reportUsage(5, $timestamp);
```

<a name="retrieving-usage-records"></a>

<!-- #### Retrieving Usage Records -->
#### Retrieving Usage Records

<!-- To retrieve a customer's past usage, you may use a subscription instance's `usageRecords` method: -->
고객의 과거 사용 이력을 조회하려면 구독 인스턴스의 `usageRecords` 메서드를 사용하면 됩니다.

```
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecords();
```

<!-- If your application offers multiple prices on a single subscription, you may use the `usageRecordsFor` method to specify the metered price that you wish to retrieve usage records for: -->
만약 하나의 구독에 여러 가격이 있다면, 원하는 측정 가격의 사용 이력을 조회하려면 `usageRecordsFor` 메서드를 사용하세요.

```
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecordsFor('price_metered');
```

<!-- The `usageRecords` and `usageRecordsFor` methods return a Collection instance containing an associative array of usage records. You may iterate over this array to display a customer's total usage: -->
`usageRecords` 및 `usageRecordsFor` 메서드는 usage record들의 연관 배열을 포함한 Collection 인스턴스를 반환합니다. 이를 반복문 등으로 순회하며 고객의 전체 사용량을 표시할 수 있습니다.

```
@foreach ($usageRecords as $usageRecord)
    - Period Starting: {{ $usageRecord['period']['start'] }}
    - Period Ending: {{ $usageRecord['period']['end'] }}
    - Total Usage: {{ $usageRecord['total_usage'] }}
@endforeach
```

<!-- For a full reference of all usage data returned and how to use Stripe's cursor based pagination, please consult [the official Stripe API documentation](https://stripe.com/docs/api/usage_records/subscription_item_summary_list). -->
사용 데이터의 전체 목록 및 Stripe의 커서 기반 페이지네이션 사용법 등은 [the official Stripe API documentation](https://stripe.com/docs/api/usage_records/subscription_item_summary_list)에서 확인할 수 있습니다.

<a name="subscription-taxes"></a>

<!-- ### Subscription Taxes -->
### Subscription Taxes

> [!NOTE]
> 세율을 직접 계산하지 않고도 [automatically calculate taxes using Stripe Tax](#tax-configuration)할 수 있습니다.

<!-- To specify the tax rates a user pays on a subscription, you should implement the `taxRates` method on your billable model and return an array containing the Stripe tax rate IDs. You can define these tax rates in [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates): -->
구독에 대해 사용자가 지불해야 할 세율을 지정하려면, 청구 가능 모델에서 `taxRates` 메서드를 구현하고 Stripe 세금 ID 배열을 반환해야 합니다. 이 세율 ID는 [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates)에서 정의할 수 있습니다.

```
/**
 * The tax rates that should apply to the customer's subscriptions.
 *
 * @return array
 */
public function taxRates()
{
    return ['txr_id'];
}
```

<!-- The `taxRates` method enables you to apply a tax rate on a customer-by-customer basis, which may be helpful for a user base that spans multiple countries and tax rates. -->
`taxRates` 메서드는 고객별로 구독 세율을 다르게 설정할 수 있어, 다양한 국가나 세율을 가진 사용자층에 유용합니다.

<!-- If you're offering multiprice subscriptions, you may define different tax rates for each price by implementing a `priceTaxRates` method on your billable model: -->
멀티 프라이스 구독을 제공하는 경우, 청구 가능 모델에 `priceTaxRates` 메서드를 구현하여 각 가격별로 다른 세율을 지정할 수도 있습니다.

```
/**
 * The tax rates that should apply to the customer's subscriptions.
 *
 * @return array
 */
public function priceTaxRates()
{
    return [
        'price_monthly' => ['txr_id'],
    ];
}
```

> [!NOTE]
> `taxRates` 메서드는 구독 요금에만 적용됩니다. Cashier로 "일회성" 결제를 진행할 경우, 해당 시점에 직접 세금을 지정해주어야 합니다.

<a name="syncing-tax-rates"></a>

<!-- #### Syncing Tax Rates -->
#### Syncing Tax Rates

<!-- When changing the hard-coded tax rate IDs returned by the `taxRates` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the new `taxRates` values, you should call the `syncTaxRates` method on the user's subscription instance: -->
`taxRates` 메서드에서 반환하는 하드코딩된 세율 ID를 변경해도, 기존 사용자의 구독에는 세팅이 그대로 남아 있습니다. 기존 구독에 대해 새로운 `taxRates` 값을 반영하려면, 해당 사용자의 구독 인스턴스에서 `syncTaxRates` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->syncTaxRates();
```

<!-- This will also sync any multiprice subscription item tax rates. If your application is offering multiprice subscriptions, you should ensure that your billable model implements the `priceTaxRates` method [discussed above](#subscription-taxes). -->
이 메서드는 멀티 프라이스 구독 아이템의 개별 세율까지 함께 동기화해 줍니다. 멀티 프라이스 구독을 제공하는 경우, 반드시 [discussed above](#subscription-taxes) `priceTaxRates` 메서드를 청구 가능 모델에 구현해 두어야 합니다.

<a name="tax-exemption"></a>

<!-- #### Tax Exemption -->
#### Tax Exemption

<!-- Cashier also offers the `isNotTaxExempt`, `isTaxExempt`, and `reverseChargeApplies` methods to determine if the customer is tax exempt. These methods will call the Stripe API to determine a customer's tax exemption status: -->
Cashier는 고객이 세금 면제 대상인지 판단할 수 있도록 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드도 제공합니다. 이들 메서드는 Stripe API를 호출하여 고객의 세금 면제 상태를 확인합니다.

```
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!NOTE]
> 위 메서드들은 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있습니다. 단, `Invoice` 객체에서 호출할 경우 인보이스가 생성된 시점의 면제 상태를 조회합니다.

<a name="subscription-anchor-date"></a>

<!-- ### Subscription Anchor Date -->
### Subscription Anchor Date

<!-- By default, the billing cycle anchor is the date the subscription was created or, if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method: -->
기본적으로 결제 주기 앵커(시작일)는 구독이 최초 생성된 날짜이거나, 체험 기간(trial)을 사용하는 경우에는 체험이 끝나는 날짜입니다. 결제일 기준(anchor)을 변경하려면, `anchorBillingCycleOn` 메서드를 이용하면 됩니다.

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
구독 결제 주기(anchor) 관리에 대한 더 자세한 사항은 [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>

<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
구독을 취소하려면, 사용자의 구독 인스턴스에서 `cancel` 메서드를 호출합니다.

```
$user->subscription('default')->cancel();
```

<!-- When a subscription is canceled, Cashier will automatically set the `ends_at` column in your `subscriptions` database table. This column is used to know when the `subscribed` method should begin returning `false`. -->
구독이 취소되면, Cashier는 자동으로 `subscriptions` 데이터베이스 테이블의 `ends_at` 컬럼을 설정합니다. 이 컬럼은 `subscribed` 메서드가 언제부터 `false`를 반환해야 하는지를 판단하는 데 사용됩니다.

<!-- For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
예를 들어, 고객이 3월 1일 구독을 취소했지만, 구독 만료일이 3월 5일이라면, `subscribed` 메서드는 3월 5일까지 계속 `true`를 반환하게 됩니다. 이는 대부분의 애플리케이션에서 결제 주기 종료일까지 계속 서비스 사용을 허용하는 방식입니다.

<!-- You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
사용자가 구독을 취소했지만 "유예 기간(grace period)" 중에 있는지 확인하려면, `onGracePeriod` 메서드를 사용합니다.

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription: -->
즉시 구독을 취소하고 싶다면, `cancelNow` 메서드를 사용하세요.

```
$user->subscription('default')->cancelNow();
```

<!-- If you wish to cancel a subscription immediately and invoice any remaining un-invoiced metered usage or new / pending proration invoice items, call the `cancelNowAndInvoice` method on the user's subscription: -->
즉시 구독을 취소하면서, 미청구된 측정 사용량 또는 새로 발생했거나 대기 중인 비례 배분 인보이스 항목에 대해 바로 인보이스를 청구하고자 한다면, `cancelNowAndInvoice` 메서드를 사용하면 됩니다.

```
$user->subscription('default')->cancelNowAndInvoice();
```

<!-- You may also choose to cancel the subscription at a specific moment in time: -->
특정 시점에 구독이 종료되도록 예약하려면 다음과 같이 합니다.

```
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

<a name="resuming-subscriptions"></a>

<!-- ### Resuming Subscriptions -->
### Resuming Subscriptions

<!-- If a customer has canceled their subscription and you wish to resume it, you may invoke the `resume` method on the subscription. The customer must still be within their "grace period" in order to resume a subscription: -->
고객이 구독을 취소한 후, 다시 구독을 활성화하려면 구독 인스턴스의 `resume` 메서드를 호출하면 됩니다. 이때 고객은 반드시 "유예 기간(grace period)" 내에 있어야 합니다.

```
$user->subscription('default')->resume();
```

<!-- If the customer cancels a subscription and then resumes that subscription before the subscription has fully expired the customer will not be billed immediately. Instead, their subscription will be re-activated and they will be billed on the original billing cycle. -->
고객이 구독을 취소한 뒤 구독 만료 전 재개하는 경우에는 바로 결제되지 않고, 원래 결제 주기에 맞추어 구독이 다시 활성화되어 요금이 청구됩니다.

<a name="subscription-trials"></a>

<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>

<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions: -->
결제 수단 정보를 미리 받은 상태로 고객에게 체험 기간을 제공하고 싶다면, 구독 생성 시 `trialDays` 메서드를 사용합니다.

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
이 메서드는 구독 레코드의 trial 종료 일자를 데이터베이스에 저장하고, Stripe에도 청구 시작을 해당 날짜 이후로 미루라고 지시합니다. `trialDays` 메서드를 사용하면 Stripe에 설정된 가격의 기본 체험 기간도 무시됩니다.

> [!NOTE]
> 고객이 체험 기간 만료 전에 구독을 취소하지 않으면, 만료 즉시 청구가 발생하므로 체험 종료일을 사용자에게 반드시 안내해 주세요.

<!-- The `trialUntil` method allows you to provide a `DateTime` instance that specifies when the trial period should end: -->
`trialUntil` 메서드를 사용하면 체험 종료일을 직접 `DateTime` 인스턴스로 지정할 수 있습니다.

```
use Carbon\Carbon;

$user->newSubscription('default', 'price_monthly')
            ->trialUntil(Carbon::now()->addDays(10))
            ->create($paymentMethod);
```

<!-- You may determine if a user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
사용자가 체험 기간 내에 있는지 확인하려면, 사용자 인스턴스의 `onTrial` 메서드나 구독 인스턴스의 `onTrial` 메서드를 사용할 수 있습니다. 아래 두 예시는 동일하게 동작합니다.

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- You may use the `endTrial` method to immediately end a subscription trial: -->
체험 기간을 즉시 종료하려면, `endTrial` 메서드를 사용하세요.

```
$user->subscription('default')->endTrial();
```

<a name="defining-trial-days-in-stripe-cashier"></a>

<!-- #### Defining Trial Days In Stripe / Cashier -->
#### Defining Trial Days In Stripe / Cashier

<!-- You may choose to define how many trial days your price's receive in the Stripe dashboard or always pass them explicitly using Cashier. If you choose to define your price's trial days in Stripe you should be aware that new subscriptions, including new subscriptions for a customer that had a subscription in the past, will always receive a trial period unless you explicitly call the `skipTrial()` method. -->
Stripe 대시보드에서 가격별 기본 체험 일수를 지정할 수도 있고, 항상 Cashier를 통해 명시적으로 넘기는 방법도 있습니다. Stripe에서 가격별 체험 일수를 지정했다면, 신규 구독(이전에 구독한 적이 있던 고객도 포함)에는 항상 체험 기간이 주어집니다. 체험 기간을 생략하려면 반드시 `skipTrial()` 메서드를 호출해야 합니다.

<a name="without-payment-method-up-front"></a>

<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration: -->
결제 수단 정보 없이 체험 기간을 제공하고 싶다면, 사용자 레코드의 `trial_ends_at` 컬럼을 원하는 체험 종료일로 설정하면 됩니다. 보통 회원가입 시점에 이 작업이 이루어집니다.

```
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!NOTE]
> 청구 가능 모델 클래스 정의에 [date cast](/docs/8.x/eloquent-mutators##date-casting)에서 `trial_ends_at` 속성을 날짜로 변환하는 casting 설정을 꼭 추가하세요.

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the billable model instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
Cashier에서는 이런 체험을 '일반(generic) 체험'으로 부르며, 아직 실제 구독과 연결되지 않은 상태입니다. 청구 가능 모델 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 값보다 이전일 때 `true`를 반환합니다.

```
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
실제 구독을 생성할 준비가 되면, 평소와 같이 `newSubscription`을 이용하면 됩니다.

```
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription name parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
사용자의 체험 종료일을 조회하려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 체험 중이면 Carbon 날짜 인스턴스를, 아니면 `null`을 반환합니다. 기본 구독이 아닌 특정 구독의 종료일을 조회하고 싶으면, 인자로 구독 이름을 전달하면 됩니다.

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not yet created an actual subscription: -->
사용자가 아직 실제 구독을 생성하지 않고 "일반(generic) 체험" 상태인지 확인하려면, `onGenericTrial` 메서드를 사용할 수 있습니다.

```
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>

<!-- ### Extending Trials -->
### Extending Trials

<!-- The `extendTrial` method allows you to extend the trial period of a subscription after the subscription has been created. If the trial has already expired and the customer is already being billed for the subscription, you can still offer them an extended trial. The time spent within the trial period will be deducted from the customer's next invoice: -->
`extendTrial` 메서드를 이용하면 구독 생성 후에도 체험 기간을 연장할 수 있습니다. 이미 체험이 만료되어 유료 결제가 진행되고 있는 경우에도 추가로 체험 기간을 제공할 수 있으며, 체험 기간 동안은 청구가 일시 중단되고 다시 기간이 합산되어 차감됩니다.

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

> [!TIP]
> [the Stripe CLI](https://stripe.com/docs/stripe-cli)를 활용하면 로컬 개발 환경에서 웹훅 테스트를 쉽게 할 수 있습니다.

<!-- Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Stripe는 다양한 이벤트 상황을 웹훅을 통해 애플리케이션에 알려줄 수 있습니다. 기본적으로, Cashier 서비스 프로바이더는 Cashier의 웹훅 컨트롤러로 향하는 라우트를 자동으로 등록합니다. 이 컨트롤러가 모든 웹훅 요청을 처리합니다.

<!-- By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like. -->
Cashier의 웹훅 컨트롤러는 기본적으로 Stripe 설정에 따라 결제 실패가 누적된 구독 취소, 고객 정보/삭제, 구독 변경, 결제 수단 변경 등 주요 Stripe 웹훅을 자동 처리합니다. 하지만 필요에 따라 이 컨트롤러를 확장해 원하는 Stripe 웹훅 이벤트를 직접 처리할 수도 있습니다.

<!-- To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are: -->
웹훅 처리를 정상적으로 하려면 Stripe 관리콘솔의 웹훅 URL 설정에 해당 라우트가 등록되어 있어야 합니다. Cashier의 기본 웹훅 URL은 `/stripe/webhook`입니다. Stripe 관리 콘솔에서 반드시 다음 이벤트에 대한 웹훅을 활성화해야 합니다.

<!--
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `invoice.payment_action_required`
-->
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `invoice.payment_action_required`

<!-- For convenience, Cashier includes a `cashier:webhook` Artisan command. This command will create a webhook in Stripe that listens to all of the events required by Cashier: -->
편의를 위해 Cashier에서는 `cashier:webhook` Artisan 명령어를 제공합니다. 이 명령어를 실행하면 Cashier에 필요한 모든 이벤트를 청취하는 웹훅이 Stripe에 생성됩니다.

```
php artisan cashier:webhook
```

<!-- By default, the created webhook will point to the URL defined by the `APP_URL` environment variable and the `cashier.webhook` route that is included with Cashier. You may provide the `--url` option when invoking the command if you would like to use a different URL: -->
이 명령어로 생성된 웹훅의 URL은 `APP_URL` 환경 변수와 Cashier에 포함된 `cashier.webhook` 라우트를 기준으로 합니다. 명령어 실행 시 `--url` 옵션을 추가해 원하는 URL을 지정할 수 있습니다.

```
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

<!-- The webhook that is created will use the Stripe API version that your version of Cashier is compatible with. If you would like to use a different Stripe version, you may provide the `--api-version` option: -->
생성된 웹훅은, 현재 사용하는 Cashier가 호환되는 Stripe API 버전을 자동으로 사용합니다. 다른 Stripe 버전을 사용하고 싶다면, 명령어 실행 시 `--api-version` 옵션을 사용하세요.

```
php artisan cashier:webhook --api-version="2019-12-03"
```

<!-- After creation, the webhook will be immediately active. If you wish to create the webhook but have it disabled until you're ready, you may provide the `--disabled` option when invoking the command: -->
웹훅은 생성된 즉시 활성화됩니다. 웹훅을 생성하되 준비가 될 때까지 비활성화 상태로 두고 싶다면 `--disabled` 옵션을 사용할 수 있습니다.

```
php artisan cashier:webhook --disabled
```

> [!NOTE]
> Stripe 웹훅 요청이 들어올 때는 Cashier가 포함한 [webhook signature verification](#verifying-webhook-signatures) 미들웨어를 사용해 반드시 보호해야 합니다.

<a name="webhooks-csrf-protection"></a>

<!-- #### Webhooks & CSRF Protection -->
#### Webhooks & CSRF Protection

<!-- Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/8.x/csrf), be sure to list the URI as an exception in your application's `App\Http\Middleware\VerifyCsrfToken` middleware or list the route outside of the `web` middleware group: -->
Stripe 웹훅은 Laravel의 [CSRF protection](/docs/8.x/csrf)를 우회해야 하므로, 애플리케이션의 `App\Http\Middleware\VerifyCsrfToken` 미들웨어에 웹훅 URI를 예외로 등록하거나, 해당 라우트를 `web` 미들웨어 그룹 외부에 두어야 합니다.

```
protected $except = [
    'stripe/*',
];
```

<a name="defining-webhook-event-handlers"></a>

<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancellations for failed charges and other common Stripe webhook events. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier는 결제 실패로 인한 구독 취소 등 흔히 발생하는 Stripe 웹훅 이벤트를 자동 처리합니다. 추가적으로 직접 처리할 웹훅 이벤트가 있다면, Cashier가 디스패치하는 다음 이벤트들을 리스닝하여 구현할 수 있습니다.

<!--
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`
-->
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

<!-- Both events contain the full payload of the Stripe webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/8.x/events#defining-listeners) that will handle the event: -->
두 이벤트 모두 Stripe 웹훅의 전체 페이로드 정보를 담고 있습니다. 예를 들어 `invoice.payment_succeeded` 웹훅을 처리하고 싶다면, [listener](/docs/8.x/events#defining-listeners)를 등록해 이벤트를 처리할 수 있습니다.

```
<?php

namespace App\Listeners;

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    /**
     * Handle received Stripe webhooks.
     *
     * @param  \Laravel\Cashier\Events\WebhookReceived  $event
     * @return void
     */
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['type'] === 'invoice.payment_succeeded') {
            // Handle the incoming event...
        }
    }
}
```

<!-- Once your listener has been defined, you may register it within your application's `EventServiceProvider`: -->
리스너를 정의했다면, 애플리케이션의 `EventServiceProvider`에 등록하면 됩니다.

```
<?php

namespace App\Providers;

use App\Listeners\StripeEventListener;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Laravel\Cashier\Events\WebhookReceived;

class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        WebhookReceived::class => [
            StripeEventListener::class,
        ],
    ];
}
```

<a name="verifying-webhook-signatures"></a>

<!-- ### Verifying Webhook Signatures -->
### Verifying Webhook Signatures

<!-- To secure your webhooks, you may use [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures). For convenience, Cashier automatically includes a middleware which validates that the incoming Stripe webhook request is valid. -->
웹훅의 보안을 위해 [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures)를 사용할 수 있습니다. Cashier에서는 Stripe 웹훅 요청의 유효성을 검증하는 미들웨어를 자동으로 포함하고 있습니다.

<!-- To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is set in your application's `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard. -->
웹훅 검증을 활성화하려면, 애플리케이션의 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경 변수를 반드시 설정해야 합니다. Stripe 계정 대시보드에서 이 웹훅 `secret`을 확인할 수 있습니다.

<a name="single-charges"></a>

<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>

<!-- ### Simple Charge -->
### Simple Charge

> [!NOTE]
> `charge` 메서드는 결제하려는 금액을, 애플리케이션에서 사용하는 통화의 최소 단위로 입력해야 합니다. 예를 들어 달러(USD)를 사용하는 경우, 금액을 센트 단위(예: 100=1달러)로 지정해야 합니다.

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance. You will need to [provide a payment method identifier](#payment-methods-for-single-charges) as the second argument to the `charge` method: -->
한 번만 결제하는 일회성 청구를 하려면 청구 가능 모델 인스턴스의 `charge` 메서드를 사용하세요. [provide a payment method identifier](#payment-methods-for-single-charges)를 `charge` 메서드의 두 번째 인수로 전달해야 합니다.

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
`charge` 메서드는 옵션 배열을 세 번째 인자로 받을 수 있어, Stripe의 결제 생성 옵션을 자유롭게 넘길 수 있습니다. 사용 가능한 옵션의 전체 목록은 [Stripe documentation](https://stripe.com/docs/api/charges/create)에서 확인하세요.

```
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

<!-- You may also use the `charge` method without an underlying customer or user. To accomplish this, invoke the `charge` method on a new instance of your application's billable model: -->
고객 또는 사용자 정보 없이도 `charge` 메서드를 사용할 수 있습니다. 이럴 때는 애플리케이션의 청구 가능 모델 새 인스턴스에서 `charge`를 호출하면 됩니다.

```
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

<!-- The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method: -->
`charge` 메서드는 결제가 실패하면 예외를 발생시킵니다. 결제가 성공적으로 처리되면, `Laravel\Cashier\Payment` 인스턴스를 반환합니다.

```
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    //
}
```

<a name="charge-with-invoice"></a>

<!-- ### Charge With Invoice -->
### Charge With Invoice

<!-- Sometimes you may need to make a one-time charge and offer a PDF receipt to your customer. The `invoicePrice` method lets you do just that. For example, let's invoice a customer for five new shirts: -->
가끔 일회성 결제와 함께 PDF 영수증을 고객에게 제공해야 할 때가 있습니다. `invoicePrice` 메서드를 사용하면 이 작업을 손쉽게 처리할 수 있습니다. 예를 들어, 고객에게 새 셔츠 5벌에 대한 인보이스를 발급하려면 다음과 같이 할 수 있습니다.

```
$user->invoicePrice('price_tshirt', 5);
```

<!-- The invoice will be immediately charged against the user's default payment method. The `invoicePrice` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array which should contain the billing options for the invoice itself: -->
이 인보이스는 사용자 기본 결제수단으로 즉시 결제됩니다. `invoicePrice` 메서드는 세 번째 인수로 배열을 받을 수 있습니다. 이 배열에는 인보이스 항목의 청구 옵션을 전달합니다. 또한 네 번째 인수도 배열로 받아 인보이스 자체에 대한 청구 옵션을 지정합니다.

```
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

<!-- Alternatively, you may use the `invoiceFor` method to make a "one-off" charge against the customer's default payment method: -->
또는, `invoiceFor` 메서드를 사용해 고객의 기본 결제수단에 대해 "일회성" 청구를 할 수도 있습니다.

```
$user->invoiceFor('One Time Fee', 500);
```

<!-- Although the `invoiceFor` method is available for you to use, it is recommendeded that you use the `invoicePrice` method with pre-defined prices. By doing so, you will have access to better analytics and data within your Stripe dashboard regarding your sales on a per-product basis. -->
`invoiceFor` 메서드도 사용할 수 있지만, 미리 정의된 가격으로 `invoicePrice` 메서드를 사용하는 것이 더 권장되는 방법입니다. 이렇게 하면 Stripe 대시보드에서 제품별 매출에 대한 더 나은 분석 및 데이터를 얻을 수 있습니다.

> [!NOTE]
> `invoicePrice`와 `invoiceFor` 메서드는 실패한 결제 시 재시도되는 Stripe 인보이스를 생성합니다. 결제 실패 시 인보이스의 재시도를 원하지 않는다면, 첫 번째 결제 실패 이후 Stripe API를 사용해 인보이스를 닫아야 합니다.

<a name="refunding-charges"></a>

<!-- ### Refunding Charges -->
### Refunding Charges

<!-- If you need to refund a Stripe charge, you may use the `refund` method. This method accepts the Stripe [payment intent ID](#payment-methods-for-single-charges) as its first argument: -->
Stripe 결제를 환불해야 할 경우, `refund` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 Stripe의 [payment intent ID](#payment-methods-for-single-charges)를 받습니다.

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
빌링 가능한 모델의 인보이스 배열을 손쉽게 조회하려면 `invoices` 메서드를 사용합니다. `invoices` 메서드는 `Laravel\Cashier\Invoice` 인스턴스들로 이루어진 컬렉션을 반환합니다.

```
$invoices = $user->invoices();
```

<!-- If you would like to include pending invoices in the results, you may use the `invoicesIncludingPending` method: -->
결과에 미결 인보이스(아직 결제가 완료되지 않은 인보이스)를 포함하려면, `invoicesIncludingPending` 메서드를 사용할 수 있습니다.

```
$invoices = $user->invoicesIncludingPending();
```

<!-- You may use the `findInvoice` method to retrieve a specific invoice by its ID: -->
특정 인보이스를 ID로 찾아오고 싶다면 `findInvoice` 메서드를 사용할 수 있습니다.

```
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>

<!-- #### Displaying Invoice Information -->
#### Displaying Invoice Information

<!-- When listing the invoices for the customer, you may use the invoice's methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them: -->
고객의 인보이스 목록을 표시할 때, 각 인보이스의 메서드를 활용해 관련 정보를 출력할 수 있습니다. 예를 들어, 아래와 같이 모든 인보이스를 표로 나열해 사용자가 각 인보이스를 손쉽게 다운로드할 수 있도록 할 수 있습니다.

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
고객의 발행 예정(곧 정기 결제가 이루어질) 인보이스를 조회하려면 `upcomingInvoice` 메서드를 사용하면 됩니다.

```
$invoice = $user->upcomingInvoice();
```

<!-- Similary, if the customer has multiple subscriptions, you can also retrieve the upcoming invoice for a specific subscription: -->
고객이 여러 개의 구독을 가지고 있는 경우, 특정 구독의 발행 예정 인보이스도 다음과 같이 가져올 수 있습니다.

```
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>

<!-- ### Previewing Subscription Invoice -->
### Previewing Subscription Invoice

<!-- Using the `previewInvoice` method, you can preview an invoice before making price changes. This will allow you to determine what your customer's invoice will look like when a given price change is made: -->
`previewInvoice` 메서드를 사용하면 가격 변경 전에 인보이스를 미리 볼 수 있습니다. 이를 통해 사용자가 특정 가격 변경이 적용됐을 때 실제 결제 청구서가 어떻게 보일지 확인할 수 있습니다.

```
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

<!-- You may pass an array of prices to the `previewInvoice` method in order to preview invoices with multiple new prices: -->
`previewInvoice` 메서드에 가격 배열을 전달하면, 여러 새로운 가격이 반영된 인보이스를 미리 볼 수 있습니다.

```
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>

<!-- ### Generating Invoice PDFs -->
### Generating Invoice PDFs

<!-- From within a route or controller, you may use the `downloadInvoice` method to generate a PDF download of a given invoice. This method will automatically generate the proper HTTP response needed to download the invoice: -->
라우트나 컨트롤러에서 `downloadInvoice` 메서드를 사용해 특정 인보이스의 PDF 파일을 다운로드하도록 할 수 있습니다. 이 메서드는 인보이스 다운로드에 필요한 적절한 HTTP 응답을 자동으로 생성해 반환합니다.

```
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId, [
        'vendor' => 'Your Company',
        'product' => 'Your Product',
    ]);
});
```

<!-- By default, all data on the invoice is derived from the customer and invoice data stored in Stripe. However, you can customize some of this data by providing an array as the second argument to the `downloadInvoice` method. This array allows you to customize information such as your company and product details: -->
기본적으로 인보이스의 모든 데이터는 Stripe에 저장된 고객 및 인보이스 정보를 바탕으로 구성됩니다. 하지만, `downloadInvoice`의 두 번째 인수로 배열을 전달해 회사명, 제품명 등 일부 정보를 커스터마이즈할 수 있습니다.

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
], 'my-invoice');
```

<!-- The `downloadInvoice` method also allows for a custom filename via its third argument. This filename will automatically be suffixed with `.pdf`: -->
`downloadInvoice` 메서드는 세 번째 인수로 파일명을 직접 지정할 수도 있습니다. 지정한 파일명 뒤에 자동으로 `.pdf`가 붙습니다.

```
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>

<!-- #### Custom Invoice Renderer -->
#### Custom Invoice Renderer

<!-- Cashier also makes it possible to use a custom invoice renderer. By default, Cashier uses the `DompdfInvoiceRenderer` implementation, which utilizes the [dompdf](https://github.com/dompdf/dompdf) PHP library to generate Cashier's invoices. However, you may use any renderer you wish by implementing the `Laravel\Cashier\Contracts\InvoiceRenderer` interface. For example, you may wish to render an invoice PDF using an API call to a third-party PDF rendering service: -->
Cashier에서는 커스텀 인보이스 렌더러 사용도 지원합니다. 기본적으로 Cashier는 [dompdf](https://github.com/dompdf/dompdf) PHP 라이브러리를 활용하는 `DompdfInvoiceRenderer` 구현체를 사용하지만, 필요한 경우 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현해 원하는 렌더러를 만들 수 있습니다. 예를 들어, 외부 PDF 렌더링 API를 통해 인보이스 PDF를 생성하려고 할 때 다음과 같이 구현할 수 있습니다.

```
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * Render the given invoice and return the raw PDF bytes.
     *
     * @param  \Laravel\Cashier\Invoice. $invoice
     * @param  array  $data
     * @param  array  $options
     * @return string
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

<!-- Once you have implemented the invoice renderer contract, you should update the `cashier.invoices.renderer` configuration value in your application's `config/cashier.php` configuration file. This configuration value should be set to the class name of your custom renderer implementation. -->
이렇게 커스텀 인보이스 렌더러를 구현했다면, 애플리케이션의 `config/cashier.php` 설정 파일에서 `cashier.invoices.renderer` 값을 해당 클래스명으로 수정해야 합니다. 이 설정값에 커스텀 렌더러 구현체의 클래스명을 지정하세요.

<a name="checkout"></a>

<!-- ## Checkout -->
## Checkout

<!-- Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page. -->
Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout)도 지원합니다. Stripe Checkout은 미리 만들어진 호스팅 결제 페이지를 제공하므로 커스텀 결제 페이지를 직접 개발하지 않아도 손쉽게 결제 기능을 도입할 수 있습니다.

<!-- The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout). -->
이 섹션에서는 Cashier와 Stripe Checkout을 연동하는 방법을 설명합니다. Stripe Checkout에 대한 더 자세한 설명은 [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout)도 참고해 주세요.

<a name="product-checkouts"></a>

<!-- ### Product Checkouts -->
### Product Checkouts

<!-- You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID: -->
Stripe 대시보드에서 생성한 기존 상품에 대해 체크아웃을 진행하려면, 빌링 모델에서 `checkout` 메서드를 사용하면 됩니다. `checkout` 메서드는 Stripe Checkout 세션을 시작합니다. 기본적으로는 Stripe 가격 ID(Price ID)를 전달해야 합니다.

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

<!-- If needed, you may also specify a product quantity: -->
필요하다면 제품의 수량도 함께 지정할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

<!-- When a customer visits this route they will be redirected to Stripe's Checkout page. By default, when a user successfully completes or cancels a purchase they will be redirected to your `home` route location, but you may specify custom callback URLs using the `success_url` and `cancel_url` options: -->
고객이 해당 라우트에 접속하면 Stripe의 Checkout 페이지로 리디렉션됩니다. 기본적으로 결제 성공 또는 취소 후에는 애플리케이션의 `home` 라우트로 리디렉션되지만, `success_url`과 `cancel_url` 옵션을 지정해 콜백 URL을 직접 설정할 수 있습니다.

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
`success_url` 체크아웃 옵션을 정의할 때, URL의 쿼리 문자열에 체크아웃 세션 ID를 추가하도록 Stripe에 요청할 수도 있습니다. 이를 위해 `success_url` 쿼리스트링에 `{CHECKOUT_SESSION_ID}` 라는 리터럴 문자열을 추가하면 Stripe가 이 플레이스홀더를 실제 체크아웃 세션 ID로 대체합니다.

```
use Illuminate\Http\Request;
use Stripe\Checkout\Session;
use Stripe\Customer;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('checkout-success') . '?session_id={CHECKOUT_SESSION_ID}',
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
기본적으로 Stripe Checkout에서는 [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 지원하지 않습니다. 다행히, Cashier에서는 `allowPromotionCodes` 메서드를 호출해 이 기능을 쉽게 활성화할 수 있습니다.

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
Stripe 대시보드에 등록되지 않은 임시 상품에 대해 단순 결제를 진행할 수도 있습니다. 이때는 빌링 모델에서 `checkoutCharge` 메서드를 사용하고, 결제 금액, 상품명, 옵션으로 수량을 전달하면 됩니다. 고객이 이 라우트로 접속하면 Stripe Checkout 페이지로 리디렉션됩니다.

```
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!NOTE]
> `checkoutCharge` 메서드를 사용할 경우 Stripe는 Stripe 대시보드에 새로운 상품과 가격을 항상 생성합니다. 이에 따라, 미리 Stripe 대시보드에서 상품을 생성해 두고 되도록 `checkout` 메서드를 사용할 것을 권장합니다.

<a name="subscription-checkouts"></a>

<!-- ### Subscription Checkouts -->
### Subscription Checkouts

> [!NOTE]
> Stripe Checkout으로 구독을 생성하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 반드시 활성화해야 합니다. 이 웹훅은 데이터베이스에 구독 레코드를 생성하고, 관련 구독 항목 정보를 모두 저장합니다.

<!-- You may also use Stripe Checkout to initiate subscriptions. After defining your subscription with Cashier's subscription builder methods, you may call the `checkout `method. When a customer visits this route they will be redirected to Stripe's Checkout page: -->
Stripe Checkout을 활용하여 구독을 시작할 수도 있습니다. 먼저 Cashier의 구독 빌더 메서드를 사용해 구독을 정의한 후, `checkout `메서드를 호출하면 됩니다. 고객은 해당 라우트에 접속하면 Stripe Checkout 페이지로 이동합니다.

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

<!-- Just as with product checkouts, you may customize the success and cancellation URLs: -->
상품 체크아웃과 동일하게, 결제 성공·실패(취소) 시 리디렉션될 URL을 직접 지정할 수도 있습니다.

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
그리고, 구독 체크아웃에도 프로모션 코드 사용을 활성화할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->allowPromotionCodes()
        ->checkout();
});
```

> [!NOTE]
> Stripe Checkout에서 구독을 시작할 때 일부 구독 청구 옵션은 지원되지 않습니다. 예를 들어 `anchorBillingCycleOn` 메서드 사용, 비례 배분 옵션(proration behavior) 지정, 결제 방식(payment behavior) 지정 등은 Stripe Checkout 세션에서는 동작하지 않습니다. 지원되는 세부 파라미터들은 [the Stripe Checkout Session API documentation](https://stripe.com/docs/api/checkout/sessions/create)를 참고하세요.

<a name="stripe-checkout-trial-periods"></a>

<!-- #### Stripe Checkout & Trial Periods -->
#### Stripe Checkout & Trial Periods

<!-- Of course, you can define a trial period when building a subscription that will be completed using Stripe Checkout: -->
Stripe Checkout을 통한 구독 생성 시에도 체험 기간(trial period)을 정의할 수 있습니다.

```
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<!-- However, the trial period must be at least 48 hours, which is the minimum amount of trial time supported by Stripe Checkout. -->
단, 체험 기간은 최소 48시간 이상이어야 하며, 이는 Stripe Checkout이 지원하는 최소 체험 기간입니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>

<!-- #### Subscriptions & Webhooks -->
#### Subscriptions & Webhooks

<!-- Remember, Stripe and Cashier update subscription statuses via webhooks, so there's a possibility a subscription might not yet be active when the customer returns to the application after entering their payment information. To handle this scenario, you may wish to display a message informing the user that their payment or subscription is pending. -->
Stripe와 Cashier는 웹훅을 사용해 구독 상태를 갱신하기 때문에, 고객이 결제 정보를 입력한 후 애플리케이션으로 돌아왔을 때 구독이 아직 활성화되지 않은 경우도 있습니다. 이런 상황을 처리하려면, 결제 또는 구독이 보류 중(pending)임을 사용자에게 안내하는 메시지를 띄우는 것이 좋습니다.

<a name="collecting-tax-ids"></a>

<!-- ### Collecting Tax IDs -->
### Collecting Tax IDs

<!-- Checkout also supports collecting a customer's Tax ID. To enable this on a checkout session, invoke the `collectTaxIds` method when creating the session: -->
Checkout 세션에서는 고객의 세금 ID(Tax ID)도 수집할 수 있습니다. 이를 활성화하려면 Checkout 세션 생성 시 `collectTaxIds` 메서드를 호출하면 됩니다.

```
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

<!-- When this method is invoked, a new checkbox will be available to the customer that allows them to indicate if they're purchasing as a company. If so, they will have the opportunity to provide their Tax ID number. -->
이 메서드를 사용하면, 고객이 회사로 구매하는 경우임을 표시하고 해당 세금 ID 번호를 입력할 수 있는 새로운 체크박스가 결제 페이지에 나타납니다.

> [!NOTE]
> 이미 애플리케이션의 서비스 프로바이더에서 [automatic tax collection](#tax-configuration)를 설정했다면, 이 기능은 자동으로 활성화되므로 `collectTaxIds` 메서드를 별도로 호출할 필요가 없습니다.

<a name="handling-failed-payments"></a>

<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed. -->
때때로 구독 또는 일회성 결제가 실패할 수 있습니다. 이런 경우 Cashier에서는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시켜 결제 실패를 알려줍니다. 이 예외를 캐치한 후에는, 다음 두 가지 중 한 가지 방식으로 후속 처리를 할 수 있습니다.

<!-- First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page: -->
첫 번째 방법은 고객을 전용 결제 확인(confirmation) 페이지로 리디렉션하는 것입니다. 이 페이지는 Cashier에 내장되어 있으며, Cashier의 서비스 프로바이더를 통해 이미 명명된 라우트가 등록됩니다. 따라서, `IncompletePayment` 예외를 캐치하여 사용자를 결제 확인 페이지로 리디렉션하면 됩니다.

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
결제 확인 페이지에서는 고객이 신용카드 정보를 다시 입력하고, Stripe에서 요구하는 추가 인증(예: "3D Secure" 확인 등) 과정을 거치게 됩니다. 결제가 정상적으로 확인되면, 사용자는 위에서 전달한 `redirect` 파라미터의 URL로 리디렉션됩니다. 이때 쿼리스트링에는 `message`(문자열)와 `success`(정수) 변수도 함께 전달됩니다. 현재 결제 페이지에서는 다음과 같은 결제 수단을 지원합니다.

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
- BECS 직접 출금
- EPS
- Giropay
- iDEAL
- SEPA 직접 출금

<!-- </div> -->
</div>

<!-- Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions. -->
다른 방법으로는 Stripe가 결제 확인 절차를 대신 처리하도록 맡길 수도 있습니다. 이 경우, 결제 확인 페이지로 리디렉션하지 않고 [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) 기능을 Stripe 대시보드에서 활성화하면 됩니다. 하지만, 여전히 `IncompletePayment` 예외가 발생한 경우 사용자에게 결제 확인 안내 메일을 수신하게 된다는 점을 반드시 안내해야 합니다.

<!-- Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions. -->
결제 예외는 `Billable` 트레이트를 사용하는 모델에서 `charge`, `invoiceFor`, `invoice` 메서드를 호출할 때 발생할 수 있습니다. 구독 관련 작업의 경우, `SubscriptionBuilder`의 `create` 메서드, `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice`와 `swapAndInvoice` 메서드에서도 결제 미완료 예외가 발생할 수 있습니다.

<!-- Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
기존 구독이 미완료(incomplete) 결제 상태인지 확인하려면, 빌링 가능한 모델이나 구독 인스턴스에서 `hasIncompletePayment` 메서드를 호출하면 됩니다.

```
if ($user->hasIncompletePayment('default')) {
    //
}

if ($user->subscription('default')->hasIncompletePayment()) {
    //
}
```

<!-- You can derive the specific status of an incomplete payment by inspecting the `payment` property on the exception instance: -->
예외 인스턴스의 `payment` 프로퍼티를 확인하여 미완료 결제의 구체적인 상태를 파악할 수도 있습니다.

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

<a name="strong-customer-authentication"></a>

<!-- ## Strong Customer Authentication -->
## Strong Customer Authentication

<!-- If your business or one of your customers is based in Europe you will need to abide by the EU's Strong Customer Authentication (SCA) regulations. These regulations were imposed in September 2019 by the European Union to prevent payment fraud. Luckily, Stripe and Cashier are prepared for building SCA compliant applications. -->
비즈니스 또는 고객 중 유럽에 기반을 둔 경우, EU의 강력한 고객 인증(Strong Customer Authentication, SCA) 규정을 준수해야 합니다. 이 규정은 2019년 9월부터 유럽연합(EU)에서 결제 사기 방지를 위해 시행되고 있습니다. 다행히 Stripe와 Cashier는 SCA를 준수하는 애플리케이션 개발을 지원하도록 준비되어 있습니다.

> [!NOTE]
> 시작 전, [Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication)와 [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication)를 반드시 참고하시기 바랍니다.

<a name="payments-requiring-additional-confirmation"></a>

<!-- ### Payments Requiring Additional Confirmation -->
### Payments Requiring Additional Confirmation

<!-- SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions be found can be found in the documentation on [handling failed payments](#handling-failed-payments). -->
SCA 규정에 따라 결제 시 추가 인증이 요구되는 경우가 많습니다. 이런 상황이 발생하면 Cashier에서 `Laravel\Cashier\Exceptions\IncompletePayment` 예외가 발생해 추가 인증이 필요함을 알려줍니다. 예외 처리 방법은 [handling failed payments](#handling-failed-payments) 섹션에서 상세히 안내하고 있습니다.

<!-- Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
Stripe 또는 Cashier에서 표시하는 결제 확인 화면은 결제 은행이나 카드 발급사가 요구하는 결제 흐름에 맞춰 조정될 수 있으며, 카드 추가 확인, 소액 임시 결제, 별도의 기기 인증 등 다양한 추가 인증 방식이 포함될 수 있습니다.

<a name="incomplete-and-past-due-state"></a>

<!-- #### Incomplete and Past Due State -->
#### Incomplete and Past Due State

<!-- When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion. -->
추가 인증이 필요한 결제가 발생하면, 구독은 `stripe_status` 데이터베이스 컬럼 값으로 `incomplete` 또는 `past_due` 상태로 유지됩니다. Cashier는 Stripe로부터 결제 완료 웹훅을 받아 인증이 완료된 즉시 자동으로 해당 구독을 활성화합니다.

<!-- For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status). -->
`incomplete` 및 `past_due` 상태에 대한 자세한 정보는 [our additional documentation on these states](#incomplete-and-past-due-status)를 참고하세요.

<a name="off-session-payment-notifications"></a>

<!-- ### Off-Session Payment Notifications -->
### Off-Session Payment Notifications

<!-- Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to a notification class. By default, this notification is disabled. Of course, Cashier includes a notification class you may use for this purpose, but you are free to provide your own notification class if desired: -->
SCA 규정에 따라, 구독이 활성 상태라 하더라도 고객이 가끔 결제 정보를 재확인해야 할 수 있습니다. 예를 들어 구독 결제가 갱신될 때 이런 일이 발생할 수 있습니다. Cashier에서는 오프세션 결제 확인이 요구될 때 고객에게 알림을 전송할 수 있습니다. Cashier에서는 이 알림 클래스를 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수로 지정하여 활성화할 수 있으며, 기본적으로는 비활성화되어 있습니다. Cashier에서 기본으로 제공하는 알림 클래스를 써도 되고, 필요한 경우 직접 구현할 수도 있습니다.

```
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

<!-- To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait. -->
오프세션 결제 확인 알림이 정상적으로 전송되려면, [Stripe webhooks are configured](#handling-stripe-webhooks)이 완료되어 있어야 하고, Stripe 대시보드에서 `invoice.payment_action_required` 웹훅도 활성화되어야 합니다. 또한, `Billable` 모델이 Laravel의 `Illuminate\Notifications\Notifiable` 트레이트도 사용하고 있어야 합니다.

> [!NOTE]
> 추가 인증이 필요한 결제를 고객이 직접 진행할 때도 알림이 전송됩니다. Stripe에서는 결제가 수동(수기)으로 이루어졌는지, 오프세션 결제인지 구분할 수 없습니다. 따라서 고객이 결제 페이지를 이미 확인한 뒤 방문하더라도 단순히 "결제 성공" 메시지 하나만 표시됩니다. 동일한 결제를 두 번 확정해 이중 결제가 발생하는 일은 없으니 안심하셔도 됩니다.

<a name="stripe-sdk"></a>

<!-- ## Stripe SDK -->
## Stripe SDK

<!-- Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method: -->
Cashier의 여러 객체들은 Stripe SDK 객체를 감싸는(wrapper) 형식으로 동작합니다. Stripe 객체를 직접 다뤄야 할 경우, `asStripe` 메서드를 사용해 쉽게 접근할 수 있습니다.

```
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

<!-- You may also use the `updateStripeSubscription` method to update a Stripe subscription directly: -->
Stripe 구독 객체를 직접 업데이트하려면 `updateStripeSubscription` 메서드를 사용할 수 있습니다.

```
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

<!-- You may invoke the `stripe` method on the `Cashier` class if you would like to use the `Stripe\StripeClient` client directly. For example, you could use this method to access the `StripeClient` instance and retrieve a list of prices from your Stripe account: -->
`Stripe\StripeClient` 클라이언트를 직접 사용하고 싶다면 `Cashier` 클래스의 `stripe` 메서드를 호출하면 됩니다. 예를 들어, 이 메서드로 `StripeClient` 인스턴스에 접근해 Stripe 계정의 가격 목록을 가져올 수 있습니다.

```
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>

<!-- ## Testing -->
## Testing

<!-- When testing an application that uses Cashier, you may mock the actual HTTP requests to the Stripe API; however, this requires you to partially re-implement Cashier's own behavior. Therefore, we recommend allowing your tests to hit the actual Stripe API. While this is slower, it provides more confidence that your application is working as expected and any slow tests may be placed within their own PHPUnit testing group. -->
Cashier를 사용하는 애플리케이션을 테스트할 때 Stripe API로 실제 HTTP 요청을 보내는 대신 mocking(가짜 응답 처리)을 할 수도 있지만, 이 경우 Cashier의 동작을 직접 일부분 재구현해야 합니다. 따라서, Cashier 기반 테스트는 실제 Stripe API와 통신하도록 두는 방법을 권장합니다. 이 경우 속도는 느릴 수 있지만, 실제 환경과 동일하게 동작하는지 제대로 검증할 수 있으며, 느린 테스트는 별도의 PHPUnit 테스트 그룹으로 분리해 운영하는 것이 좋습니다.

<!-- When testing, remember that Cashier itself already has a great test suite, so you should only focus on testing the subscription and payment flow of your own application and not every underlying Cashier behavior. -->
테스트를 작성할 때 Cashier 자체는 이미 우수한 테스트 스위트를 포함하고 있으니, 애플리케이션 내 구독·결제 흐름에만 집중해 테스트 코드를 작성하면 됩니다.

<!-- To get started, add the **testing** version of your Stripe secret to your `phpunit.xml` file: -->
먼저, `phpunit.xml` 파일에 **테스트용** Stripe 비밀키를 추가하세요.

```
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

<!-- Now, whenever you interact with Cashier while testing, it will send actual API requests to your Stripe testing environment. For convenience, you should pre-fill your Stripe testing account with subscriptions / prices that you may use during testing. -->
이제 Cashier와 상호작용하는 테스트는 실제 Stripe 테스트 환경으로 API 요청을 전송하게 됩니다. 편의를 위해, 미리 Stripe 테스트 계정에 구독이나 가격을 등록해두고 활용하는 것이 좋습니다.

> [!TIP]
> 카드 결제 거절, 결제 실패 등 다양한 시나리오를 테스트하려면, Stripe에서 제공하는 [testing card numbers and tokens](https://stripe.com/docs/testing)을 자유롭게 활용할 수 있습니다.
