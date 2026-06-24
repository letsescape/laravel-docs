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
    - [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)
    - [Multiple Subscriptions](#multiple-subscriptions)
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
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [Payments Requiring Additional Confirmation](#payments-requiring-additional-confirmation)
    - [Off-session Payment Notifications](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [Testing](#testing)

<a name="introduction"></a>

<!-- ## Introduction -->
## Introduction

<!-- [Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe) provides an expressive, fluent interface to [Stripe's](https://stripe.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs. -->
[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe's](https://stripe.com)의 구독 결제 서비스를 쉽고 유연하게 사용할 수 있도록 하는 직관적인 인터페이스를 제공합니다. Cashier는 여러분이 작성하기 번거로울 수 있는 구독 결제 관련 기본 코드를 대부분 대신 처리해줍니다. 기본적인 구독 관리 외에도, Cashier는 쿠폰, 구독 변경, 구독 "수량", 구독 취소 유예 기간, 인보이스 PDF 생성 등 다양한 기능을 제공합니다.

<a name="upgrading-cashier"></a>

<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md). -->
Cashier를 새로운 버전으로 업그레이드할 때는 반드시 [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

> [!WARNING]
> 중요한 변경 사항을 방지하기 위해, Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 14는 Stripe API 버전 `2022-11-15`를 사용합니다. Stripe API 버전은 Stripe의 새로운 기능과 개선 사항을 활용하기 위해 소규모 릴리스에서 업데이트될 수 있습니다.

<a name="installation"></a>

<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Stripe using the Composer package manager: -->
먼저, Composer 패키지 관리자를 사용하여 Stripe용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier
```

> [!WARNING]
> Cashier가 Stripe의 모든 이벤트를 제대로 처리할 수 있도록 반드시 [set up Cashier's webhook handling](#handling-stripe-webhooks)을 진행해야 합니다.

<a name="database-migrations"></a>

<!-- ### Database Migrations -->
### Database Migrations

<!-- Cashier's service provider registers its own database migration directory, so remember to migrate your database after installing the package. The Cashier migrations will add several columns to your `users` table as well as create a new `subscriptions` table to hold all of your customer's subscriptions: -->
Cashier의 서비스 프로바이더는 자체 마이그레이션 디렉토리를 등록하므로, 패키지를 설치한 후에는 데이터베이스 마이그레이션을 꼭 실행해야 합니다. Cashier 마이그레이션은 여러분의 `users` 테이블에 여러 컬럼을 추가하고, 고객의 구독 정보를 저장할 `subscriptions` 테이블을 새롭게 생성합니다.

```shell
php artisan migrate
```

<!-- If you need to overwrite the migrations that ship with Cashier, you can publish them using the `vendor:publish` Artisan command: -->
Cashier에서 기본 제공하는 마이그레이션을 직접 수정하려면, `vendor:publish` Artisan 명령어를 사용해 마이그레이션 파일을 퍼블리시할 수 있습니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- If you would like to prevent Cashier's migrations from running entirely, you may use the `ignoreMigrations` method provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
Cashier의 마이그레이션을 아예 실행하지 않도록 하려면, Cashier에서 제공하는 `ignoreMigrations` 메서드를 사용할 수 있습니다. 이 메서드는 일반적으로 여러분의 `AppServiceProvider`의 `register` 메서드 내부에서 호출해야 합니다.

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

> [!WARNING]
> Stripe에서는 Stripe 식별자를 저장하는 컬럼에 대하여 대소문자 구분을 권장합니다. 따라서 MySQL을 사용할 때 `stripe_id` 컬럼의 collation이 `utf8_bin`으로 설정되어 있는지 확인해야 합니다. 보다 자세한 내용은 [Stripe documentation](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하십시오.

<a name="configuration"></a>

<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>

<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, add the `Billable` trait to your billable model definition. Typically, this will be the `App\Models\User` model. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information: -->
Cashier를 사용하기 전에, 과금 모델 정의에 `Billable` 트레이트를 추가해야 합니다. 일반적으로 이 모델은 `App\Models\User`가 됩니다. 해당 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 일반적인 과금 작업을 간편하게 수행할 수 있도록 다양한 메서드를 제공합니다.

```
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- Cashier assumes your billable model will be the `App\Models\User` class that ships with Laravel. If you wish to change this you may specify a different model via the `useCustomerModel` method. This method should typically be called in the `boot` method of your `AppServiceProvider` class: -->
Cashier는 과금 모델이 Laravel에서 기본 제공되는 `App\Models\User` 클래스라고 가정합니다. 만약 이를 변경하고 싶다면, `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 보통 이 메서드는 여러분의 `AppServiceProvider` 클래스의 `boot` 메서드에 추가하면 됩니다.

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

> [!WARNING]
> Laravel에서 기본 제공하는 `App\Models\User` 모델이 아닌 다른 모델을 사용하는 경우, Cashier에서 제공하는 [Cashier migrations](#installation)하여 새로운 모델의 테이블 명에 맞게 변경해야 합니다.

<a name="api-keys"></a>

<!-- ### API Keys -->
### API Keys

<!-- Next, you should configure your Stripe API keys in your application's `.env` file. You can retrieve your Stripe API keys from the Stripe control panel: -->
다음으로, 애플리케이션의 `.env` 파일에 Stripe API 키를 설정해야 합니다. Stripe API 키는 Stripe 관리 페이지에서 발급받을 수 있습니다.

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 반드시 정의되어 있어야 합니다. 이 변수는 웹훅이 실제로 Stripe로부터 온 것인지 확인하는 데 사용됩니다.

<a name="currency-configuration"></a>

<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정하면 됩니다.

```ini
CASHIER_CURRENCY=eur
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
Cashier의 통화 설정 외에도, 인보이스에 표시될 금액 포맷을 위한 로케일(locale)을 설정할 수도 있습니다. 내부적으로 Cashier는 [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php)를 사용하여 통화 로케일을 지정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 프로그램이 설치되고 설정되어 있어야 합니다.

<a name="tax-configuration"></a>

<!-- ### Tax Configuration -->
### Tax Configuration

<!-- Thanks to [Stripe Tax](https://stripe.com/tax), it's possible to automatically calculate taxes for all invoices generated by Stripe. You can enable automatic tax calculation by invoking the `calculateTaxes` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
[Stripe Tax](https://stripe.com/tax)를 통해 Stripe에서 생성된 모든 인보이스에 대해 세금을 자동으로 계산할 수 있습니다. 자동 세금 계산을 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하면 됩니다.

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
세금 계산을 활성화하면, 생성되는 모든 새로운 구독(Subscription)과 단일 인보이스에 대해 자동으로 세금이 계산됩니다.

<!-- For this feature to work properly, your customer's billing details, such as the customer's name, address, and tax ID, need to be synced to Stripe. You may use the [customer data synchronization](#syncing-customer-data-with-stripe) and [Tax ID](#tax-ids) methods offered by Cashier to accomplish this. -->
이 기능이 제대로 작동하려면, 고객의 이름, 주소, 세금 ID 등 결제 관련 세부 정보가 Stripe에 동기화되어 있어야 합니다. Cashier가 제공하는 [customer data synchronization](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 기능을 사용해 이 작업을 할 수 있습니다.

> [!WARNING]
> [single charges](#single-charges)나 [single charge checkouts](#single-charge-checkouts)에는 세금이 계산되지 않습니다.

<a name="logging"></a>

<!-- ### Logging -->
### Logging

<!-- Cashier allows you to specify the log channel to be used when logging fatal Stripe errors. You may specify the log channel by defining the `CASHIER_LOGGER` environment variable within your application's `.env` file: -->
Cashier에서는 Stripe에서 발생하는 치명적인(fatal) 오류를 로깅할 때 사용할 로그 채널을 지정할 수 있습니다. `.env` 파일에서 `CASHIER_LOGGER` 환경 변수를 설정하여 로그 채널을 지정하세요.

```ini
CASHIER_LOGGER=stack
```

<!-- Exceptions that are generated by API calls to Stripe will be logged through your application's default log channel. -->
Stripe API 호출로 인해 발생하는 예외는 애플리케이션의 기본 로그 채널을 통해 로그로 기록됩니다.

<a name="using-custom-models"></a>

<!-- ### Using Custom Models -->
### Using Custom Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
Cashier가 내부적으로 사용하는 모델을 직접 확장해서 사용할 수도 있습니다. 여러분만의 커스텀 모델을 정의하고, 해당 모델이 Cashier 모델을 상속하도록 만드면 됩니다.

```
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Cashier\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
모델을 정의한 후에는, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier가 여러분의 커스텀 모델을 사용하도록 설정할 수 있습니다. 일반적으로 해당 설정은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 진행하면 됩니다.

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
`Cashier::findBillable` 메서드를 사용하면 Stripe ID를 기준으로 고객을 조회할 수 있습니다. 이 메서드는 과금 모델의 인스턴스를 반환합니다.

```
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>

<!-- ### Creating Customers -->
### Creating Customers

<!-- Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method: -->
가끔은 구독을 시작하지 않고 Stripe 고객만 먼저 생성하고 싶을 수 있습니다. 이럴 때는 `createAsStripeCustomer` 메서드를 사용할 수 있습니다.

```
$stripeCustomer = $user->createAsStripeCustomer();
```

<!-- Once the customer has been created in Stripe, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create): -->
고객이 Stripe에 생성된 후에는 나중에 구독을 시작할 수 있습니다. 필요하다면 `$options` 배열을 추가로 전달하여 [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create)를 지정할 수 있습니다.

```
$stripeCustomer = $user->createAsStripeCustomer($options);
```

<!-- You may use the `asStripeCustomer` method if you want to return the Stripe customer object for a billable model: -->
과금 모델에 연결된 Stripe 고객 객체를 반환하려면 `asStripeCustomer` 메서드를 사용할 수 있습니다.

```
$stripeCustomer = $user->asStripeCustomer();
```

<!-- The `createOrGetStripeCustomer` method may be used if you would like to retrieve the Stripe customer object for a given billable model but are not sure whether the billable model is already a customer within Stripe. This method will create a new customer in Stripe if one does not already exist: -->
주어진 과금 모델이 Stripe의 고객인지 확실치 않은 경우에는 `createOrGetStripeCustomer` 메서드를 사용할 수 있습니다. 이 메서드는 Stripe에 고객이 이미 존재하면 그 객체를, 없으면 새로 생성하여 반환합니다.

```
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>

<!-- ### Updating Customers -->
### Updating Customers

<!-- Occasionally, you may wish to update the Stripe customer directly with additional information. You may accomplish this using the `updateStripeCustomer` method. This method accepts an array of [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update): -->
때때로 Stripe의 고객 정보를 직접 추가로 업데이트하고 싶을 수 있습니다. 이때는 `updateStripeCustomer` 메서드를 사용하세요. 이 메서드는 [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update)을 배열로 받아 처리합니다.

```
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>

<!-- ### Balances -->
### Balances

<!-- Stripe allows you to credit or debit a customer's "balance". Later, this balance will be credited or debited on new invoices. To check the customer's total balance you may use the `balance` method that is available on your billable model. The `balance` method will return a formatted string representation of the balance in the customer's currency: -->
Stripe에서는 고객의 "잔액"을 충전(적립)하거나 차감할 수 있습니다. 나중에 이 잔액은 신규 인보이스에서 사용되거나 차감됩니다. 해당 고객의 잔액 총액을 확인하려면, 과금 모델에서 `balance` 메서드를 사용할 수 있습니다. `balance` 메서드는 고객 통화 기준으로 포매팅된 잔액 문자열을 반환합니다.

```
$balance = $user->balance();
```

<!-- To credit a customer's balance, you may provide a value to the `creditBalance` method. If you wish, you may also provide a description: -->
고객의 잔액을 충전하려면 `creditBalance` 메서드에 값을 전달합니다. 원하는 경우 설명(Description)도 함께 추가할 수 있습니다.

```
$user->creditBalance(500, 'Premium customer top-up.');
```

<!-- Providing a value to the `debitBalance` method will debit the customer's balance: -->
`debitBalance` 메서드에 값을 전달하면 고객의 잔액이 차감됩니다.

```
$user->debitBalance(300, 'Bad usage penalty.');
```

<!-- The `applyBalance` method will create new customer balance transactions for the customer. You may retrieve these transaction records using the `balanceTransactions` method, which may be useful in order to provide a log of credits and debits for the customer to review: -->
`applyBalance` 메서드는 고객에게 새로운 잔액 거래(트랜잭션)를 생성합니다. 이런 거래 내역들은 `balanceTransactions` 메서드로 조회할 수 있으며, 고객에게 충전과 차감 내역의 로그 화면을 제공하고 싶을 때 유용합니다.

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
Cashier를 이용하면 고객의 세금 ID를 쉽게 관리할 수 있습니다. 예를 들어, `taxIds` 메서드를 사용하면, 고객에게 할당된 [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션 형태로 받아올 수 있습니다.

```
$taxIds = $user->taxIds();
```

<!-- You can also retrieve a specific tax ID for a customer by its identifier: -->
또한, 식별자를 이용해 특정 세금 ID를 조회할 수 있습니다.

```
$taxId = $user->findTaxId('txi_belgium');
```

<!-- You may create a new Tax ID by providing a valid [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) and value to the `createTaxId` method: -->
유효한 [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 입력해 `createTaxId` 메서드로 새로운 세금 ID를 만들 수도 있습니다.

```
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

<!-- The `createTaxId` method will immediately add the VAT ID to the customer's account. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); however, this is an asynchronous process. You can be notified of verification updates by subscribing to the `customer.tax_id.updated` webhook event and inspecting [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). For more information on handling webhooks, please consult the [documentation on defining webhook handlers](#handling-stripe-webhooks). -->
`createTaxId` 메서드는 즉시 해당 VAT ID를 고객 계정에 추가합니다. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation)되며, 완료 시점에 알림을 받을 수 있습니다. 검증 관련 업데이트는 `customer.tax_id.updated` 웹훅 이벤트를 구독하고, [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 확인하면 됩니다. 웹훅 처리에 대한 자세한 내용은 [documentation on defining webhook handlers](#handling-stripe-webhooks)를 참고하세요.

<!-- You may delete a tax ID using the `deleteTaxId` method: -->
`deleteTaxId` 메서드로 세금 ID를 삭제할 수 있습니다.

```
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>

<!-- ### Syncing Customer Data With Stripe -->
### Syncing Customer Data With Stripe

<!-- Typically, when your application's users update their name, email address, or other information that is also stored by Stripe, you should inform Stripe of the updates. By doing so, Stripe's copy of the information will be in sync with your application's. -->
보통, 애플리케이션의 사용자가 이름, 이메일 등만 아니라 Stripe에도 저장되는 정보를 업데이트할 경우, Stripe에도 해당 업데이트 내용을 반영해야 합니다. 이렇게 하면 Stripe의 고객 정보와 애플리케이션의 데이터가 항상 동기화된 상태가 됩니다.

<!-- To automate this, you may define an event listener on your billable model that reacts to the model's `updated` event. Then, within your event listener, you may invoke the `syncStripeCustomerDetails` method on the model: -->
이 과정을 자동화하려면, 과금 모델의 `updated` 이벤트에 반응하는 이벤트 리스너를 정의할 수 있습니다. 이벤트 리스너 내에서 `syncStripeCustomerDetails` 메서드를 호출해 Stripe와 정보를 동기화합니다.

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
이제 고객 모델이 업데이트될 때마다 Stripe와 정보가 자동으로 동기화됩니다. 참고로, Cashier는 신규 고객 생성 시 고객 정보를 Stripe와 자동으로 동기화합니다.

<!-- You may customize the columns used for syncing customer information to Stripe by overriding a variety of methods provided by Cashier. For example, you may override the `stripeName` method to customize the attribute that should be considered the customer's "name" when Cashier syncs customer information to Stripe: -->
Stripe로 동기화되는 고객 정보 컬럼을 커스터마이즈하려면, Cashier에서 제공하는 다양한 메서드를 오버라이드할 수 있습니다. 예를 들어, `stripeName` 메서드를 오버라이드해 Stripe에 동기화할 "이름" 필드를 변경할 수 있습니다.

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

<!-- Similarly, you may override the `stripeEmail`, `stripePhone`, `stripeAddress`, and `stripePreferredLocales` methods. These methods will sync information to their corresponding customer parameters when [updating the Stripe customer object](https://stripe.com/docs/api/customers/update). If you wish to take total control over the customer information sync process, you may override the `syncStripeCustomerDetails` method. -->
마찬가지로, `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales` 메서드도 오버라이드할 수 있습니다. 이 메서드들은 [updating the Stripe customer object](https://stripe.com/docs/api/customers/update) 시 해당 파라미터에 정보를 동기화합니다. 만약 고객 정보 동기화 과정을 완전히 커스터마이즈하고 싶다면, `syncStripeCustomerDetails` 메서드를 직접 오버라이드하면 됩니다.

<a name="billing-portal"></a>

<!-- ### Billing Portal -->
### Billing Portal

<!-- Stripe offers [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) so that your customer can manage their subscription, payment methods, and view their billing history. You can redirect your users to the billing portal by invoking the `redirectToBillingPortal` method on the billable model from a controller or route: -->
Stripe에서는 [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal)할 수 있게 해줍니다. 이를 통해 고객은 구독, 결제 수단, 결제 내역 등을 직접 관리할 수 있습니다. 컨트롤러나 라우트에서 과금 모델의 `redirectToBillingPortal` 메서드를 호출해 사용자를 Stripe 청구 포털로 리다이렉트할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

<!-- By default, when the user is finished managing their subscription, they will be able to return to the `home` route of your application via a link within the Stripe billing portal. You may provide a custom URL that the user should return to by passing the URL as an argument to the `redirectToBillingPortal` method: -->
사용자가 Stripe 청구 포털에서 구독 관리를 마치면, 기본적으로 애플리케이션의 `home` 라우트로 돌아올 수 있습니다. 사용자가 돌아올 URL을 직접 지정하고 싶다면, `redirectToBillingPortal` 메서드에 원하는 URL을 인수로 전달하면 됩니다.

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

<!-- If you would like to generate the URL to the billing portal without generating an HTTP redirect response, you may invoke the `billingPortalUrl` method: -->
만약 HTTP 리다이렉트 응답을 생성하지 않고 청구 포털의 URL만 생성하고 싶다면, `billingPortalUrl` 메서드를 활용하면 됩니다.

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
Stripe로 구독을 생성하거나 "단일 청구"를 처리하려면 우선 결제 수단을 저장하고, Stripe에서 결제 수단의 식별자(ID)를 받아와야 합니다. 이 방법은 결제 수단이 구독용인지 단일 청구용인지에 따라 다르니, 각각의 상황을 아래에서 설명합니다.

<a name="payment-methods-for-subscriptions"></a>

<!-- #### Payment Methods For Subscriptions -->
#### Payment Methods For Subscriptions

<!-- When storing a customer's credit card information for future use by a subscription, the Stripe "Setup Intents" API must be used to securely gather the customer's payment method details. A "Setup Intent" indicates to Stripe the intention to charge a customer's payment method. Cashier's `Billable` trait includes the `createSetupIntent` method to easily create a new Setup Intent. You should invoke this method from the route or controller that will render the form which gathers your customer's payment method details: -->
구독을 위해 고객의 신용카드 정보를 추후 사용할 목적으로 저장하려면 Stripe의 "Setup Intents" API를 이용해 결제 수단 정보를 안전하게 수집해야 합니다. "Setup Intent"란 Stripe에 고객 결제 수단에 대한 결제 의도가 있음을 미리 알려주는 역할을 합니다. Cashier의 `Billable` 트레이트에는 새 Setup Intent를 쉽게 생성할 수 있는 `createSetupIntent` 메서드가 포함되어 있습니다. 이 메서드는 결제 수단 입력 폼을 렌더링하는 라우트나 컨트롤러에서 호출해야 합니다.

```
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

<!-- After you have created the Setup Intent and passed it to the view, you should attach its secret to the element that will gather the payment method. For example, consider this "update payment method" form: -->
Setup Intent를 생성해 뷰로 전달했다면, 해당 secret 값을 결제 수단을 입력받는 요소에 할당해야 합니다. 아래는 "결제 수단 업데이트" 폼 예시입니다.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

<!-- Next, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
그 다음 Stripe.js 라이브러리를 이용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 연결하면, 고객의 결제 정보를 안전하게 수집할 수 있습니다.

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
이제 카드를 인증하고 Stripe에서 보안 "결제 수단 식별자"를 받아오려면, [Stripe's `confirmCardSetup` method](https://stripe.com/docs/js/setup_intents/confirm_card_setup)를 사용할 수 있습니다.

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
카드 인증이 Stripe에서 정상적으로 완료되면, 생성된 `setupIntent.payment_method` 식별자를 Laravel 애플리케이션으로 전달하여 고객에게 연결할 수 있습니다. 이 결제 수단은 [added as a new payment method](#adding-payment-methods)하거나, [used to update the default payment method](#updating-the-default-payment-method) 등에 사용할 수 있습니다. 또는 즉시 해당 식별자로 [create a new subscription](#creating-subscriptions)도 가능합니다.

> [!NOTE]
> Setup Intents와 고객 결제 정보 수집에 대해 더 자세한 내용을 알고 싶다면 [review this overview provided by Stripe](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>

<!-- #### Payment Methods For Single Charges -->
#### Payment Methods For Single Charges

<!-- Of course, when making a single charge against a customer's payment method, we will only need to use a payment method identifier once. Due to Stripe limitations, you may not use the stored default payment method of a customer for single charges. You must allow the customer to enter their payment method details using the Stripe.js library. For example, consider the following form: -->
물론, 고객의 결제 수단으로 단 한 번만 결제할 계획이라면 해당 결제 수단 식별자는 한 번만 사용하면 됩니다. Stripe의 제한으로 인해 고객의 저장된 기본 결제 수단으로 단일 청구를 처리할 수는 없습니다. Stripe.js 라이브러리를 통해 고객이 직접 결제 정보를 입력할 수 있게 해야 합니다. 예를 들어 아래와 같은 폼을 사용할 수 있습니다.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

<!-- After defining such a form, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
이후 Stripe.js 라이브러리로 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 연결하면 고객의 결제 정보를 안전하게 수집할 수 있습니다.

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
그 다음, 카드를 인증하고 Stripe에서 보안 "결제 수단 식별자"를 받아오려면, [Stripe's `createPaymentMethod` method](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method)를 사용할 수 있습니다.

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
카드 인증이 정상적으로 완료되면, `paymentMethod.id`를 Laravel 애플리케이션으로 전달하여 [single charge](#simple-charge)를 처리할 수 있습니다.

<a name="retrieving-payment-methods"></a>

<!-- ### Retrieving Payment Methods -->
### Retrieving Payment Methods

<!-- The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances: -->
청구 가능한 모델 인스턴스에서 `paymentMethods` 메서드를 호출하면 `Laravel\Cashier\PaymentMethod` 인스턴스의 컬렉션을 반환합니다.

```
$paymentMethods = $user->paymentMethods();
```

<!-- By default, this method will return payment methods of the `card` type. To retrieve payment methods of a different type, you may pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 `card` 타입의 결제 수단만 반환합니다. 만약 다른 타입의 결제 수단을 조회하고 싶다면, 메서드의 인수로 `type`을 전달하면 됩니다.

```
$paymentMethods = $user->paymentMethods('sepa_debit');
```

<!-- To retrieve the customer's default payment method, the `defaultPaymentMethod` method may be used: -->
고객의 기본 결제 수단을 조회하려면 `defaultPaymentMethod` 메서드를 사용할 수 있습니다.

```
$paymentMethod = $user->defaultPaymentMethod();
```

<!-- You can retrieve a specific payment method that is attached to the billable model using the `findPaymentMethod` method: -->
청구 가능한 모델에 연결된 특정 결제 수단을 조회하려면 `findPaymentMethod` 메서드를 사용할 수 있습니다.

```
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="check-for-a-payment-method"></a>

<!-- ### Determining If A User Has A Payment Method -->
### Determining If A User Has A Payment Method

<!-- To determine if a billable model has a default payment method attached to their account, invoke the `hasDefaultPaymentMethod` method: -->
청구 가능한 모델이 계정에 기본 결제 수단이 연결되어 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 호출하면 됩니다.

```
if ($user->hasDefaultPaymentMethod()) {
    //
}
```

<!-- You may use the `hasPaymentMethod` method to determine if a billable model has at least one payment method attached to their account: -->
청구 가능한 모델이 적어도 하나 이상의 결제 수단을 가지는지 확인하려면 `hasPaymentMethod` 메서드를 사용할 수 있습니다.

```
if ($user->hasPaymentMethod()) {
    //
}
```

<!-- This method will determine if the billable model has payment methods of the `card` type. To determine if a payment method of another type exists for the model, you may pass the `type` as an argument to the method: -->
이 메서드는 모델이 `card` 타입의 결제 수단을 가지고 있는지 판단합니다. 만약 다른 타입의 결제 수단을 확인하고 싶다면, 해당 `type`을 인수로 전달할 수 있습니다.

```
if ($user->hasPaymentMethod('sepa_debit')) {
    //
}
```

<a name="updating-the-default-payment-method"></a>

<!-- ### Updating The Default Payment Method -->
### Updating The Default Payment Method

<!-- The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method: -->
고객의 기본 결제 수단 정보를 업데이트하려면 `updateDefaultPaymentMethod` 메서드를 사용할 수 있습니다. 이 메서드는 Stripe 결제 수단 식별자를 받아 새로운 결제 수단을 기본 청구 결제 수단으로 지정해줍니다.

```
$user->updateDefaultPaymentMethod($paymentMethod);
```

<!-- To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method: -->
Stripe에 저장된 고객의 기본 결제 수단 정보와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용할 수 있습니다.

```
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 고객의 기본 결제 수단은 송장 처리 또는 신규 구독 생성에만 사용할 수 있습니다. Stripe의 제한으로 인해 단건 결제에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>

<!-- ### Adding Payment Methods -->
### Adding Payment Methods

<!-- To add a new payment method, you may call the `addPaymentMethod` method on the billable model, passing the payment method identifier: -->
새로운 결제 수단을 추가하려면 결제 수단 식별자를 전달하여 청구 가능한 모델의 `addPaymentMethod` 메서드를 호출하면 됩니다.

```
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 식별자를 조회하는 방법에 대해서는 [payment method storage documentation](#storing-payment-methods)를 참고해 주세요.

<a name="deleting-payment-methods"></a>

<!-- ### Deleting Payment Methods -->
### Deleting Payment Methods

<!-- To delete a payment method, you may call the `delete` method on the `Laravel\Cashier\PaymentMethod` instance you wish to delete: -->
결제 수단을 삭제하려면 삭제하려는 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```
$paymentMethod->delete();
```

<!-- The `deletePaymentMethod` method will delete a specific payment method from the billable model: -->
특정 결제 수단을 청구 가능한 모델에서 삭제하려면 `deletePaymentMethod` 메서드를 사용할 수 있습니다.

```
$user->deletePaymentMethod('pm_visa');
```

<!-- The `deletePaymentMethods` method will delete all of the payment method information for the billable model: -->
모델에 저장된 모든 결제 수단 정보를 삭제하려면 `deletePaymentMethods` 메서드를 사용할 수 있습니다.

```
$user->deletePaymentMethods();
```

<!-- By default, this method will delete payment methods of the `card` type. To delete payment methods of a different type you can pass the `type` as an argument to the method: -->
기본적으로 이 메서드는 `card` 타입의 결제 수단만 삭제합니다. 다른 타입의 결제 수단을 삭제하고 싶다면 해당 `type`을 인수로 전달할 수 있습니다.

```
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 사용자가 활성 구독을 가지고 있는 경우, 기본 결제 수단을 삭제하지 못하도록 애플리케이션에서 반드시 제한해야 합니다.

<a name="subscriptions"></a>

<!-- ## Subscriptions -->
## Subscriptions

<!-- Subscriptions provide a way to set up recurring payments for your customers. Stripe subscriptions managed by Cashier provide support for multiple subscription prices, subscription quantities, trials, and more. -->
구독 기능은 고객의 반복 결제를 설정하는 방법을 제공합니다. Cashier가 관리하는 Stripe 구독은 복수의 구독 가격, 구독 수량, 체험 기간 등 다양한 기능을 지원합니다.

<a name="creating-subscriptions"></a>

<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription: -->
구독을 생성하려면 먼저 보통 `App\Models\User` 인스턴스인 청구 가능한 모델을 가져와야 합니다. 모델 인스턴스를 가져온 다음, `newSubscription` 메서드를 사용해 구독을 생성할 수 있습니다.

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
`newSubscription` 메서드에 전달하는 첫 번째 인수는 구독의 내부 이름입니다. 애플리케이션에서 구독이 하나만 있다면 `default` 또는 `primary`와 같은 이름을 사용할 수 있습니다. 이 구독 이름은 내부적으로만 사용되며, 사용자에게 표시하지 않습니다. 또한 공백을 포함하지 않아야 하고, 구독 생성 후에는 변경하지 않아야 합니다. 두 번째 인수는 사용자가 가입할 Stripe의 가격 식별자입니다.

<!-- The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information. -->
`create` 메서드는 [a Stripe payment method identifier](#storing-payment-methods)나 Stripe `PaymentMethod` 객체를 받아 해당 구독을 시작하며, 모델의 Stripe 고객 ID 등 관련 결제 정보를 데이터베이스에 업데이트합니다.

> [!WARNING]
> 결제 수단 식별자를 `create` 구독 메서드에 직접 전달하면, 그 결제 수단이 사용자의 저장된 결제 수단 목록에도 자동으로 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>

<!-- #### Collecting Recurring Payments Via Invoice Emails -->
#### Collecting Recurring Payments Via Invoice Emails

<!-- Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices: -->
반복 결제를 자동으로 청구하는 대신, Stripe가 반복 결제일마다 고객에게 송장 이메일을 보내도록 지시할 수 있습니다. 이 경우, 고객은 송장을 받은 뒤 직접 결제할 수 있습니다. 송장 이메일을 통한 반복 결제에서는 최초에 결제 수단을 등록하지 않아도 됩니다.

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

<!-- The amount of time a customer has to pay their invoice before their subscription is cancelled is determined by the `days_until_due` option. By default, this is 30 days; however, you may provide a specific value for this option if you wish: -->
송장 만료(= 구독 취소) 전까지 고객이 송장을 결제할 수 있는 기간은 `days_until_due` 옵션으로 설정됩니다. 기본값은 30일이며, 필요하다면 이 옵션에 원하는 값을 지정할 수 있습니다.

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>

<!-- #### Quantities -->
#### Quantities

<!-- If you would like to set a specific [quantity](https://stripe.com/docs/billing/subscriptions/quantities) for the price when creating the subscription, you should invoke the `quantity` method on the subscription builder before creating the subscription: -->
구독 생성 시 가격에 대해 원하는 [quantity](https://stripe.com/docs/billing/subscriptions/quantities)을 지정하려면, 구독 빌더에서 `quantity` 메서드를 구독 생성 전에 호출해야 합니다.

```
$user->newSubscription('default', 'price_monthly')
     ->quantity(5)
     ->create($paymentMethod);
```

<a name="additional-details"></a>

<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional [customer](https://stripe.com/docs/api/customers/create) or [subscription](https://stripe.com/docs/api/subscriptions/create) options supported by Stripe, you may do so by passing them as the second and third arguments to the `create` method: -->
Stripe에서 지원하는 추가 [customer](https://stripe.com/docs/api/customers/create) 또는 [subscription](https://stripe.com/docs/api/subscriptions/create) 옵션을 지정하고 싶다면, `create` 메서드의 두 번째와 세 번째 인수에 배열로 전달할 수 있습니다.

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
구독 생성 시 쿠폰을 적용하고 싶다면, `withCoupon` 메서드를 사용할 수 있습니다.

```
$user->newSubscription('default', 'price_monthly')
     ->withCoupon('code')
     ->create($paymentMethod);
```

<!-- Or, if you would like to apply a [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes), you may use the `withPromotionCode` method: -->
또는 [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 적용하고 싶으면, `withPromotionCode` 메서드를 사용할 수 있습니다.

```
$user->newSubscription('default', 'price_monthly')
     ->withPromotionCode('promo_code_id')
     ->create($paymentMethod);
```

<!-- The given promotion code ID should be the Stripe API ID assigned to the promotion code and not the customer facing promotion code. If you need to find a promotion code ID based on a given customer facing promotion code, you may use the `findPromotionCode` method: -->
여기서 전달해야 하는 프로모션 코드 ID는 고객이 보는 코드가 아닌, Stripe에서 해당 프로모션 코드에 할당한 API ID여야 합니다. 만약 고객에게 보여지는 프로모션 코드로부터 할당된 ID를 찾고 싶다면, `findPromotionCode` 메서드를 사용할 수 있습니다.

```
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

<!-- In the example above, the returned `$promotionCode` object is an instance of `Laravel\Cashier\PromotionCode`. This class decorates an underlying `Stripe\PromotionCode` object. You can retrieve the coupon related to the promotion code by invoking the `coupon` method: -->
위 예시에서 반환되는 `$promotionCode` 객체는 `Laravel\Cashier\PromotionCode` 인스턴스입니다. 이 클래스는 내부적으로 `Stripe\PromotionCode` 객체를 감싸고 있습니다. 프로모션 코드와 연결된 쿠폰 정보를 가져오려면 `coupon` 메서드를 호출하면 됩니다.

```
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

<!-- The coupon instance allows you to determine the discount amount and whether the coupon represents a fixed discount or percentage based discount: -->
쿠폰 인스턴스를 통해 할인 금액이 얼마이고, 고정 금액 할인인지, 퍼센트 할인인지도 알 수 있습니다.

```
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

<!-- You can also retrieve the discounts that are currently applied to a customer or subscription: -->
또한, 현재 고객이나 구독에 적용된 할인 내역도 조회할 수 있습니다.

```
$discount = $billable->discount();

$discount = $subscription->discount();
```

<!-- The returned `Laravel\Cashier\Discount` instances decorate an underlying `Stripe\Discount` object instance. You may retrieve the coupon related to this discount by invoking the `coupon` method: -->
반환되는 `Laravel\Cashier\Discount` 인스턴스는 내부적으로 `Stripe\Discount` 객체를 감싸고 있습니다. 관련 쿠폰 정보를 조회하려면 `coupon` 메서드를 호출하면 됩니다.

```
$coupon = $subscription->discount()->coupon();
```

<!-- If you would like to apply a new coupon or promotion code to a customer or subscription, you may do so via the `applyCoupon` or `applyPromotionCode` methods: -->
고객 또는 구독에 새로운 쿠폰이나 프로모션 코드를 적용하려면, `applyCoupon` 또는 `applyPromotionCode` 메서드를 사용하면 됩니다.

```
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

<!-- Remember, you should use the Stripe API ID assigned to the promotion code and not the customer facing promotion code. Only one coupon or promotion code can be applied to a customer or subscription at a given time. -->
중요: 반드시 고객에게 보여지는 코드가 아니라 Stripe에서 프로모션 코드에 할당한 API ID를 사용해야 합니다. 한 시점에 한 고객이나 구독에는 하나의 쿠폰 또는 프로모션 코드만 적용할 수 있습니다.

<!-- For more info on this subject, please consult the Stripe documentation regarding [coupons](https://stripe.com/docs/billing/subscriptions/coupons) and [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes). -->
더 자세한 정보는 Stripe 문서의 [coupons](https://stripe.com/docs/billing/subscriptions/coupons)과 [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes) 관련 자료를 참고해 주세요.

<a name="adding-subscriptions"></a>

<!-- #### Adding Subscriptions -->
#### Adding Subscriptions

<!-- If you would like to add a subscription to a customer who already has a default payment method you may invoke the `add` method on the subscription builder: -->
이미 기본 결제 수단이 등록되어 있는 고객에게 구독을 추가하고 싶다면, 구독 빌더에서 `add` 메서드를 호출하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>

<!-- #### Creating Subscriptions From The Stripe Dashboard -->
#### Creating Subscriptions From The Stripe Dashboard

<!-- You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a name of `default`. To customize the subscription name that is assigned to dashboard created subscriptions, [extend the `WebhookController`](#defining-webhook-event-handlers) and overwrite the `newSubscriptionName` method. -->
Stripe 대시보드에서도 직접 구독을 생성할 수 있습니다. 이 경우 Cashier는 새로 추가된 구독을 `default`라는 이름으로 동기화합니다. 대시보드에서 생성된 구독에 할당되는 이름을 커스터마이즈하려면, [extend the `WebhookController`](#defining-webhook-event-handlers) `newSubscriptionName` 메서드를 오버라이드 해야 합니다.

<!-- In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different names, only one type of subscription may be added through the Stripe dashboard. -->
또한, Stripe 대시보드에서는 한 종류의 구독만 생성할 수 있습니다. 즉, 애플리케이션에서 여러 구독 종류(다른 이름)를 제공하더라도, 대시보드에서는 한 종류만 추가할 수 있습니다.

<!-- Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If a customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database. -->
마지막으로, 애플리케이션에서 제공하는 구독 종류마다 한 번에 하나의 활성 구독만 추가해야 합니다. 고객이 두 개의 `default` 구독을 가지게 될 경우, Cashier는 데이터베이스와 동기화는 하더라도 가장 최근에 추가된 구독만 사용합니다.

<a name="checking-subscription-status"></a>

<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the name of the subscription as its first argument: -->
고객이 구독에 가입한 뒤에는, 여러 편리한 메서드를 사용해서 구독 상태를 쉽게 확인할 수 있습니다. 먼저, `subscribed` 메서드는 고객이 현재 활성 구독을 가지고 있으면(시범 이용 기간도 포함) `true`를 반환합니다. `subscribed` 메서드는 첫 번째 인수로 구독 이름을 받습니다.

```
if ($user->subscribed('default')) {
    //
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/9.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` 메서드는 [route middleware](/docs/9.x/middleware)로 활용해, 사용자의 구독 상태에 따라 특정 라우트 또는 컨트롤러 접근을 필터링하는 데에도 유용합니다.

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
사용자가 아직 시범 이용(trial) 기간 중인지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이를 통해 사용자에게 여전히 시범 이용 중임을 알리는 경고 등을 표시할지 판단할 수 있습니다.

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- The `subscribedToProduct` method may be used to determine if the user is subscribed to a given product based on a given Stripe product's identifier. In Stripe, products are collections of prices. In this example, we will determine if the user's `default` subscription is actively subscribed to the application's "premium" product. The given Stripe product identifier should correspond to one of your product's identifiers in the Stripe dashboard: -->
`subscribedToProduct` 메서드는, Stripe의 제품 식별자를 기반으로 사용자가 해당 제품에 대해 구독 중인지 확인할 수 있습니다. Stripe에서 제품은 여러 가격의 집합입니다. 아래 예시에서는 사용자의 `default` 구독이 애플리케이션의 "premium" 제품에 해당하는지 확인합니다. Stripe 제품 식별자는 대시보드에서 확인할 수 있습니다.

```
if ($user->subscribedToProduct('prod_premium', 'default')) {
    //
}
```

<!-- By passing an array to the `subscribedToProduct` method, you may determine if the user's `default` subscription is actively subscribed to the application's "basic" or "premium" product: -->
`subscribedToProduct` 메서드에 배열을 전달하면, 사용자의 `default` 구독이 애플리케이션의 "basic" 또는 "premium" 제품에 활성 구독되어 있는지 확인할 수 있습니다.

```
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    //
}
```

<!-- The `subscribedToPrice` method may be used to determine if a customer's subscription corresponds to a given price ID: -->
`subscribedToPrice` 메서드는 고객의 구독이 특정 가격 ID에 해당하는지 확인하는 데 사용할 수 있습니다.

```
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    //
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
`recurring` 메서드는 사용자가 현재 구독 중이고, 시범 이용 기간을 벗어났는지 확인하는 데 사용합니다.

```
if ($user->subscription('default')->recurring()) {
    //
}
```

> [!WARNING]
> 동일한 이름을 가진 여러 개의 구독이 있을 경우, `subscription` 메서드는 항상 가장 최근 구독만 반환합니다. 예를 들어, 사용자가 `default`라는 이름으로 두 개의 구독 정보를 가지게 되면, 그 중 하나가 예전 만료된 구독이고 다른 하나가 현재 활성 구독이더라도, 항상 가장 최근 구독만 반환하고 이전 구독 데이터는 기록 목적으로 데이터베이스에 남아 있게 됩니다.

<a name="cancelled-subscription-status"></a>

<!-- #### Canceled Subscription Status -->
#### Canceled Subscription Status

<!-- To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method: -->
사용자가 한때 구독을 했었지만 현재는 취소한 상태임을 확인하려면 `canceled` 메서드를 사용할 수 있습니다.

```
if ($user->subscription('default')->canceled()) {
    //
}
```

<!-- You may also determine if a user has canceled their subscription but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
또한 사용자가 구독 취소는 했지만, 아직 "유예 기간(grace period)"이 남아 있는지도 확인할 수 있습니다. 예를 들어 사용자가 3월 5일에 구독을 취소했는데, 원래 만료일이 3월 10일이었다면, 3월 10일까지는 유예 기간입니다. 이 기간 동안 `subscribed` 메서드는 여전히 `true`를 반환합니다.

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- To determine if the user has canceled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
마지막으로 사용자 구독이 취소되었고, 유예 기간도 끝났는지 확인하려면 `ended` 메서드를 사용합니다.

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="incomplete-and-past-due-status"></a>

<!-- #### Incomplete and Past Due Status -->
#### Incomplete and Past Due Status

<!-- If a subscription requires a secondary payment action after creation the subscription will be marked as `incomplete`. Subscription statuses are stored in the `stripe_status` column of Cashier's `subscriptions` database table. -->
구독이 생성된 후 추가 결제 처리가 필요하면, 해당 구독 상태는 `incomplete`로 표시됩니다. 구독 상태는 Cashier의 `subscriptions` 데이터베이스 테이블 내 `stripe_status` 컬럼에 저장됩니다.

<!-- Similarly, if a secondary payment action is required when swapping prices the subscription will be marked as `past_due`. When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Determining if a subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
마찬가지로, 가격을 변경(swap)할 때 추가 결제 처리가 필요하면, 구독 상태는 `past_due`로 표시됩니다. 이들 상태에서는 고객이 결제를 확정할 때까지 구독이 활성화되지 않습니다. 구독이 미완료 결제 상태인지 확인하려면, 청구 가능한 모델 또는 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용할 수 있습니다.

```
if ($user->hasIncompletePayment('default')) {
    //
}

if ($user->subscription('default')->hasIncompletePayment()) {
    //
}
```

<!-- When a subscription has an incomplete payment, you should direct the user to Cashier's payment confirmation page, passing the `latestPayment` identifier. You may use the `latestPayment` method available on subscription instance to retrieve this identifier: -->
구독이 미완료 결제 상태라면, 사용자를 Cashier의 결제 확인 페이지로 안내해야 합니다. 이때 `latestPayment` 식별자를 전달해야 하며, 구독 인스턴스의 `latestPayment` 메서드로 해당 식별자를 가져올 수 있습니다.

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

<!-- If you would like the subscription to still be considered active when it's in a `past_due` or `incomplete` state, you may use the `keepPastDueSubscriptionsActive` and `keepIncompleteSubscriptionsActive` methods provided by Cashier. Typically, these methods should be called in the `register` method of your `App\Providers\AppServiceProvider`: -->
만약 구독이 `past_due` 또는 `incomplete` 상태일 때도 활성 구독으로 간주하고 싶다면, Cashier의 `keepPastDueSubscriptionsActive` 및 `keepIncompleteSubscriptionsActive` 메서드를 사용할 수 있습니다. 보통 이 메서드들은 `App\Providers\AppServiceProvider`의 `register` 메서드에서 호출하면 됩니다.

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
    Cashier::keepIncompleteSubscriptionsActive();
}
```

> [!WARNING]
> 구독이 `incomplete` 상태일 때는 결제를 확정하기 전까지 변경할 수 없습니다. 따라서 구독이 `incomplete` 상태이면 `swap` 및 `updateQuantity` 메서드가 예외를 발생시킵니다.

<a name="subscription-scopes"></a>

<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
대부분의 구독 상태는 쿼리 스코프로도 제공되어, 특정 상태의 구독을 데이터베이스에서 쉽게 조회할 수 있습니다.

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
고객이 애플리케이션 구독 후 새 가격으로 변경하고 싶어 하는 경우가 있습니다. 고객의 구독 가격을 변경하려면 Stripe 가격의 식별자를 `swap` 메서드에 전달하면 됩니다. 가격 변경(swap)시, 만약 구독이 이전에 취소된 상태라면 재활성화한다고 간주합니다. Stripe 가격 식별자는 Stripe 대시보드에서 확인할 수 있습니다.

```
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

<!-- If the customer is on trial, the trial period will be maintained. Additionally, if a "quantity" exists for the subscription, that quantity will also be maintained. -->
만약 고객이 시범 이용(trial) 중이라면, 시범 기간이 유지됩니다. 또한 "수량(quantity)"이 지정되어 있다면, 그 수량도 그대로 유지됩니다.

<!-- If you would like to swap prices and cancel any trial period the customer is currently on, you may invoke the `skipTrial` method: -->
가격을 변경하면서 시범 이용(trial) 기간을 바로 취소하고 싶다면, `skipTrial` 메서드를 호출하면 됩니다.

```
$user->subscription('default')
        ->skipTrial()
        ->swap('price_yearly');
```

<!-- If you would like to swap prices and immediately invoice the customer instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
가격을 변경하면서, 다음 결제 주기를 기다리지 않고 즉시 고객에게 송장을 발행하려면, `swapAndInvoice` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>

<!-- #### Prorations -->
#### Prorations

<!-- By default, Stripe prorates charges when swapping between prices. The `noProrate` method may be used to update the subscription's price without prorating the charges: -->
Stripe는 가격 변경(swap) 시 기본적으로 비용을 일할 계산(prorate)합니다. 비용을 일할 계산하지 않고 구독 가격만 갱신하려면 `noProrate` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->noProrate()->swap('price_yearly');
```

<!-- For more information on subscription proration, consult the [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations). -->
구독 비용의 일할 계산에 대해 더 자세히 알고 싶다면 [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations)를 참고하시기 바랍니다.

> [!WARNING]
> `swapAndInvoice` 메서드 전에 `noProrate` 메서드를 실행하더라도 비용 일할 계산에는 영향을 주지 않습니다. 항상 송장이 발급됩니다.

<a name="subscription-quantity"></a>

<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. You may use the `incrementQuantity` and `decrementQuantity` methods to easily increment or decrement your subscription quantity: -->
일부 구독은 "수량"에 따라 요금이 책정됩니다. 예를 들어, 프로젝트 관리 애플리케이션에서 프로젝트당 월 10달러를 청구한다고 가정해볼 수 있습니다. `incrementQuantity`와 `decrementQuantity` 메서드를 사용하면 구독 수량을 쉽게 증가/감소시킬 수 있습니다.

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
또는 `updateQuantity` 메서드를 통해 특정 수량을 설정할 수도 있습니다.

```
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
수량 변경시 비용을 일할 계산 없이 처리하고 싶을 때는 `noProrate` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<!-- For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities). -->
구독 수량에 대해 더 알고 싶다면, [Stripe documentation](https://stripe.com/docs/subscriptions/quantities)를 참고해 주세요.

<a name="quantities-for-subscription-with-multiple-products"></a>

<!-- #### Quantities For Subscriptions With Multiple Products -->
#### Quantities For Subscriptions With Multiple Products

<!-- If your subscription is a [subscription with multiple products](#subscriptions-with-multiple-products), you should pass the ID of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods: -->
구독이 [subscription with multiple products](#subscriptions-with-multiple-products)인 경우, 수량을 변경할 가격의 ID를 두 번째 인수로 전달해야 합니다.

```
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>

<!-- ### Subscriptions With Multiple Products -->
### Subscriptions With Multiple Products

<!-- [Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products) allow you to assign multiple billing products to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on product for an additional $15 per month. Information for subscriptions with multiple products is stored in Cashier's `subscription_items` database table. -->
[Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products)은 하나의 구독에 여러 결제 상품을 할당할 수 있도록 합니다. 예를 들어, 고객 지원(헬프데스크) 애플리케이션을 예로 들면, 기본 구독 가격은 월 $10이고, 실시간 채팅 추가 상품(add-on)은 월 $15로 추가 요금을 부과할 수 있습니다. 이러한 여러 상품에 대한 정보는 Cashier의 `subscription_items` 데이터베이스 테이블에 저장됩니다.

<!-- You may specify multiple products for a given subscription by passing an array of prices as the second argument to the `newSubscription` method: -->
하나의 구독에 여러 상품을 할당하려면, `newSubscription`의 두 번째 인수로 가격 배열을 전달합니다.

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
위 예시에서는 고객의 `default` 구독에 두 개의 가격이 연결됩니다. 두 가격 모두 각각의 청구 주기에 따라 결제됩니다. 필요한 경우 `quantity` 메서드를 사용해 각 가격별로 별도의 수량도 지정할 수 있습니다.

```
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

<!-- If you would like to add another price to an existing subscription, you may invoke the subscription's `addPrice` method: -->
이미 생성된 구독에 가격을 추가하고 싶다면, 구독의 `addPrice` 메서드를 호출하면 됩니다.

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

<!-- The example above will add the new price and the customer will be billed for it on their next billing cycle. If you would like to bill the customer immediately you may use the `addPriceAndInvoice` method: -->
위 코드는 다음 청구 주기에 새 가격이 반영되어 고객에게 청구됩니다. 바로 청구를 진행하고 싶다면, `addPriceAndInvoice` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

<!-- If you would like to add a price with a specific quantity, you can pass the quantity as the second argument of the `addPrice` or `addPriceAndInvoice` methods: -->
특정 가격에 대해 수량까지 지정해서 추가하려면, `addPrice` 또는 `addPriceAndInvoice` 메서드의 두 번째 인수로 수량을 전달하면 됩니다.

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

<!-- You may remove prices from subscriptions using the `removePrice` method: -->
구독에서 가격을 제거하려면 `removePrice` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> 구독의 마지막 가격은 제거할 수 없습니다. 마지막 가격을 없애고 싶다면 구독을 취소해야 합니다.

<a name="swapping-prices"></a>

<!-- #### Swapping Prices -->
#### Swapping Prices

<!-- You may also change the prices attached to a subscription with multiple products. For example, imagine a customer has a `price_basic` subscription with a `price_chat` add-on product and you want to upgrade the customer from the `price_basic` to the `price_pro` price: -->
여러 개의 제품이 포함된 구독에 연결된 가격을 변경할 수도 있습니다. 예를 들어, 고객이 `price_basic` 구독에 `price_chat` 추가 제품을 사용 중이고, 이 고객을 `price_basic`에서 `price_pro` 가격으로 업그레이드하려 한다고 가정해보겠습니다.

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

<!-- When executing the example above, the underlying subscription item with the `price_basic` is deleted and the one with the `price_chat` is preserved. Additionally, a new subscription item for the `price_pro` is created. -->
위 예시를 실행하면, `price_basic`이 적용된 구독 아이템은 삭제되고, `price_chat`이 적용된 아이템은 그대로 유지됩니다. 그리고 `price_pro`에 대한 새로운 구독 아이템이 생성됩니다.

<!-- You can also specify subscription item options by passing an array of key / value pairs to the `swap` method. For example, you may need to specify the subscription price quantities: -->
또한, `swap` 메서드에 키/값 쌍이 포함된 배열을 전달하여 구독 아이템의 옵션도 지정할 수 있습니다. 예를 들어, 각각의 구독 가격에 대해 수량(quantity)을 지정해야 할 수도 있습니다.

```
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

<!-- If you want to swap a single price on a subscription, you may do so using the `swap` method on the subscription item itself. This approach is particularly useful if you would like to preserve all of the existing metadata on the subscription's other prices: -->
단일 가격만 교체하고 싶을 때는, 해당 구독 아이템의 `swap` 메서드를 직접 사용할 수 있습니다. 이 방식은 구독 내 다른 가격들의 모든 기존 메타데이터를 유지하고 싶을 때 특히 유용합니다.

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
기본적으로 Stripe는 여러 제품이 포함된 구독에서 가격을 추가하거나 제거할 때 자동으로 비례 청구(프레이션)를 적용합니다. 만약 비례 청구 없이 가격을 조정하려면, 가격 변동 관련 메서드에 `noProrate` 메서드를 체이닝하여 사용해야 합니다.

```
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>

<!-- #### Quantities -->
#### Quantities

<!-- If you would like to update quantities on individual subscription prices, you may do so using the [existing quantity methods](#subscription-quantity) by passing the name of the price as an additional argument to the method: -->
각 구독 가격의 수량을 개별적으로 업데이트하려면, 기존의 [existing quantity methods](#subscription-quantity)를 사용할 때 가격 이름을 추가 인수로 전달하면 됩니다.

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 구독에 여러 가격이 있는 경우, `Subscription` 모델의 `stripe_price` 및 `quantity` 속성은 `null`이 됩니다. 개별 가격 속성에 접근하려면, `Subscription` 모델에서 제공하는 `items` 연관관계를 사용해야 합니다.

<a name="subscription-items"></a>

<!-- #### Subscription Items -->
#### Subscription Items

<!-- When a subscription has multiple prices, it will have multiple subscription "items" stored in your database's `subscription_items` table. You may access these via the `items` relationship on the subscription: -->
여러 가격이 적용된 구독은 데이터베이스의 `subscription_items` 테이블에 여러 구독 "아이템"이 저장됩니다. 해당 구독의 `items` 관계를 통해 이 아이템들에 접근할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

<!-- You can also retrieve a specific price using the `findItemOrFail` method: -->
또한, `findItemOrFail` 메서드를 사용하여 특정 가격의 아이템을 직접 조회할 수도 있습니다.

```
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>

<!-- ### Multiple Subscriptions -->
### Multiple Subscriptions

<!-- Stripe allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans. -->
Stripe는 고객이 동시에 여러 개의 구독을 가질 수 있도록 지원합니다. 예를 들어, 체육관을 운영하면서 수영 구독권과 웨이트 트레이닝 구독권을 각각 별도로 판매할 수 있으며, 각 구독은 서로 다른 가격을 가질 수 있습니다. 물론 사용자는 두 플랜 중 하나 또는 모두를 구독할 수 있어야 합니다.

<!-- When your application creates subscriptions, you may provide the name of the subscription to the `newSubscription` method. The name may be any string that represents the type of subscription the user is initiating: -->
애플리케이션에서 구독을 생성할 때는 `newSubscription` 메서드에 구독의 이름을 전달할 수 있습니다. 이 이름은 사용자가 시작하는 구독 유형을 나타내는 임의의 문자열이면 됩니다.

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
이 예제에서는 고객의 월간 수영 구독을 시작했습니다. 그러나 나중에 연간 요금제로 전환하고 싶어질 수도 있습니다. 사용자의 구독을 조정할 때는 `swimming` 구독의 가격만 간단히 교체하면 됩니다.

```
$user->subscription('swimming')->swap('price_swimming_yearly');
```

<!-- Of course, you may also cancel the subscription entirely: -->
물론 구독을 완전히 취소할 수도 있습니다.

```
$user->subscription('swimming')->cancel();
```

<a name="metered-billing"></a>

<!-- ### Metered Billing -->
### Metered Billing

<!-- [Metered billing](https://stripe.com/docs/billing/subscriptions/metered-billing) allows you to charge customers based on their product usage during a billing cycle. For example, you may charge customers based on the number of text messages or emails they send per month. -->
[Metered billing](https://stripe.com/docs/billing/subscriptions/metered-billing)은 고객의 제품 사용량에 따라 청구하는 방식입니다. 예를 들어, 고객이 한 달 동안 전송한 문자 메시지나 이메일 개수에 따라 요금을 부과할 수 있습니다.

<!-- To start using metered billing, you will first need to create a new product in your Stripe dashboard with a metered price. Then, use the `meteredPrice` to add the metered price ID to a customer subscription: -->
사용량 기반 과금을 시작하려면 Stripe 대시보드에서 사용량 기반 가격(metered price)이 적용된 새로운 제품을 생성하세요. 그리고 `meteredPrice`를 사용해 해당 가격 ID를 구독에 추가합니다.

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
또한, [Stripe Checkout](#checkout)을 통해 사용량 기반 구독을 시작할 수도 있습니다.

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
고객이 애플리케이션을 사용할 때마다 Stripe에 사용량을 보고해야 정확한 청구가 이루어집니다. 사용량 기반 구독의 사용량을 증가시키려면 `reportUsage` 메서드를 사용하면 됩니다.

```
$user = User::find(1);

$user->subscription('default')->reportUsage();
```

<!-- By default, a "usage quantity" of 1 is added to the billing period. Alternatively, you may pass a specific amount of "usage" to add to the customer's usage for the billing period: -->
기본적으로 한 번 호출하면 "사용량"이 1만큼 추가됩니다. 원한다면 이번 청구 기간에 추가할 "사용량"의 양을 직접 지정할 수도 있습니다.

```
$user = User::find(1);

$user->subscription('default')->reportUsage(15);
```

<!-- If your application offers multiple prices on a single subscription, you will need to use the `reportUsageFor` method to specify the metered price you want to report usage for: -->
애플리케이션에서 하나의 구독에 여러 가격 옵션이 있을 경우, `reportUsageFor` 메서드를 사용해 어떤 사용량 기반 가격(metered price)에 대해 사용량을 보고할지 지정해야 합니다.

```
$user = User::find(1);

$user->subscription('default')->reportUsageFor('price_metered', 15);
```

<!-- Sometimes, you may need to update usage which you have previously reported. To accomplish this, you may pass a timestamp or a `DateTimeInterface` instance as the second parameter to `reportUsage`. When doing so, Stripe will update the usage that was reported at that given time. You can continue to update previous usage records as the given date and time is still within the current billing period: -->
가끔 이전에 보고한 사용량을 업데이트해야 할 수도 있습니다. 이런 경우 `reportUsage`의 두 번째 인수로 타임스탬프 또는 `DateTimeInterface` 인스턴스를 전달하면 됩니다. 이렇게 하면 Stripe는 해당 시간에 보고된 사용량을 업데이트합니다. 지정한 날짜와 시간이 현재 청구 기간 내라면 여러 번 업데이트할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')->reportUsage(5, $timestamp);
```

<a name="retrieving-usage-records"></a>

<!-- #### Retrieving Usage Records -->
#### Retrieving Usage Records

<!-- To retrieve a customer's past usage, you may use a subscription instance's `usageRecords` method: -->
고객의 과거 사용량을 조회하려면 구독 인스턴스의 `usageRecords` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecords();
```

<!-- If your application offers multiple prices on a single subscription, you may use the `usageRecordsFor` method to specify the metered price that you wish to retrieve usage records for: -->
하나의 구독에 여러 가격 옵션이 있을 경우, `usageRecordsFor` 메서드를 이용해 특정 사용량 기반 가격에 대한 사용량 기록만 조회할 수 있습니다.

```
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecordsFor('price_metered');
```

<!-- The `usageRecords` and `usageRecordsFor` methods return a Collection instance containing an associative array of usage records. You may iterate over this array to display a customer's total usage: -->
이 `usageRecords` 및 `usageRecordsFor` 메서드는 사용량 기록의 연관 배열이 담긴 Collection 인스턴스를 반환합니다. 이 배열을 반복하여 고객의 총 사용량을 표시할 수 있습니다.

```
@foreach ($usageRecords as $usageRecord)
    - Period Starting: {{ $usageRecord['period']['start'] }}
    - Period Ending: {{ $usageRecord['period']['end'] }}
    - Total Usage: {{ $usageRecord['total_usage'] }}
@endforeach
```

<!-- For a full reference of all usage data returned and how to use Stripe's cursor based pagination, please consult [the official Stripe API documentation](https://stripe.com/docs/api/usage_records/subscription_item_summary_list). -->
반환되는 모든 사용 데이터와 Stripe의 커서 기반 페이징 기능에 대해 더 자세히 알고 싶다면 [the official Stripe API documentation](https://stripe.com/docs/api/usage_records/subscription_item_summary_list)를 참고하세요.

<a name="subscription-taxes"></a>

<!-- ### Subscription Taxes -->
### Subscription Taxes

> [!WARNING]
> 세율을 수동으로 계산하는 대신 [automatically calculate taxes using Stripe Tax](#tax-configuration)할 수 있습니다.

<!-- To specify the tax rates a user pays on a subscription, you should implement the `taxRates` method on your billable model and return an array containing the Stripe tax rate IDs. You can define these tax rates in [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates): -->
사용자가 구독에 대해 내야 할 세율을 지정하려면, 청구가 가능한(billable) 모델에 `taxRates` 메서드를 구현하여 Stripe 세율 ID 배열을 반환해야 합니다. [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates)에서 해당 세율을 등록할 수 있습니다.

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
`taxRates` 메서드를 사용하면 각 고객별로 세율을 다르게 적용할 수 있으므로, 여러 국가 및 다양한 세율을 가진 사용자 기반을 관리할 때 유용합니다.

<!-- If you're offering subscriptions with multiple products, you may define different tax rates for each price by implementing a `priceTaxRates` method on your billable model: -->
여러 상품이 포함된 구독을 제공하는 경우, 청구가 가능한 모델에서 `priceTaxRates` 메서드를 구현하여 각 가격에 대해 다른 세율을 정의할 수 있습니다.

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

> [!WARNING]
> `taxRates` 메서드는 구독 요금에만 적용됩니다. Cashier로 "일회성" 청구를 하려면, 해당 시점에 세율을 직접 지정해야 합니다.

<a name="syncing-tax-rates"></a>

<!-- #### Syncing Tax Rates -->
#### Syncing Tax Rates

<!-- When changing the hard-coded tax rate IDs returned by the `taxRates` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the new `taxRates` values, you should call the `syncTaxRates` method on the user's subscription instance: -->
`taxRates` 메서드에서 반환되는 하드코딩된 세율 ID를 변경해도, 해당 사용자의 기존 구독의 세금 설정은 그대로 남아 있습니다. 기존 구독에 대해 새로운 `taxRates` 값을 적용하려면, 해당 사용자의 구독 인스턴스에서 `syncTaxRates` 메서드를 호출해야 합니다.

```
$user->subscription('default')->syncTaxRates();
```

<!-- This will also sync any item tax rates for a subscription with multiple products. If your application is offering subscriptions with multiple products, you should ensure that your billable model implements the `priceTaxRates` method [discussed above](#subscription-taxes). -->
이 메서드는 여러 상품이 포함된 구독의 각 아이템 세율도 동기화합니다. 여러 상품 구독을 제공 중이라면 [discussed above](#subscription-taxes) 모델에 `priceTaxRates` 메서드를 구현해야 합니다.

<a name="tax-exemption"></a>

<!-- #### Tax Exemption -->
#### Tax Exemption

<!-- Cashier also offers the `isNotTaxExempt`, `isTaxExempt`, and `reverseChargeApplies` methods to determine if the customer is tax exempt. These methods will call the Stripe API to determine a customer's tax exemption status: -->
Cashier는 고객이 세금 면제 대상인지 확인할 수 있는 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드도 제공합니다. 이 메서드들은 Stripe API를 호출하여 고객의 세금 면제 상태를 확인합니다.

```
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]
> 이러한 메서드들은 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있습니다. 단, `Invoice` 객체에서 호출할 경우, 송장이 생성될 당시의 세금 면제 상태를 기준으로 확인합니다.

<a name="subscription-anchor-date"></a>

<!-- ### Subscription Anchor Date -->
### Subscription Anchor Date

<!-- By default, the billing cycle anchor is the date the subscription was created or, if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method: -->
기본적으로 결제 주기의 기준일(billing cycle anchor)은 구독이 생성된 날짜, 또는 체험 기간이 있다면 체험이 끝나는 날짜입니다. 기준일을 수정하려면 `anchorBillingCycleOn` 메서드를 사용할 수 있습니다.

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
구독 결제 주기 관리에 대한 더 자세한 정보는 [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>

<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
구독을 취소하려면, 해당 사용자의 구독에서 `cancel` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->cancel();
```

<!-- When a subscription is canceled, Cashier will automatically set the `ends_at` column in your `subscriptions` database table. This column is used to know when the `subscribed` method should begin returning `false`. -->
구독이 취소되면, Cashier는 자동으로 데이터베이스의 `subscriptions` 테이블에 있는 `ends_at` 컬럼을 설정합니다. 이 컬럼은 `subscribed` 메서드가 언제부터 `false`를 반환해야 하는지 판단하는 데 사용됩니다.

<!-- For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
예를 들어, 사용자가 3월 1일에 구독을 취소했다 하더라도 구독이 3월 5일까지 유효하다면, `subscribed` 메서드는 3월 5일까지 계속해서 `true`를 반환합니다. 이는 일반적으로 사용자가 결제 주기 종료 시점까지 애플리케이션을 계속 사용할 수 있도록 허용하기 위함입니다.

<!-- You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
구독을 취소했지만 아직 "유예 기간(grace period)"에 해당하는지 확인하려면 `onGracePeriod` 메서드를 사용할 수 있습니다.

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription: -->
즉시 구독을 취소하려면 `cancelNow` 메서드를 호출합니다.

```
$user->subscription('default')->cancelNow();
```

<!-- If you wish to cancel a subscription immediately and invoice any remaining un-invoiced metered usage or new / pending proration invoice items, call the `cancelNowAndInvoice` method on the user's subscription: -->
즉시 구독을 취소하고, 청구되지 않은 사용량이나 새로 추가된/보류 중인 청구 항목(proration invoice item)이 있다면 즉시 인보이스를 발생시키려면 `cancelNowAndInvoice` 메서드를 사용합니다.

```
$user->subscription('default')->cancelNowAndInvoice();
```

<!-- You may also choose to cancel the subscription at a specific moment in time: -->
특정 시점에 구독이 취소되도록 지정할 수도 있습니다.

```
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

<a name="resuming-subscriptions"></a>

<!-- ### Resuming Subscriptions -->
### Resuming Subscriptions

<!-- If a customer has canceled their subscription and you wish to resume it, you may invoke the `resume` method on the subscription. The customer must still be within their "grace period" in order to resume a subscription: -->
고객이 구독을 취소한 뒤, 다시 재개할 수 있도록 하려면 해당 구독에서 `resume` 메서드를 호출하세요. 단, 고객이 아직 "유예 기간" 내에 있어야만 구독을 재개할 수 있습니다.

```
$user->subscription('default')->resume();
```

<!-- If the customer cancels a subscription and then resumes that subscription before the subscription has fully expired the customer will not be billed immediately. Instead, their subscription will be re-activated and they will be billed on the original billing cycle. -->
고객이 구독을 취소한 뒤 만료되기 전에 다시 재개하면, 즉시 청구되지 않고 구독이 다시 활성화되며 원래 결제 주기에 따라 다음 결제가 이루어집니다.

<a name="subscription-trials"></a>

<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>

<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions: -->
고객에게 체험 기간을 제공하되, 결제 수단 정보를 미리 수집하고 싶다면 구독 생성 시 `trialDays` 메서드를 사용해야 합니다.

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
이 메서드는 데이터베이스의 구독 레코드에 체험 기간 종료 날짜를 저장하며, Stripe에는 해당 날짜 이후에만 결제가 시작되도록 지시합니다. `trialDays` 메서드를 사용할 경우, Stripe에서 해당 가격에 기본 체험 기간이 설정되어 있더라도 이를 덮어씁니다.

> [!WARNING]
> 고객의 구독이 체험 기간 만료 전에 취소되지 않을 경우, 체험 기간이 끝나는 즉시 즉시 결제가 진행됩니다. 따라서 반드시 사용자에게 체험 종료일을 미리 안내해야 합니다.

<!-- The `trialUntil` method allows you to provide a `DateTime` instance that specifies when the trial period should end: -->
`trialUntil` 메서드를 이용하면, 체험 기간이 종료되어야 할 정확한 시점을 `DateTime` 인스턴스로 지정할 수 있습니다.

```
use Carbon\Carbon;

$user->newSubscription('default', 'price_monthly')
            ->trialUntil(Carbon::now()->addDays(10))
            ->create($paymentMethod);
```

<!-- You may determine if a user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
현재 사용자가 체험 기간 내에 있는지 확인하려면 사용자 인스턴스의 `onTrial` 메서드 또는 구독 인스턴스의 `onTrial` 메서드를 사용할 수 있습니다. 아래 두 예제는 동일하게 동작합니다.

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- You may use the `endTrial` method to immediately end a subscription trial: -->
체험 기간을 즉시 종료하려면 `endTrial` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->endTrial();
```

<!-- To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods: -->
기존 체험 기간이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용할 수 있습니다.

```
if ($user->hasExpiredTrial('default')) {
    //
}

if ($user->subscription('default')->hasExpiredTrial()) {
    //
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>

<!-- #### Defining Trial Days In Stripe / Cashier -->
#### Defining Trial Days In Stripe / Cashier

<!-- You may choose to define how many trial days your price's receive in the Stripe dashboard or always pass them explicitly using Cashier. If you choose to define your price's trial days in Stripe you should be aware that new subscriptions, including new subscriptions for a customer that had a subscription in the past, will always receive a trial period unless you explicitly call the `skipTrial()` method. -->
Stripe 대시보드에서 각 가격별 체험 기간(일수)을 지정하거나 Cashier를 통해 명시적으로 지정할 수 있습니다. Stripe에서 가격별 체험 기간을 지정하면, 과거에 구독 이력이 있던 고객을 포함해 새로운 구독 생성 시마다 항상 체험 기간이 적용됩니다. 단, `skipTrial()` 메서드를 명시적으로 호출하면 체험 기간 없이 바로 결제가 시작됩니다.

<a name="without-payment-method-up-front"></a>

<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration: -->
결제 수단 정보를 미리 받지 않고 체험 기간을 제공하고 싶다면, 사용자 레코드의 `trial_ends_at` 컬럼에 원하는 체험 종료 날짜를 설정하면 됩니다. 보통 회원 가입 시 이 작업을 처리합니다.

```
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!WARNING]
> 청구가 가능한(billable) 모델의 클래스에서 `trial_ends_at` 속성에 대해 [date cast](/docs/9.x/eloquent-mutators#date-casting)를 반드시 추가해야 합니다.

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the billable model instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
Cashier에서는 이런 유형의 체험을 "일반(generic) 체험"이라고 부릅니다. 이는 실제 구독에 연결되지 않은 상태이기 때문입니다. billable 모델 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 속성의 값보다 전이면 `true`를 반환합니다.

```
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
실제 구독을 생성하고 싶으면, 평소처럼 `newSubscription` 메서드를 사용하면 됩니다.

```
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription name parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
사용자의 체험 종료 날짜를 조회하고 싶다면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 체험 중이면 Carbon 인스턴스를 반환하고, 아니면 `null`을 반환합니다. 기본이 아닌 특정 구독의 체험 종료 날짜를 조회하려면 인수로 구독 이름을 전달할 수도 있습니다.

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not yet created an actual subscription: -->
특히 사용자가 "일반(generic) 체험" 상태임을 알고 싶다면, 즉 실제 구독을 아직 생성하지 않은 상태라면 `onGenericTrial` 메서드를 사용할 수 있습니다.

```
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>

<!-- ### Extending Trials -->
### Extending Trials

<!-- The `extendTrial` method allows you to extend the trial period of a subscription after the subscription has been created. If the trial has already expired and the customer is already being billed for the subscription, you can still offer them an extended trial. The time spent within the trial period will be deducted from the customer's next invoice: -->
`extendTrial` 메서드를 사용하면 구독이 이미 생성된 후에도 체험 기간을 연장할 수 있습니다. 심지어 체험 기간이 만료되어 이미 결제가 시작된 경우에도 체험을 연장해줄 수 있습니다. 체험 기간에 속해 있었던 일차 기간은 고객의 다음 인보이스에서 차감됩니다.

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
> [the Stripe CLI](https://stripe.com/docs/stripe-cli)를 사용하면 로컬 개발 중 웹훅 테스트를 쉽게 할 수 있습니다.

<!-- Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Stripe는 다양한 이벤트 발생 시 웹훅을 통해 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier 서비스 프로바이더가 Cashier의 웹훅 컨트롤러로 연결되는 라우트를 자동으로 등록합니다. 이 컨트롤러가 모든 웹훅 요청을 처리하게 됩니다.

<!-- By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like. -->
Cashier 웹훅 컨트롤러는 Stripe 설정에 따라 미결제 건이 너무 많을 때 구독 취소, 고객 정보 업데이트, 고객 삭제, 구독 업데이트, 결제 수단 변경을 자동으로 처리합니다. 필요하다면 이 컨트롤러를 확장해 원하는 Stripe 웹훅 이벤트를 직접 처리할 수 있습니다.

<!-- To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are: -->
Stripe 웹훅이 올바르게 동작하려면, Stripe 관리 패널에서 웹훅 URL을 설정해야 합니다. 기본적으로 Cashier의 웹훅 컨트롤러는 `/stripe/webhook` URL 경로로 요청을 받습니다. Stripe 관리 패널에서 활성화해야 하는 웹훅 이벤트 목록은 다음과 같습니다.

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
편의를 위해 Cashier에는 `cashier:webhook` 아티즌 명령어가 제공됩니다. 이 명령어는 Cashier에서 필요한 모든 Stripe 이벤트를 수신하는 웹훅을 Stripe에 등록합니다.

```shell
php artisan cashier:webhook
```

<!-- By default, the created webhook will point to the URL defined by the `APP_URL` environment variable and the `cashier.webhook` route that is included with Cashier. You may provide the `--url` option when invoking the command if you would like to use a different URL: -->
기본적으로 생성되는 웹훅은 `APP_URL` 환경 변수와 Cashier에서 포함하는 `cashier.webhook` 라우트의 URL을 사용합니다. 다른 URL로 생성하고 싶다면 명령어 실행 시 `--url` 옵션을 사용할 수 있습니다.

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

<!-- The webhook that is created will use the Stripe API version that your version of Cashier is compatible with. If you would like to use a different Stripe version, you may provide the `--api-version` option: -->
생성된 웹훅은 현재 Cashier 버전과 호환되는 Stripe API 버전을 사용합니다. 다른 Stripe 버전을 원한다면 `--api-version` 옵션을 사용하세요.

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

<!-- After creation, the webhook will be immediately active. If you wish to create the webhook but have it disabled until you're ready, you may provide the `--disabled` option when invoking the command: -->
웹훅을 생성하자마자 즉시 활성 상태가 됩니다. 준비 전까지 비활성 상태로 생성하려면 `--disabled` 옵션을 사용할 수 있습니다.

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> 반드시 Cashier에서 제공하는 [webhook signature verification](#verifying-webhook-signatures) 미들웨어를 사용하여 Stripe 웹훅 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>

<!-- #### Webhooks & CSRF Protection -->
#### Webhooks & CSRF Protection

<!-- Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/9.x/csrf), be sure to list the URI as an exception in your application's `App\Http\Middleware\VerifyCsrfToken` middleware or list the route outside of the `web` middleware group: -->
Stripe 웹훅은 Laravel의 [CSRF protection](/docs/9.x/csrf)를 우회해야 하므로, 반드시 애플리케이션의 `App\Http\Middleware\VerifyCsrfToken` 미들웨어에서 해당 URI를 예외 목록에 넣거나, 해당 라우트를 `web` 미들웨어 그룹 외부에 두어야 합니다.

```
protected $except = [
    'stripe/*',
];
```

<a name="defining-webhook-event-handlers"></a>

<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancellations for failed charges and other common Stripe webhook events. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier는 결제 실패 등으로 인한 구독 취소 등 자주 발생하는 Stripe 웹훅 이벤트는 자동으로 처리해줍니다. 그러나 추가적으로 처리하고 싶은 웹훅 이벤트가 있다면 Cashier가 디스패치하는 다음 이벤트를 리스닝하여 직접 처리할 수 있습니다.

<!--
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`
-->
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

<!-- Both events contain the full payload of the Stripe webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/9.x/events#defining-listeners) that will handle the event: -->
두 이벤트 모두 Stripe 웹훅의 전체 페이로드를 포함합니다. 예를 들어, `invoice.payment_succeeded` 웹훅을 직접 처리하고 싶다면 [listener](/docs/9.x/events#defining-listeners)를 등록하여 이벤트를 처리하면 됩니다.

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
리스너를 정의한 뒤에는 애플리케이션의 `EventServiceProvider`에 리스너를 등록하면 됩니다.

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
웹훅(Webhook)의 보안을 강화하기 위해 [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures)을 사용할 수 있습니다. 편의를 위해, Cashier는 Stripe에서 들어오는 웹훅 요청이 유효한지 자동으로 검증하는 미들웨어를 기본으로 제공합니다.

<!-- To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is set in your application's `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard. -->
웹훅 검증을 활성화하려면, 애플리케이션의 `.env` 파일에서 `STRIPE_WEBHOOK_SECRET` 환경 변수가 반드시 설정되어 있어야 합니다. 이 웹훅 `secret` 값은 Stripe 계정 대시보드에서 확인할 수 있습니다.

<a name="single-charges"></a>

<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>

<!-- ### Simple Charge -->
### Simple Charge

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance. You will need to [provide a payment method identifier](#payment-methods-for-single-charges) as the second argument to the `charge` method: -->
고객에게 일회성 결제를 받으려면, 청구 가능한 모델 인스턴스에서 `charge` 메서드를 사용할 수 있습니다. 이때 [provide a payment method identifier](#payment-methods-for-single-charges)를 `charge` 메서드의 두 번째 인수로 전달해야 합니다.

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
`charge` 메서드는 세 번째 인수로 배열을 받아, Stripe의 결제 생성에 필요한 다양한 옵션을 전달할 수 있습니다. 사용 가능한 옵션에 대한 자세한 내용은 [Stripe documentation](https://stripe.com/docs/api/charges/create)를 참고하십시오.

```
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

<!-- You may also use the `charge` method without an underlying customer or user. To accomplish this, invoke the `charge` method on a new instance of your application's billable model: -->
또한, 고객이나 사용자와 연결된 인스턴스 없이 `charge` 메서드를 사용할 수도 있습니다. 이때는 애플리케이션의 billable 모델의 새 인스턴스에서 `charge` 메서드를 호출하면 됩니다.

```
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

<!-- The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method: -->
`charge` 메서드는 결제에 실패할 경우 예외를 발생시킵니다. 성공적으로 결제가 처리되면, `Laravel\Cashier\Payment` 인스턴스가 반환됩니다.

```
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    //
}
```

> [!WARNING]
> `charge` 메서드는 결제 금액을 애플리케이션이 사용하는 통화의 최소 단위(예: USD의 경우 센트 단위)로 지정해야 합니다.

<a name="charge-with-invoice"></a>

<!-- ### Charge With Invoice -->
### Charge With Invoice

<!-- Sometimes you may need to make a one-time charge and offer a PDF receipt to your customer. The `invoicePrice` method lets you do just that. For example, let's invoice a customer for five new shirts: -->
단발성 결제와 함께 고객에게 PDF 영수증을 제공해야 할 때가 있습니다. 이럴 때 `invoicePrice` 메서드를 사용할 수 있습니다. 예를 들어, 고객에게 티셔츠 5장을 청구하는 방법은 다음과 같습니다.

```
$user->invoicePrice('price_tshirt', 5);
```

<!-- The invoice will be immediately charged against the user's default payment method. The `invoicePrice` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array which should contain the billing options for the invoice itself: -->
이 청구서는 즉시 해당 사용자의 기본 결제 수단으로 결제됩니다. `invoicePrice` 메서드는 세 번째 인수로 배열을 받을 수 있으며, 이 배열에는 인보이스 항목의 청구 옵션을 설정합니다. 네 번째 인수는 인보이스 자체의 청구 옵션을 담은 배열입니다.

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
`invoicePrice`와 유사하게, `tabPrice` 메서드를 이용해 고객의 "탭"에 여러 개의 일회성 항목(최대 250개)을 추가한 후 인보이스를 발행할 수 있습니다. 예를 들어, 티셔츠 5장과 머그컵 2개를 추가하는 코드는 다음과 같습니다.

```
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

<!-- Alternatively, you may use the `invoiceFor` method to make a "one-off" charge against the customer's default payment method: -->
또 다른 방법으로, `invoiceFor` 메서드를 사용해 고객의 기본 결제 수단으로 임의의 특별 결제(예: "일회성 요금")를 청구할 수 있습니다.

```
$user->invoiceFor('One Time Fee', 500);
```

<!-- Although the `invoiceFor` method is available for you to use, it is recommended that you use the `invoicePrice` and `tabPrice` methods with pre-defined prices. By doing so, you will have access to better analytics and data within your Stripe dashboard regarding your sales on a per-product basis. -->
`invoiceFor` 메서드도 사용 가능하지만, 미리 생성한 가격 ID를 이용해 `invoicePrice` 및 `tabPrice` 메서드를 사용하는 것이 Stripe 대시보드에서 상품별 판매 분석 등 더 나은 데이터를 얻을 수 있으므로 권장합니다.

> [!WARNING]
> `invoice`, `invoicePrice`, `invoiceFor` 메서드는 Stripe 인보이스를 생성하며, 결제 실패 시 재시도를 수행합니다. 인보이스에서 결제 실패 시 재시도를 원하지 않는다면, 첫 결제 실패 후 Stripe API를 사용하여 인보이스를 종료(close)해야 합니다.

<a name="creating-payment-intents"></a>

<!-- ### Creating Payment Intents -->
### Creating Payment Intents

<!-- You can create a new Stripe payment intent by invoking the `pay` method on a billable model instance. Calling this method will create a payment intent that is wrapped in a `Laravel\Cashier\Payment` instance: -->
청구 가능한 모델 인스턴스에서 `pay` 메서드를 호출하면 Stripe Payment Intent(결제 의도)를 새로 만들 수 있습니다. 이 메서드를 호출하면 결제 의도가 `Laravel\Cashier\Payment` 인스턴스에 래핑되어 반환됩니다.

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
결제 의도 생성 후 반환된 client secret을 프론트엔드로 전달하여, 사용자가 브라우저에서 결제를 완료할 수 있습니다. Stripe Payment Intent를 이용한 다양한 결제 플로우 구축에 대해 궁금하다면 [Stripe documentation](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참고하세요.

<!-- When using the `pay` method, the default payment methods that are enabled within your Stripe dashboard will be available to the customer. Alternatively, if you only want to allow for some specific payment methods to be used, you may use the `payWith` method: -->
`pay` 메서드를 사용할 때 Stripe 대시보드의 기본 결제 수단들이 고객에게 제공됩니다. 특정 결제 수단만 허용하고 싶으면 `payWith` 메서드를 사용할 수 있습니다.

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
> `pay` 및 `payWith` 메서드는 결제 금액을 애플리케이션이 사용하는 통화의 최소 단위(예: USD의 경우 센트)로 입력해야 합니다.

<a name="refunding-charges"></a>

<!-- ### Refunding Charges -->
### Refunding Charges

<!-- If you need to refund a Stripe charge, you may use the `refund` method. This method accepts the Stripe [payment intent ID](#payment-methods-for-single-charges) as its first argument: -->
Stripe 결제를 환불하려면 `refund` 메서드를 사용할 수 있습니다. 이 메서드는 Stripe의 [payment intent ID](#payment-methods-for-single-charges)를 첫 번째 인수로 받습니다.

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
청구 가능한 모델의 인보이스 목록을 배열 형태로 간편하게 조회하려면 `invoices` 메서드를 사용합니다. `invoices` 메서드는 `Laravel\Cashier\Invoice` 인스턴스의 컬렉션을 반환합니다.

```
$invoices = $user->invoices();
```

<!-- If you would like to include pending invoices in the results, you may use the `invoicesIncludingPending` method: -->
결제 대기 중인 인보이스도 결과에 포함하려면 `invoicesIncludingPending` 메서드를 사용하면 됩니다.

```
$invoices = $user->invoicesIncludingPending();
```

<!-- You may use the `findInvoice` method to retrieve a specific invoice by its ID: -->
특정 인보이스를 ID로 조회하려면 `findInvoice` 메서드를 사용할 수 있습니다.

```
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>

<!-- #### Displaying Invoice Information -->
#### Displaying Invoice Information

<!-- When listing the invoices for the customer, you may use the invoice's methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them: -->
고객의 인보이스 목록을 표시할 때, 각 인보이스의 다양한 정보를 메서드로 호출하여 보여줄 수 있습니다. 예를 들어, 모든 인보이스를 테이블로 나열하고, 각 인보이스를 쉽게 다운로드할 수 있는 예시는 다음과 같습니다.

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
고객의 다가오는 예정 인보이스를 조회하려면 `upcomingInvoice` 메서드를 사용할 수 있습니다.

```
$invoice = $user->upcomingInvoice();
```

<!-- Similarly, if the customer has multiple subscriptions, you can also retrieve the upcoming invoice for a specific subscription: -->
만약 고객이 여러 구독을 가지고 있다면, 특정 구독에 대한 예정 인보이스도 다음과 같이 조회할 수 있습니다.

```
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>

<!-- ### Previewing Subscription Invoices -->
### Previewing Subscription Invoices

<!-- Using the `previewInvoice` method, you can preview an invoice before making price changes. This will allow you to determine what your customer's invoice will look like when a given price change is made: -->
`previewInvoice` 메서드를 사용하면 가격 변경 전 인보이스를 미리 볼 수 있어, 새로운 가격 적용 시 고객의 인보이스가 어떻게 표시될지 확인할 수 있습니다.

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

<!-- Before generating invoice PDFs, you should use Composer to install the Dompdf library, which is the default invoice renderer for Cashier: -->
인보이스 PDF 생성 전, Cashier의 기본 인보이스 렌더러인 Dompdf 라이브러리를 Composer로 설치해야 합니다.

```php
composer require dompdf/dompdf
```

<!-- From within a route or controller, you may use the `downloadInvoice` method to generate a PDF download of a given invoice. This method will automatically generate the proper HTTP response needed to download the invoice: -->
컨트롤러나 라우트 내에서 `downloadInvoice` 메서드를 사용해 지정한 인보이스의 PDF 파일을 생성하여 다운로드 받을 수 있습니다. 이 메서드는 인보이스 다운로드에 적합한 HTTP 응답을 자동으로 반환합니다.

```
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

<!-- By default, all data on the invoice is derived from the customer and invoice data stored in Stripe. The filename is based on your `app.name` config value. However, you can customize some of this data by providing an array as the second argument to the `downloadInvoice` method. This array allows you to customize information such as your company and product details: -->
기본적으로 인보이스의 모든 데이터는 Stripe에 저장된 고객 및 인보이스 정보를 바탕으로 합니다. 파일명은 `app.name` 설정 값을 기반으로 지정됩니다. 하지만 `downloadInvoice` 메서드의 두 번째 인수로 배열을 전달하여, 회사 정보 및 상품 정보 등 일부 데이터를 커스터마이징할 수도 있습니다.

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
`downloadInvoice` 메서드는 세 번째 인수로 파일 이름을 직접 지정할 수 있으며, 자동으로 `.pdf` 확장자가 붙습니다.

```
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>

<!-- #### Custom Invoice Renderer -->
#### Custom Invoice Renderer

<!-- Cashier also makes it possible to use a custom invoice renderer. By default, Cashier uses the `DompdfInvoiceRenderer` implementation, which utilizes the [dompdf](https://github.com/dompdf/dompdf) PHP library to generate Cashier's invoices. However, you may use any renderer you wish by implementing the `Laravel\Cashier\Contracts\InvoiceRenderer` interface. For example, you may wish to render an invoice PDF using an API call to a third-party PDF rendering service: -->
Cashier에서는 커스텀 인보이스 렌더러 구현도 가능합니다. 기본적으로 Cashier는 `DompdfInvoiceRenderer` 구현체를 사용하고, 여기서 [dompdf](https://github.com/dompdf/dompdf) PHP 라이브러리를 활용해 인보이스를 만듭니다. 하지만 직접 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현하여 원하는 방식의 렌더러를 사용할 수 있습니다. 예를 들어, 외부의 PDF 렌더링 API를 호출하여 인보이스 PDF를 생성할 수 있습니다.

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
인보이스 렌더러 계약(Contract)을 구현한 뒤에는 애플리케이션의 `config/cashier.php` 설정 파일에서 `cashier.invoices.renderer` 설정 값을 커스텀 렌더러 클래스명으로 지정해야 합니다.

<a name="checkout"></a>

<!-- ## Checkout -->
## Checkout

<!-- Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page. -->
Cashier Stripe는 또한 [Stripe Checkout](https://stripe.com/payments/checkout)도 지원합니다. Stripe Checkout은 결제 페이지를 직접 구현하지 않아도 되도록, Stripe에서 미리 만들어 둔 호스팅 결제 페이지를 제공합니다.

<!-- The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout). -->
아래 문서에서는 Cashier와 Stripe Checkout을 연동하는 방법을 안내합니다. Stripe Checkout에 대한 더 자세한 내용은 [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout)도 참고하십시오.

<a name="product-checkouts"></a>

<!-- ### Product Checkouts -->
### Product Checkouts

<!-- You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID: -->
Stripe 대시보드에서 생성된 상품을 대상으로, 청구 가능한 모델에서 `checkout` 메서드를 사용해 체크아웃을 진행할 수 있습니다. `checkout` 메서드는 Stripe Checkout 세션을 새로 시작하며, 기본적으로 Stripe Price ID를 인수로 전달해야 합니다.

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

<!-- If needed, you may also specify a product quantity: -->
필요하다면 상품의 수량도 지정할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

<!-- When a customer visits this route they will be redirected to Stripe's Checkout page. By default, when a user successfully completes or cancels a purchase they will be redirected to your `home` route location, but you may specify custom callback URLs using the `success_url` and `cancel_url` options: -->
이 라우트에 방문한 고객은 Stripe Checkout 결제 페이지로 리디렉션됩니다. 기본적으로 결제가 성공하거나 취소되면 `home` 라우트로 리디렉션되지만, `success_url`과 `cancel_url` 옵션을 사용해 콜백 URL을 직접 지정할 수 있습니다.

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
`success_url` 옵션에 Stripe가 체크아웃 세션 ID를 쿼리스트링 파라미터로 추가해주길 원한다면, `success_url` 쿼리스트링에 `{CHECKOUT_SESSION_ID}` 문자열을 그대로 넣으십시오. Stripe가 이 플레이스홀더를 실제 세션 ID로 치환합니다.

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
기본적으로 Stripe Checkout 결제 페이지는 [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 허용하지 않습니다. 하지만, Cashier에서 `allowPromotionCodes` 메서드를 호출하면 이 기능을 쉽게 활성화할 수 있습니다.

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
Stripe 대시보드에 등록되어 있지 않은 임시 제품에 대해서도 단일 결제를 진행할 수 있습니다. 이때는 billable 모델에서 `checkoutCharge` 메서드를 사용해 금액, 상품명, 선택적으로 수량을 지정해줍니다. 고객이 해당 라우트에 방문하면 Stripe Checkout 페이지로 리디렉션됩니다.

```
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` 메서드를 사용할 경우 Stripe는 Stripe 대시보드에 새로운 상품과 가격을 항상 생성합니다. 따라서 미리 Stripe 대시보드에서 상품을 만들어두고, `checkout` 메서드를 사용하는 방식을 권장합니다.

<a name="subscription-checkouts"></a>

<!-- ### Subscription Checkouts -->
### Subscription Checkouts

> [!WARNING]
> Stripe Checkout으로 구독을 시작하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 반드시 활성화해야 합니다. 이 웹훅이 구독 정보를 데이터베이스에 기록하고 관련 구독 항목도 저장합니다.

<!-- You may also use Stripe Checkout to initiate subscriptions. After defining your subscription with Cashier's subscription builder methods, you may call the `checkout `method. When a customer visits this route they will be redirected to Stripe's Checkout page: -->
Stripe Checkout을 이용해 구독을 시작할 수도 있습니다. Cashier의 구독 빌더 메서드로 구독을 정의한 뒤, `checkout `메서드를 호출하면 준비가 완료됩니다. 고객이 해당 라우트에 방문할 경우 Stripe Checkout 결제 페이지로 이동합니다.

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

<!-- Just as with product checkouts, you may customize the success and cancellation URLs: -->
상품별 체크아웃과 마찬가지로, 성공 및 취소 시 리디렉션될 URL도 지정할 수 있습니다.

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
또한 구독 결제 체크아웃에서도 프로모션 코드 사용을 허용할 수 있습니다.

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
> Stripe Checkout을 사용해 구독을 시작할 때는 일부 구독 청구 옵션(예: `anchorBillingCycleOn` 메서드, 체증(proration) 설정, 결제 동작 설정 등)이 지원되지 않습니다. 사용 가능한 파라미터는 [the Stripe Checkout Session API documentation](https://stripe.com/docs/api/checkout/sessions/create)를 참고하십시오.

<a name="stripe-checkout-trial-periods"></a>

<!-- #### Stripe Checkout & Trial Periods -->
#### Stripe Checkout & Trial Periods

<!-- Of course, you can define a trial period when building a subscription that will be completed using Stripe Checkout: -->
Stripe Checkout으로 진행하는 구독에도 체험 기간을 설정할 수 있습니다.

```
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<!-- However, the trial period must be at least 48 hours, which is the minimum amount of trial time supported by Stripe Checkout. -->
단, Stripe Checkout에서 지원하는 최소 체험 기간은 48시간 이상이어야 합니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>

<!-- #### Subscriptions & Webhooks -->
#### Subscriptions & Webhooks

<!-- Remember, Stripe and Cashier update subscription statuses via webhooks, so there's a possibility a subscription might not yet be active when the customer returns to the application after entering their payment information. To handle this scenario, you may wish to display a message informing the user that their payment or subscription is pending. -->
Stripe와 Cashier는 웹훅을 통해 구독 상태를 갱신하므로, 고객이 결제 정보를 입력하고 애플리케이션으로 돌아왔을 때 아직 구독이 활성화되지 않았을 수도 있습니다. 이런 경우 사용자가 결제 또는 구독이 처리 중임을 알리는 메시지를 화면에 띄우는 것을 권장합니다.

<a name="collecting-tax-ids"></a>

<!-- ### Collecting Tax IDs -->
### Collecting Tax IDs

<!-- Checkout also supports collecting a customer's Tax ID. To enable this on a checkout session, invoke the `collectTaxIds` method when creating the session: -->
Checkout은 고객의 세금 번호(Tax ID)를 수집하는 기능도 지원합니다. 체크아웃 세션을 시작할 때 `collectTaxIds` 메서드를 호출하면 해당 기능이 활성화됩니다.

```
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

<!-- When this method is invoked, a new checkbox will be available to the customer that allows them to indicate if they're purchasing as a company. If so, they will have the opportunity to provide their Tax ID number. -->
이렇게 하면 고객이 회사로 결제하는 경우 세금 번호(Tax ID)를 입력할 수 있는 체크박스가 표시됩니다.

> [!WARNING]
> 만약 애플리케이션의 서비스 프로바이더에서 이미 [automatic tax collection](#tax-configuration)를 설정하였다면, 이 기능은 자동으로 활성화되므로 `collectTaxIds` 메서드를 별도로 호출할 필요가 없습니다.

<a name="guest-checkouts"></a>

<!-- ### Guest Checkouts -->
### Guest Checkouts

<!-- Using the `Checkout::guest` method, you may initiate checkout sessions for guests of your application that do not have an "account": -->
`Checkout::guest` 메서드를 사용하면, 계정이 없는 애플리케이션 게스트 사용자용 체크아웃 세션도 시작할 수 있습니다.

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
사용자 계정이 있는 경우와 마찬가지로, `Laravel\Cashier\CheckoutBuilder` 인스턴스에서 제공하는 다양한 메서드를 활용하여 게스트 체크아웃 세션을 커스터마이징할 수 있습니다.

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
비회원 체크아웃이 완료된 후, Stripe는 `checkout.session.completed` 웹훅 이벤트를 보낼 수 있으니, 반드시 [configure your Stripe webhook](https://dashboard.stripe.com/webhooks)하여 이 이벤트가 애플리케이션에 전달되게 해야 합니다. Stripe 대시보드에서 웹훅을 활성화한 뒤, [handle the webhook with Cashier](#handling-stripe-webhooks)할 수 있습니다. 웹훅 본문에서는 [`checkout` object](https://stripe.com/docs/api/checkout/sessions/object)가 전달되므로, 이를 활용해 고객의 주문을 처리하십시오.

<a name="handling-failed-payments"></a>

<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed. -->
가끔 구독이나 단일 결제에 실패할 수 있습니다. 이 경우 Cashier는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시켜 결제 실패를 알립니다. 이 예외를 캐치한 뒤 두 가지 방식으로 대응할 수 있습니다.

<!-- First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page: -->
첫째, Cashier가 자체 제공하는 결제 확인 페이지로 고객을 리디렉션할 수 있습니다. 이 페이지는 Cashier의 서비스 프로바이더에서 이미 명명된 라우트로 등록되어 있습니다. 따라서, `IncompletePayment` 예외를 캐치하고, 아래와 같이 사용자를 결제 확인 페이지로 리디렉션하면 됩니다.

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
결제 확인 페이지에서는 사용자가 신용카드 정보를 다시 입력하거나, Stripe에서 요구하는 추가 인증(예: "3D Secure")을 진행할 수 있습니다. 결제 완료 후에는 위 예시에서 `redirect` 파라미터로 지정한 URL로 리디렉션됩니다. 이때 `message`(문자열)와 `success`(정수) 쿼리 문자열 변수가 URL에 추가됩니다. 현재 결제 페이지에서 지원하는 결제 수단은 다음과 같습니다.

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
- 신용카드(Credit Cards)
- Alipay
- Bancontact
- BECS Direct Debit
- EPS
- Giropay
- iDEAL
- SEPA Direct Debit

<!-- </div> -->
</div>

<!-- Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions. -->
또 다른 방법으로, Stripe의 결제 확인을 Stripe 자체에서 처리하도록 할 수도 있습니다. 이 경우, 별도의 결제 확인 페이지로 리디렉션하지 않고, Stripe 대시보드에서 [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic)을 활성화하면 됩니다. 단, 이 방법 역시 `IncompletePayment` 예외가 발생했을 때 사용자가 이메일로 안내를 받게 된다는 점을 사전에 꼭 알려야 합니다.

<!-- Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions. -->
`Billable` 트레이트를 사용하는 모델의 `charge`, `invoiceFor`, `invoice` 메서드에서 결제 예외가 발생할 수 있습니다. 구독 관련 기능을 사용할 때는 `SubscriptionBuilder`의 `create` 메서드와 `Subscription`, `SubscriptionItem` 모델의 `incrementAndInvoice`, `swapAndInvoice` 등에서도 불완전 결제 예외가 발생할 수 있습니다.

<!-- Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
기존 구독(Subscription)의 결제가 미완료 상태인지 확인하려면 billable 모델이나 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용하면 됩니다.

```
if ($user->hasIncompletePayment('default')) {
    //
}

if ($user->subscription('default')->hasIncompletePayment()) {
    //
}
```

<!-- You can derive the specific status of an incomplete payment by inspecting the `payment` property on the exception instance: -->
불완전 결제의 구체적 상태는 예외 객체의 `payment` 속성을 통해 확인할 수 있습니다.

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
귀하의 비즈니스 또는 고객 중 일부가 유럽에 기반을 두고 있다면, 유럽연합(EU)에서 정한 강력한 고객 인증(SCA) 규정을 반드시 준수해야 합니다. 이 규정은 2019년 9월에 결제 사기를 방지하기 위해 도입되었습니다. 다행히 Stripe와 Cashier는 SCA 규정에 부합하는 애플리케이션을 손쉽게 구축할 수 있도록 준비되어 있습니다.

> [!WARNING]
> 시작하기 전에, [Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication)와 [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication)를 반드시 검토하시기 바랍니다.

<a name="payments-requiring-additional-confirmation"></a>

<!-- ### Payments Requiring Additional Confirmation -->
### Payments Requiring Additional Confirmation

<!-- SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions be found can be found in the documentation on [handling failed payments](#handling-failed-payments). -->
SCA 규정에 따라 결제를 승인∙처리하려면 추가 인증이 요구되는 경우가 많습니다. 이러한 상황이 발생하면, Cashier는 추가 인증이 필요하다는 사실을 알리는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이러한 예외를 어떻게 처리해야 하는지는 [handling failed payments](#handling-failed-payments) 문서를 참고하시기 바랍니다.

<!-- Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
Stripe 또는 Cashier가 제공하는 결제 인증 화면은 각 은행이나 카드 발급사별 결제 방식에 맞춰 제공되며, 추가 카드 인증, 소액 임시 결제, 별도의 기기 인증 등 다양한 형태의 추가 인증 절차를 포함할 수 있습니다.

<a name="incomplete-and-past-due-state"></a>

<!-- #### Incomplete and Past Due State -->
#### Incomplete and Past Due State

<!-- When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion. -->
결제에 추가 인증이 필요하면, 해당 구독의 `stripe_status` 데이터베이스 컬럼에 따라 구독 상태가 `incomplete`(미완료) 또는 `past_due`(연체)로 유지됩니다. 결제 인증이 완료되고 Stripe에서 웹훅을 통해 완료 사실이 애플리케이션에 통지되는 즉시, Cashier는 자동으로 해당 고객의 구독을 활성화합니다.

<!-- For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status). -->
`incomplete` 및 `past_due` 상태에 대한 자세한 내용은 [our additional documentation on these states](#incomplete-and-past-due-status)를 참고하시기 바랍니다.

<a name="off-session-payment-notifications"></a>

<!-- ### Off-Session Payment Notifications -->
### Off-Session Payment Notifications

<!-- Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to a notification class. By default, this notification is disabled. Of course, Cashier includes a notification class you may use for this purpose, but you are free to provide your own notification class if desired: -->
SCA 규정에 따라, 구독이 활성화된 상태에서도 고객이 결제 정보를 주기적으로 다시 인증해야 할 수 있습니다. Cashier는 오프 세션(off-session, 즉 사용자가 직접 결제 페이지를 방문하지 않았을 때) 결제 인증이 필요할 때 고객에게 알림을 발송할 수 있습니다. 예를 들어, 구독이 갱신되는 시점에 이러한 상황이 발생할 수 있습니다. Cashier의 결제 알림 기능은 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수에 알림 클래스를 지정하여 활성화할 수 있습니다. 기본적으로는 이 알림 기능이 비활성화되어 있습니다. 물론, Cashier에서 제공하는 기본 알림 클래스를 사용할 수 있지만, 필요하다면 직접 정의한 알림 클래스를 사용해도 됩니다.

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

<!-- To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait. -->
오프 세션 결제 인증 알림이 제대로 발송되도록 하려면, [Stripe webhooks are configured](#handling-stripe-webhooks)이 완료되어 있어야 하며, Stripe 대시보드에서 `invoice.payment_action_required` 웹훅 이벤트가 활성화되어 있어야 합니다. 추가로, `Billable` 모델에 Laravel의 `Illuminate\Notifications\Notifiable` 트레이트도 적용되어 있어야 합니다.

> [!WARNING]
> 고객이 수동으로 결제를 진행하다가 추가 인증이 필요한 경우에도 알림이 전송됩니다. Stripe에서는 결제가 수동으로 이루어진 것인지(수동 결제) 또는 오프 세션 결제인지를 구분할 방법이 없기 때문입니다. 하지만, 고객이 이미 결제를 완료한 뒤 결제 페이지를 다시 방문하면 단순히 "결제 성공" 메시지만 확인하게 되고, 동일 결제를 두 번 인증해 중복 결제가 발생할 일은 없으니 안심하셔도 됩니다.

<a name="stripe-sdk"></a>

<!-- ## Stripe SDK -->
## Stripe SDK

<!-- Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method: -->
Cashier의 다양한 객체들은 Stripe SDK 객체를 감싸는 래퍼(wrapper) 역할을 합니다. Stripe의 실제 객체와 직접 상호작용하고 싶다면, `asStripe` 메서드를 사용해 간편하게 해당 객체를 얻을 수 있습니다.

```
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

<!-- You may also use the `updateStripeSubscription` method to update a Stripe subscription directly: -->
또한, Stripe 구독을 직접 업데이트하려면 `updateStripeSubscription` 메서드를 사용할 수 있습니다.

```
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

<!-- You may invoke the `stripe` method on the `Cashier` class if you would like to use the `Stripe\StripeClient` client directly. For example, you could use this method to access the `StripeClient` instance and retrieve a list of prices from your Stripe account: -->
`Stripe\StripeClient` 클라이언트를 직접 사용하고 싶다면, `Cashier` 클래스의 `stripe` 메서드를 호출하면 됩니다. 예를 들어, 이 메서드로 `StripeClient` 인스턴스에 접근해 Stripe 계정에 등록된 가격 목록을 조회할 수 있습니다.

```
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>

<!-- ## Testing -->
## Testing

<!-- When testing an application that uses Cashier, you may mock the actual HTTP requests to the Stripe API; however, this requires you to partially re-implement Cashier's own behavior. Therefore, we recommend allowing your tests to hit the actual Stripe API. While this is slower, it provides more confidence that your application is working as expected and any slow tests may be placed within their own PHPUnit testing group. -->
Cashier를 사용하는 애플리케이션을 테스트할 때, 실제 Stripe API로 보내는 HTTP 요청을 모킹(mock)할 수 있습니다. 하지만, 이 방법은 Cashier 내부 동작을 일부 재구현해야 하므로 권장하지 않습니다. 따라서 실제 Stripe API를 테스트가 직접 호출하도록 하는 것이 더 좋습니다. 비록 테스트가 조금 느려질 수 있지만, 실제 애플리케이션이 의도대로 동작한다는 신뢰성을 확보할 수 있고, 느린 테스트는 별도의 PHPUnit 테스트 그룹으로 분리하면 됩니다.

<!-- When testing, remember that Cashier itself already has a great test suite, so you should only focus on testing the subscription and payment flow of your own application and not every underlying Cashier behavior. -->
Cashier는 이미 자체적으로 훌륭한 테스트 스위트를 보유하고 있으므로, 여러분은 자신의 애플리케이션에서 사용하는 구독 및 결제 흐름 위주로만 테스트를 수행하면 됩니다. Cashier 내부의 모든 행동까지 직접 테스트할 필요는 없습니다.

<!-- To get started, add the **testing** version of your Stripe secret to your `phpunit.xml` file: -->
테스트를 시작하려면, Stripe 시크릿의 **테스트** 버전을 `phpunit.xml` 파일에 추가하면 됩니다.

```
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

<!-- Now, whenever you interact with Cashier while testing, it will send actual API requests to your Stripe testing environment. For convenience, you should pre-fill your Stripe testing account with subscriptions / prices that you may use during testing. -->
이제 테스트 시 Cashier와 상호작용하는 모든 과정에서 실제 Stripe 테스트 환경으로 API 요청이 전송됩니다. 편의를 위해, 테스트용 Stripe 계정에 구독/가격 정보를 미리 등록해 두면 좋습니다.

> [!NOTE]
> 다양한 결제 시나리오(예: 카드 거절, 결제 실패)를 테스트하려면, Stripe에서 제공하는 [testing card numbers and tokens](https://stripe.com/docs/testing)을 활용할 수 있습니다.
