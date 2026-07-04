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
[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe) は、[Stripe's](https://stripe.com) サブスクリプション請求サービスへの表現力豊かで流暢なインターフェイスを提供します。あなたが書くのを恐れている定型的なサブスクリプション請求コードのほぼすべてを処理します。基本的なサブスクリプション管理に加えて、Cashier はクーポン、サブスクリプションの交換、サブスクリプションの「数量」、キャンセル猶予期間を処理し、請求書の PDF を生成することもできます。

<a name="upgrading-cashier"></a>
<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md). -->
Cashier の新しいバージョンにアップグレードする場合は、[the upgrade guide](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md) を注意深く確認することが重要です。

> [!WARNING]
> 重大な変更を防ぐために、Cashier は固定の Stripe API バージョンを使用します。 Cashier 16 は、Stripe API バージョン `2025-06-30.basil` を利用します。 Stripe API バージョンは、Stripe の新しい機能と改善を利用するためにマイナー リリースで更新されます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Stripe using the Composer package manager: -->
まず、Composer パッケージ マネージャーを使用して Stripe の Cashier パッケージをインストールします。

```shell
composer require laravel/cashier
```

<!-- After installing the package, publish Cashier's migrations using the `vendor:publish` Artisan command: -->
パッケージをインストールした後、`vendor:publish` Artisan コマンドを使用して Cashier の移行を公開します。

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- Then, migrate your database: -->
次に、データベースを移行します。

```shell
php artisan migrate
```

<!-- Cashier's migrations will add several columns to your `users` table. They will also create a new `subscriptions` table to hold all of your customer's subscriptions and a `subscription_items` table for subscriptions with multiple prices. -->
Cashier の移行により、`users` テーブルにいくつかの列が追加されます。また、顧客のすべてのサブスクリプションを保持する新しい `subscriptions` テーブルと、複数の価格のサブスクリプション用の `subscription_items` テーブルも作成されます。

<!-- If you wish, you can also publish Cashier's configuration file using the `vendor:publish` Artisan command: -->
必要に応じて、`vendor:publish` Artisan コマンドを使用して、Cashier の構成ファイルを公開することもできます。

```shell
php artisan vendor:publish --tag="cashier-config"
```

<!-- Lastly, to ensure Cashier properly handles all Stripe events, remember to [configure Cashier's webhook handling](#handling-stripe-webhooks). -->
最後に、Cashier がすべての Stripe イベントを適切に処理できるようにするには、[configure Cashier's webhook handling](#handling-stripe-webhooks) を忘れないでください。

> [!WARNING]
> Stripe では、Stripe 識別子の格納に使用される列では大文字と小文字を区別することをお勧めします。したがって、MySQL を使用する場合は、`stripe_id` 列の列照合順序が `utf8_bin` に設定されていることを確認する必要があります。これに関する詳細については、[Stripe documentation](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible) を参照してください。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>
<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, add the `Billable` trait to your billable model definition. Typically, this will be the `App\Models\User` model. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information: -->
Cashier を使用する前に、`Billable` 特性を請求可能モデル定義に追加します。通常、これは `App\Models\User` モデルになります。この特性は、サブスクリプションの作成、クーポンの適用、支払い方法情報の更新などの一般的な請求タスクを実行できるようにするさまざまなメソッドを提供します。

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- Cashier assumes your billable model will be the `App\Models\User` class that ships with Laravel. If you wish to change this you may specify a different model via the `useCustomerModel` method. This method should typically be called in the `boot` method of your `AppServiceProvider` class: -->
Cashier は、請求可能なモデルが Laravel に同梱される `App\Models\User` クラスであると想定します。これを変更したい場合は、`useCustomerModel` メソッドで別のモデルを指定できます。このメソッドは通常、`AppServiceProvider` クラスの `boot` メソッドで呼び出す必要があります。

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
> Laravel が提供する `App\Models\User` モデル以外のモデルを使用している場合は、提供される [Cashier migrations](#installation) を公開し、代替モデルのテーブル名と一致するように変更する必要があります。

<a name="api-keys"></a>
<!-- ### API Keys -->
### API Keys

<!-- Next, you should configure your Stripe API keys in your application's `.env` file. You can retrieve your Stripe API keys from the Stripe control panel: -->
次に、アプリケーションの `.env` ファイルで Stripe API キーを構成する必要があります。 Stripe API キーは、Stripe コントロール パネルから取得できます。

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 環境変数がアプリケーションの `.env` ファイルで定義されていることを確認する必要があります。この変数は、受信 Webhook が実際に Stripe からのものであることを確認するために使用されます。

<a name="currency-configuration"></a>
<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
デフォルトのCashier通貨は米ドル (USD) です。アプリケーションの `.env` ファイル内で `CASHIER_CURRENCY` 環境変数を設定することで、デフォルトの通貨を変更できます。

```ini
CASHIER_CURRENCY=eur
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
Cashier の通貨を構成することに加えて、請求書に表示する金額の書式を設定するときに使用するロケールを指定することもできます。内部的には、Cashier は [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) を使用して通貨ロケールを設定します。

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 以外のロケールを使用するには、`ext-intl` PHP 拡張機能がサーバーにインストールされ、構成されていることを確認してください。

<a name="tax-configuration"></a>
<!-- ### Tax Configuration -->
### Tax Configuration

<!-- Thanks to [Stripe Tax](https://stripe.com/tax), it's possible to automatically calculate taxes for all invoices generated by Stripe. You can enable automatic tax calculation by invoking the `calculateTaxes` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
[Stripe Tax](https://stripe.com/tax) のおかげで、Stripe によって生成されたすべての請求書の税金を自動的に計算することができます。自動税金計算を有効にするには、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドで `calculateTaxes` メソッドを呼び出します。

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
税計算が有効になると、新しいサブスクリプションと生成される 1 回限りの請求書で自動的に税計算が行われるようになります。

<!-- For this feature to work properly, your customer's billing details, such as the customer's name, address, and tax ID, need to be synced to Stripe. You may use the [customer data synchronization](#syncing-customer-data-with-stripe) and [Tax ID](#tax-ids) methods offered by Cashier to accomplish this. -->
この機能が適切に動作するには、顧客の名前、住所、納税者番号などの請求詳細が Stripe に同期される必要があります。これを実現するには、Cashier が提供する [customer data synchronization](#syncing-customer-data-with-stripe) および [Tax ID](#tax-ids) メソッドを使用できます。

<a name="logging"></a>
<!-- ### Logging -->
### Logging

<!-- Cashier allows you to specify the log channel to be used when logging fatal Stripe errors. You may specify the log channel by defining the `CASHIER_LOGGER` environment variable within your application's `.env` file: -->
Cashier を使用すると、致命的な Stripe エラーを記録するときに使用するログ チャネルを指定できます。アプリケーションの `.env` ファイル内で `CASHIER_LOGGER` 環境変数を定義することで、ログ チャネルを指定できます。

```ini
CASHIER_LOGGER=stack
```

<!-- Exceptions that are generated by API calls to Stripe will be logged through your application's default log channel. -->
Stripe への API 呼び出しによって生成された例外は、アプリケーションのデフォルトのログ チャネルを通じて記録されます。

<a name="using-custom-models"></a>
<!-- ### Using Custom Models -->
### Using Custom Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
独自のモデルを定義し、対応する Cashier モデルを拡張することで、Cashier によって内部的に使用されるモデルを自由に拡張できます。

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Cashier\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
モデルを定義した後、`Laravel\Cashier\Cashier` クラスを介してカスタム モデルを使用するように Cashier に指示できます。通常、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドでカスタム モデルについて Cashier に通知する必要があります。

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
> Stripe Checkout を利用する前に、Stripe ダッシュボードで固定価格の製品を定義する必要があります。さらに、[configure Cashier's webhook handling](#handling-stripe-webhooks) を実行する必要があります。

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations. -->
アプリケーション経由で製品やサブスクリプションの請求を行うのは、威圧的な場合があります。ただし、Cashier と [Stripe Checkout](https://stripe.com/payments/checkout) のおかげで、最新の堅牢な支払い統合を簡単に構築できます。

<!-- To charge customers for non-recurring, single-charge products, we'll utilize Cashier to direct customers to Stripe Checkout, where they will provide their payment details and confirm their purchase. Once the payment has been made via Checkout, the customer will be redirected to a success URL of your choosing within your application: -->
非定期的な 1 回限りの製品に対して顧客に請求するには、Cashier を利用して顧客を Stripe Checkout に誘導し、そこで支払いの詳細を入力して購入を確認します。 Checkout 経由で支払いが完了すると、顧客はアプリケーション内で選択した成功 URL にリダイレクトされます。

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
上の例でわかるように、Cashierが提供する `checkout` メソッドを利用して、顧客を特定の「価格識別子」の Stripe Checkout にリダイレクトします。 Stripe を使用する場合、「価格」は [defined prices for specific products](https://stripe.com/docs/products-prices/how-products-and-prices-work) を指します。

<!-- If necessary, the `checkout` method will automatically create a customer in Stripe and connect that Stripe customer record to the corresponding user in your application's database. After completing the checkout session, the customer will be redirected to a dedicated success or cancellation page where you can display an informational message to the customer. -->
必要に応じて、`checkout` メソッドは Stripe に顧客を自動的に作成し、その Stripe 顧客レコードをアプリケーションのデータベース内の対応するユーザーに接続します。チェックアウト セッションが完了すると、顧客は専用の成功ページまたはキャンセル ページにリダイレクトされ、そこで顧客に情報メッセージを表示できます。

<a name="providing-meta-data-to-stripe-checkout"></a>
<!-- #### Providing Meta Data to Stripe Checkout -->
#### Providing Meta Data to Stripe Checkout

<!-- When selling products, it's common to keep track of completed orders and purchased products via `Cart` and `Order` models defined by your own application. When redirecting customers to Stripe Checkout to complete a purchase, you may need to provide an existing order identifier so that you can associate the completed purchase with the corresponding order when the customer is redirected back to your application. -->
製品を販売する場合、独自のアプリケーションで定義された `Cart` および `Order` モデルを介して、完了した注文と購入した製品を追跡するのが一般的です。購入を完了するために顧客を Stripe Checkout にリダイレクトする場合、顧客がアプリケーションにリダイレクトされて戻ったときに、完了した購入を対応する注文に関連付けることができるように、既存の注文 ID を提供することが必要になる場合があります。

<!-- To accomplish this, you may provide an array of `metadata` to the `checkout` method. Let's imagine that a pending `Order` is created within our application when a user begins the checkout process. Remember, the `Cart` and `Order` models in this example are illustrative and not provided by Cashier. You are free to implement these concepts based on the needs of your own application: -->
これを実現するには、`metadata` の配列を `checkout` メソッドに提供します。ユーザーがチェックアウトプロセスを開始したときに、アプリケーション内で保留中の `Order` が作成されると想像してみましょう。この例の `Cart` モデルと `Order` モデルは説明用であり、Cashier によって提供されるものではないことに注意してください。独自のアプリケーションのニーズに基づいて、これらの概念を自由に実装できます。

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
上の例でわかるように、ユーザーがチェックアウト プロセスを開始すると、カート/注文に関連付けられたすべての Stripe 価格識別子が `checkout` メソッドに提供されます。もちろん、アプリケーションは、顧客がこれらの商品を追加したときに、これらの商品を「ショッピング カート」または注文に関連付ける責任があります。また、`metadata` 配列を介して注文の ID を Stripe Checkout セッションに提供します。最後に、`CHECKOUT_SESSION_ID` テンプレート変数をチェックアウト成功ルートに追加しました。 Stripe が顧客をアプリケーションにリダイレクトすると、このテンプレート変数にはチェックアウト セッション ID が自動的に設定されます。

<!-- Next, let's build the Checkout success route. This is the route that users will be redirected to after their purchase has been completed via Stripe Checkout. Within this route, we can retrieve the Stripe Checkout session ID and the associated Stripe Checkout instance in order to access our provided meta data and update our customer's order accordingly: -->
次に、Checkout 成功ルートを構築しましょう。これは、Stripe Checkout 経由で購入が完了した後にユーザーがリダイレクトされるルートです。このルート内で、提供されたメタデータにアクセスし、それに応じて顧客の注文を更新するために、Stripe Checkout セッション ID と関連する Stripe Checkout インスタンスを取得できます。

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
[data contained by the Checkout session object](https://stripe.com/docs/api/checkout/sessions/object) の詳細については、Stripe のドキュメントを参照してください。

<a name="quickstart-selling-subscriptions"></a>
<!-- ### Selling Subscriptions -->
### Selling Subscriptions

> [!NOTE]
> Stripe Checkout を利用する前に、Stripe ダッシュボードで固定価格の製品を定義する必要があります。さらに、[configure Cashier's webhook handling](#handling-stripe-webhooks) を実行する必要があります。

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations. -->
アプリケーション経由で製品やサブスクリプションの請求を行うのは、威圧的な場合があります。ただし、Cashier と [Stripe Checkout](https://stripe.com/payments/checkout) のおかげで、最新の堅牢な支払い統合を簡単に構築できます。

<!-- To learn how to sell subscriptions using Cashier and Stripe Checkout, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Stripe dashboard. In addition, our subscription service might offer an Expert plan as `pro_expert`. -->
Cashier と Stripe Checkout を使用してサブスクリプションを販売する方法を学ぶために、基本的な月次 (`price_basic_monthly`) および年次 (`price_basic_yearly`) プランを持つサブスクリプション サービスの簡単なシナリオを考えてみましょう。これら 2 つの価格は、Stripe ダッシュボードの「Basic」製品 (`pro_basic`) にグループ化できます。さらに、当社のサブスクリプション サービスでは、`pro_expert` としてエキスパート プランを提供する場合があります。

<!-- First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button or link should direct the user to a Laravel route which creates the Stripe Checkout session for their chosen plan: -->
まず、顧客がサービスに登録する方法を見てみましょう。もちろん、顧客がアプリケーションの価格設定ページでベーシック プランの「購読」ボタンをクリックする可能性があることは想像できます。このボタンまたはリンクは、選択したプランの Stripe Checkout セッションを作成する Laravel ルートにユーザーを誘導する必要があります。

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
上の例でわかるように、顧客を Stripe Checkout セッションにリダイレクトし、ベーシック プランに加入できるようにします。チェックアウトまたはキャンセルが成功すると、顧客は `checkout` メソッドに指定した URL にリダイレクトされます。サブスクリプションが実際にいつ開始されたかを知るには (支払い方法によっては処理に数秒かかるため)、[configure Cashier's webhook handling](#handling-stripe-webhooks) も必要になります。

<!-- Now that customers can start subscriptions, we need to restrict certain portions of our application so that only subscribed users can access them. Of course, we can always determine a user's current subscription status via the `subscribed` method provided by Cashier's `Billable` trait: -->
顧客がサブスクリプションを開始できるようになったので、アプリケーションの特定の部分を制限して、サブスクライブしたユーザーのみがアクセスできるようにする必要があります。もちろん、Cashier の `Billable` トレイトによって提供される `subscribed` メソッドを介して、ユーザーの現在のサブスクリプション ステータスをいつでも確認できます。

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

<!-- We can even easily determine if a user is subscribed to specific product or price: -->
ユーザーが特定の製品や価格を購読しているかどうかを簡単に判断することもできます。

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
便宜上、受信リクエストが購読ユーザーからのものであるかどうかを判断する [middleware](/docs/12.x/middleware) を作成するとよいでしょう。このミドルウェアを定義したら、それをルートに簡単に割り当てて、サブスクライブされていないユーザーがルートにアクセスできないようにすることができます。

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
ミドルウェアを定義したら、それをルートに割り当てることができます。

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
もちろん、顧客はサブスクリプション プランを別の製品または「階層」に変更したい場合もあります。これを許可する最も簡単な方法は、顧客を Stripe の [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal) に誘導することです。これは、顧客が請求書のダウンロード、支払い方法の更新、サブスクリプション プランの変更を可能にするホスト型ユーザー インターフェイスを提供します。

<!-- First, define a link or button within your application that directs users to a Laravel route which we will utilize to initiate a Billing Portal session: -->
まず、Billing Portal セッションを開始するために利用する Laravel ルートにユーザーを誘導するリンクまたはボタンをアプリケーション内に定義します。

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

<!-- Next, let's define the route that initiates a Stripe Customer Billing Portal session and redirects the user to the Portal. The `redirectToBillingPortal` method accepts the URL that users should be returned to when exiting the Portal: -->
次に、Stripe Customer Billing Portal セッションを開始し、ユーザーをポータルにリダイレクトするルートを定義しましょう。 `redirectToBillingPortal` メソッドは、ポータルを終了するときにユーザーが戻る URL を受け入れます。

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier の Webhook 処理を構成している限り、Cashier は Stripe から受信した Webhook を検査することで、アプリケーションの Cashier 関連のデータベース テーブルの同期を自動的に維持します。したがって、たとえば、ユーザーが Stripe の顧客請求ポータル経由でサブスクリプションをキャンセルすると、Cashier は対応する Webhook を受け取り、アプリケーションのデータベース内でサブスクリプションを「キャンセル済み」としてマークします。

<a name="customers"></a>
<!-- ## Customers -->
## Customers

<a name="retrieving-customers"></a>
<!-- ### Retrieving Customers -->
### Retrieving Customers

<!-- You can retrieve a customer by their Stripe ID using the `Cashier::findBillable` method. This method will return an instance of the billable model: -->
`Cashier::findBillable` メソッドを使用して、Stripe ID によって顧客を取得できます。このメソッドは、課金対象モデルのインスタンスを返します。

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
<!-- ### Creating Customers -->
### Creating Customers

<!-- Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method: -->
場合によっては、サブスクリプションを開始せずに Stripe 顧客を作成したい場合があります。これは、`createAsStripeCustomer` メソッドを使用して実行できます。

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

<!-- Once the customer has been created in Stripe, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create): -->
Stripe で顧客を作成したら、後日サブスクリプションを開始できます。オプションの `$options` 配列を指定して、追加の [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create) を渡すことができます。

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

<!-- You may use the `asStripeCustomer` method if you want to return the Stripe customer object for a billable model: -->
課金対象モデルの Stripe 顧客オブジェクトを返したい場合は、`asStripeCustomer` メソッドを使用できます。

```php
$stripeCustomer = $user->asStripeCustomer();
```

<!-- The `createOrGetStripeCustomer` method may be used if you would like to retrieve the Stripe customer object for a given billable model but are not sure whether the billable model is already a customer within Stripe. This method will create a new customer in Stripe if one does not already exist: -->
`createOrGetStripeCustomer` メソッドは、特定の請求可能モデルの Stripe 顧客オブジェクトを取得したいが、請求可能モデルがすでに Stripe 内の顧客であるかどうかが不明な場合に使用できます。このメソッドは、Stripe に新しい顧客がまだ存在しない場合に作成します。

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
<!-- ### Updating Customers -->
### Updating Customers

<!-- Occasionally, you may wish to update the Stripe customer directly with additional information. You may accomplish this using the `updateStripeCustomer` method. This method accepts an array of [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update): -->
場合によっては、Stripe 顧客に追加情報を直接更新したい場合があります。これは、`updateStripeCustomer` メソッドを使用して実行できます。このメソッドは、[customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update) の配列を受け入れます。

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
<!-- ### Balances -->
### Balances

<!-- Stripe allows you to credit or debit a customer's "balance". Later, this balance will be credited or debited on new invoices. To check the customer's total balance you may use the `balance` method that is available on your billable model. The `balance` method will return a formatted string representation of the balance in the customer's currency: -->
Stripe では、顧客の「残高」を入金または借方記入することができます。後で、この残高は新しい請求書に記入または借方記入されます。顧客の合計残高を確認するには、請求対象モデルで利用できる `balance` メソッドを使用できます。 `balance` メソッドは、顧客の通貨で残高を表すフォーマットされた文字列を返します。

```php
$balance = $user->balance();
```

<!-- To credit a customer's balance, you may provide a value to the `creditBalance` method. If you wish, you may also provide a description: -->
顧客の残高を入金するには、`creditBalance` メソッドに値を指定できます。必要に応じて、説明も入力できます。

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

<!-- Providing a value to the `debitBalance` method will debit the customer's balance: -->
`debitBalance` メソッドに値を指定すると、顧客の残高が引き落とされます。

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

<!-- The `applyBalance` method will create new customer balance transactions for the customer. You may retrieve these transaction records using the `balanceTransactions` method, which may be useful in order to provide a log of credits and debits for the customer to review: -->
`applyBalance` メソッドは、顧客の新しい顧客残高トランザクションを作成します。これらのトランザクション レコードは、`balanceTransactions` メソッドを使用して取得できます。これは、顧客が確認できる貸方と借方のログを提供するのに役立ちます。

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
Cashier は、顧客の納税者番号を管理する簡単な方法を提供します。たとえば、`taxIds` メソッドを使用して、顧客に割り当てられたすべての [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object) をコレクションとして取得できます。

```php
$taxIds = $user->taxIds();
```

<!-- You can also retrieve a specific tax ID for a customer by its identifier: -->
顧客の特​​定の納税者 ID を識別子によって取得することもできます。

```php
$taxId = $user->findTaxId('txi_belgium');
```

<!-- You may create a new Tax ID by providing a valid [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) and value to the `createTaxId` method: -->
有効な [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) と値を `createTaxId` メソッドに指定することで、新しい税 ID を作成できます。

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

<!-- The `createTaxId` method will immediately add the VAT ID to the customer's account. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); however, this is an asynchronous process. You can be notified of verification updates by subscribing to the `customer.tax_id.updated` webhook event and inspecting [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). For more information on handling webhooks, please consult the [documentation on defining webhook handlers](#handling-stripe-webhooks). -->
`createTaxId` メソッドは、顧客のアカウントに VAT ID をすぐに追加します。 [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation);ただし、これは非同期プロセスです。 `customer.tax_id.updated` Webhook イベントをサブスクライブし、[the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification) を検査することで、検証の更新の通知を受け取ることができます。 Webhook の処理の詳細については、[documentation on defining webhook handlers](#handling-stripe-webhooks) を参照してください。

<!-- You may delete a tax ID using the `deleteTaxId` method: -->
`deleteTaxId` メソッドを使用して納税者 ID を削除できます。

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
<!-- ### Syncing Customer Data With Stripe -->
### Syncing Customer Data With Stripe

<!-- Typically, when your application's users update their name, email address, or other information that is also stored by Stripe, you should inform Stripe of the updates. By doing so, Stripe's copy of the information will be in sync with your application's. -->
通常、アプリケーションのユーザーが自分の名前、電子メール アドレス、または Stripe によって保存されているその他の情報を更新する場合は、Stripe に更新を通知する必要があります。そうすることで、Stripe の情報のコピーがアプリケーションの情報と同期されます。

<!-- To automate this, you may define an event listener on your billable model that reacts to the model's `updated` event. Then, within your event listener, you may invoke the `syncStripeCustomerDetails` method on the model: -->
これを自動化するには、モデルの `updated` イベントに反応するイベント リスナを課金対象モデルに定義できます。次に、イベント リスナ内で、モデルに対して `syncStripeCustomerDetails` メソッドを呼び出すことができます。

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
これで、顧客モデルが更新されるたびに、その情報が Stripe と同期されるようになります。便宜上、Cashier は顧客の最初の作成時に顧客情報を Stripe と自動的に同期します。

<!-- You may customize the columns used for syncing customer information to Stripe by overriding a variety of methods provided by Cashier. For example, you may override the `stripeName` method to customize the attribute that should be considered the customer's "name" when Cashier syncs customer information to Stripe: -->
Cashier が提供するさまざまなメソッドをオーバーライドすることで、顧客情報を Stripe に同期するために使用される列をカスタマイズできます。たとえば、`stripeName` メソッドをオーバーライドして、Cashier が顧客情報を Stripe に同期するときに顧客の「名前」とみなされる属性をカスタマイズできます。

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
同様に、`stripeEmail`、`stripePhone` (最大 20 文字)、`stripeAddress`、および `stripePreferredLocales` メソッドをオーバーライドできます。これらのメソッドは、[updating the Stripe customer object](https://stripe.com/docs/api/customers/update) のときに、対応する顧客パラメータに情報を同期します。顧客情報の同期プロセスを完全に制御したい場合は、`syncStripeCustomerDetails` メソッドをオーバーライドできます。

<a name="billing-portal"></a>
<!-- ### Billing Portal -->
### Billing Portal

<!-- Stripe offers [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) so that your customer can manage their subscription, payment methods, and view their billing history. You can redirect your users to the billing portal by invoking the `redirectToBillingPortal` method on the billable model from a controller or route: -->
Stripe は、顧客がサブスクリプション、支払い方法を管理し、請求履歴を表示できるように [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) を提供します。コントローラまたはルートから課金対象モデルの `redirectToBillingPortal` メソッドを呼び出すことで、ユーザーを課金ポータルにリダイレクトできます。

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

<!-- By default, when the user is finished managing their subscription, they will be able to return to the `home` route of your application via a link within the Stripe billing portal. You may provide a custom URL that the user should return to by passing the URL as an argument to the `redirectToBillingPortal` method: -->
デフォルトでは、ユーザーはサブスクリプションの管理を終了すると、Stripe 請求ポータル内のリンクを介してアプリケーションの `home` ルートに戻ることができます。 URL を引数として `redirectToBillingPortal` メソッドに渡すことで、ユーザーが戻るカスタム URL を指定できます。

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

<!-- If you would like to generate the URL to the billing portal without generating an HTTP redirect response, you may invoke the `billingPortalUrl` method: -->
HTTP リダイレクト応答を生成せずに課金ポータルへの URL を生成したい場合は、`billingPortalUrl` メソッドを呼び出します。

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
Stripe でサブスクリプションを作成したり、「1 回限り」の請求を実行するには、支払い方法を保存し、Stripe からその識別子を取得する必要があります。これを達成するために使用されるアプローチは、サブスクリプションまたは単一料金のどちらの支払い方法を使用する予定であるかによって異なります。そのため、以下では両方について検討します。

<a name="payment-methods-for-subscriptions"></a>
<!-- #### Payment Methods for Subscriptions -->
#### Payment Methods for Subscriptions

<!-- When storing a customer's credit card information for future use by a subscription, the Stripe "Setup Intents" API must be used to securely gather the customer's payment method details. A "Setup Intent" indicates to Stripe the intention to charge a customer's payment method. Cashier's `Billable` trait includes the `createSetupIntent` method to easily create a new Setup Intent. You should invoke this method from the route or controller that will render the form which gathers your customer's payment method details: -->
サブスクリプションで将来使用するために顧客のクレジット カード情報を保存する場合は、Stripe の「Setup Intents」API を使用して顧客の支払い方法の詳細を安全に収集する必要があります。 「セットアップ インテント」は、顧客の支払い方法に請求する意図を Stripe に示します。 Cashier の `Billable` トレイトには、新しいセットアップ インテントを簡単に作成するための `createSetupIntent` メソッドが含まれています。このメソッドは、顧客の支払い方法の詳細を収集するフォームをレンダリングするルートまたはコントローラから呼び出す必要があります。

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

<!-- After you have created the Setup Intent and passed it to the view, you should attach its secret to the element that will gather the payment method. For example, consider this "update payment method" form: -->
Setup Intent を作成してビューに渡した後、支払い方法を収集する要素にそのシークレットを添付する必要があります。たとえば、次の「支払い方法の更新」フォームについて考えてみましょう。

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

<!-- Next, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
次に、Stripe.js ライブラリを使用して、[Stripe Element](https://stripe.com/docs/stripe-js) をフォームに添付し、顧客の支払い詳細を安全に収集します。

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
次に、カードを検証し、[Stripe's `confirmCardSetup` method](https://stripe.com/docs/js/setup_intents/confirm_card_setup) を使用して Stripe から安全な「支払い方法識別子」を取得できます。

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
Stripe によってカードが検証された後、結果の `setupIntent.payment_method` 識別子を Laravel アプリケーションに渡し、そこで顧客に添付できます。支払い方法は、[added as a new payment method](#adding-payment-methods) または [used to update the default payment method](#updating-the-default-payment-method) のいずれかです。支払い方法識別子をすぐに [create a new subscription](#creating-subscriptions) に使用することもできます。

> [!NOTE]
> セットアップ インテントおよび顧客の支払い詳細の収集に関する詳細情報が必要な場合は、[review this overview provided by Stripe](https://stripe.com/docs/payments/save-and-reuse#php) までお問い合わせください。

<a name="payment-methods-for-single-charges"></a>
<!-- #### Payment Methods for Single Charges -->
#### Payment Methods for Single Charges

<!-- Of course, when making a single charge against a customer's payment method, we will only need to use a payment method identifier once. Due to Stripe limitations, you may not use the stored default payment method of a customer for single charges. You must allow the customer to enter their payment method details using the Stripe.js library. For example, consider the following form: -->
もちろん、顧客の支払い方法に対して 1 回の請求を行う場合、支払い方法識別子を使用する必要があるのは 1 回だけです。 Stripe の制限により、顧客の保存されているデフォルトの支払い方法を 1 回の請求に使用することはできません。 Stripe.js ライブラリを使用して顧客が支払い方法の詳細を入力できるようにする必要があります。たとえば、次の形式を考えてみましょう。

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

<!-- After defining such a form, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details: -->
このようなフォームを定義した後、Stripe.js ライブラリを使用して [Stripe Element](https://stripe.com/docs/stripe-js) をフォームに添付し、顧客の支払い詳細を安全に収集できます。

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
次に、カードを検証し、[Stripe's `createPaymentMethod` method](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method) を使用して Stripe から安全な「支払い方法識別子」を取得できます。

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
カードが正常に検証された場合は、`paymentMethod.id` を Laravel アプリケーションに渡し、[single charge](#simple-charge) を処理できます。

<a name="retrieving-payment-methods"></a>
<!-- ### Retrieving Payment Methods -->
### Retrieving Payment Methods

<!-- The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances: -->
課金対象モデル インスタンスの `paymentMethods` メソッドは、`Laravel\Cashier\PaymentMethod` インスタンスのコレクションを返します。

```php
$paymentMethods = $user->paymentMethods();
```

<!-- By default, this method will return payment methods of every type. To retrieve payment methods of a specific type, you may pass the `type` as an argument to the method: -->
デフォルトでは、このメソッドはあらゆる種類の支払い方法を返します。特定のタイプの支払い方法を取得するには、メソッドの引数として `type` を渡すことができます。

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

<!-- To retrieve the customer's default payment method, the `defaultPaymentMethod` method may be used: -->
顧客のデフォルトの支払い方法を取得するには、`defaultPaymentMethod` メソッドを使用できます。

```php
$paymentMethod = $user->defaultPaymentMethod();
```

<!-- You can retrieve a specific payment method that is attached to the billable model using the `findPaymentMethod` method: -->
`findPaymentMethod` メソッドを使用して、請求可能なモデルに関連付けられている特定の支払い方法を取得できます。

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
<!-- ### Payment Method Presence -->
### Payment Method Presence

<!-- To determine if a billable model has a default payment method attached to their account, invoke the `hasDefaultPaymentMethod` method: -->
請求可能なモデルのアカウントにデフォルトの支払い方法が関連付けられているかどうかを確認するには、`hasDefaultPaymentMethod` メソッドを呼び出します。

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

<!-- You may use the `hasPaymentMethod` method to determine if a billable model has at least one payment method attached to their account: -->
`hasPaymentMethod` メソッドを使用して、請求可能なモデルのアカウントに少なくとも 1 つの支払い方法が関連付けられているかどうかを確認できます。

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```

<!-- This method will determine if the billable model has any payment method at all. To determine if a payment method of a specific type exists for the model, you may pass the `type` as an argument to the method: -->
このメソッドは、請求可能なモデルに支払い方法があるかどうかを判断します。モデルに特定のタイプの支払い方法が存在するかどうかを確認するには、メソッドの引数として `type` を渡すことができます。

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
<!-- ### Updating the Default Payment Method -->
### Updating the Default Payment Method

<!-- The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method: -->
`updateDefaultPaymentMethod` メソッドは、顧客のデフォルトの支払い方法情報を更新するために使用できます。このメソッドは、Stripe 支払い方法識別子を受け入れ、新しい支払い方法をデフォルトの請求支払い方法として割り当てます。

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

<!-- To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method: -->
デフォルトの支払い方法情報を Stripe の顧客のデフォルトの支払い方法情報と同期するには、`updateDefaultPaymentMethodFromStripe` メソッドを使用できます。

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 顧客のデフォルトの支払い方法は、請求書発行と新しいサブスクリプションの作成にのみ使用できます。 Stripe によって課された制限により、単一のチャージには使用できない場合があります。

<a name="adding-payment-methods"></a>
<!-- ### Adding Payment Methods -->
### Adding Payment Methods

<!-- To add a new payment method, you may call the `addPaymentMethod` method on the billable model, passing the payment method identifier: -->
新しい支払い方法を追加するには、支払い方法識別子を渡して、請求可能モデルで `addPaymentMethod` メソッドを呼び出します。

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 支払い方法識別子の取得方法については、[payment method storage documentation](#storing-payment-methods) をご覧ください。

<a name="deleting-payment-methods"></a>
<!-- ### Deleting Payment Methods -->
### Deleting Payment Methods

<!-- To delete a payment method, you may call the `delete` method on the `Laravel\Cashier\PaymentMethod` instance you wish to delete: -->
支払い方法を削除するには、削除する `Laravel\Cashier\PaymentMethod` インスタンスで `delete` メソッドを呼び出します。

```php
$paymentMethod->delete();
```

<!-- The `deletePaymentMethod` method will delete a specific payment method from the billable model: -->
`deletePaymentMethod` メソッドは、請求可能なモデルから特定の支払い方法を削除します。

```php
$user->deletePaymentMethod('pm_visa');
```

<!-- The `deletePaymentMethods` method will delete all of the payment method information for the billable model: -->
`deletePaymentMethods` メソッドは、請求可能なモデルのすべての支払い方法情報を削除します。

```php
$user->deletePaymentMethods();
```

<!-- By default, this method will delete payment methods of every type. To delete payment methods of a specific type you can pass the `type` as an argument to the method: -->
デフォルトでは、このメソッドはあらゆる種類の支払い方法を削除します。特定のタイプの支払い方法を削除するには、メソッドの引数として `type` を渡すことができます。

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> ユーザーがアクティブなサブスクリプションを持っている場合、アプリケーションではユーザーがデフォルトの支払い方法を削除できないようにする必要があります。

<a name="subscriptions"></a>
<!-- ## Subscriptions -->
## Subscriptions

<!-- Subscriptions provide a way to set up recurring payments for your customers. Stripe subscriptions managed by Cashier provide support for multiple subscription prices, subscription quantities, trials, and more. -->
サブスクリプションは、顧客に定期的な支払いを設定する方法を提供します。 Cashier によって管理される Stripe サブスクリプションは、複数のサブスクリプション価格、サブスクリプション数量、トライアルなどのサポートを提供します。

<a name="creating-subscriptions"></a>
<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription: -->
サブスクリプションを作成するには、まず課金対象モデルのインスタンスを取得します。これは通常、`App\Models\User` のインスタンスになります。モデル インスタンスを取得したら、`newSubscription` メソッドを使用してモデルのサブスクリプションを作成できます。

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
`newSubscription` メソッドに渡される最初の引数は、サブスクリプションの内部タイプである必要があります。アプリケーションが単一のサブスクリプションのみを提供する場合は、これを `default` または `primary` と呼びます。このサブスクリプション タイプはアプリケーション内部でのみ使用され、ユーザーに表示されることを目的としていません。また、スペースを含めることはできません。また、サブスクリプションの作成後に変更しないでください。 2 番目の引数は、ユーザーが購読している特定の価格です。この値は、Stripe の価格の識別子に対応する必要があります。

<!-- The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information. -->
[a Stripe payment method identifier](#storing-payment-methods) または Stripe `PaymentMethod` オブジェクトを受け入れる `create` メソッドは、サブスクリプションを開始するだけでなく、課金対象モデルの Stripe 顧客 ID およびその他の関連課金情報でデータベースを更新します。

> [!WARNING]
> 支払い方法識別子を `create` サブスクリプション メソッドに直接渡すと、その識別子がユーザーの保存された支払い方法に自動的に追加されます。

<a name="collecting-recurring-payments-via-invoice-emails"></a>
<!-- #### Collecting Recurring Payments via Invoice Emails -->
#### Collecting Recurring Payments via Invoice Emails

<!-- Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices: -->
顧客の定期支払いを自動的に収集する代わりに、定期支払いの期限が来るたびに顧客に請求書を電子メールで送信するように Stripe に指示できます。その後、顧客は請求書を受け取ったら手動で支払うことができます。請求書を通じて定期的な支払いを回収する場合、顧客は前もって支払い方法を指定する必要はありません。

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

<!-- The amount of time a customer has to pay their invoice before their subscription is canceled is determined by the `days_until_due` option. By default, this is 30 days; however, you may provide a specific value for this option if you wish: -->
サブスクリプションがキャンセルされるまでに顧客が請求書を支払わなければならない期間は、`days_until_due` オプションによって決まります。デフォルトでは、これは 30 日です。ただし、必要に応じて、このオプションに特定の値を指定できます。

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
<!-- #### Quantities -->
#### Quantities

<!-- If you would like to set a specific [quantity](https://stripe.com/docs/billing/subscriptions/quantities) for the price when creating the subscription, you should invoke the `quantity` method on the subscription builder before creating the subscription: -->
サブスクリプションの作成時に価格に特定の [quantity](https://stripe.com/docs/billing/subscriptions/quantities) を設定したい場合は、サブスクリプションを作成する前にサブスクリプション ビルダで `quantity` メソッドを呼び出す必要があります。

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional [customer](https://stripe.com/docs/api/customers/create) or [subscription](https://stripe.com/docs/api/subscriptions/create) options supported by Stripe, you may do so by passing them as the second and third arguments to the `create` method: -->
Stripe でサポートされている追加の [customer](https://stripe.com/docs/api/customers/create) または [subscription](https://stripe.com/docs/api/subscriptions/create) オプションを指定したい場合は、それらを `create` メソッドの 2 番目と 3 番目の引数として渡すことで指定できます。

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
サブスクリプションの作成時にクーポンを適用したい場合は、`withCoupon` メソッドを使用できます。

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

<!-- Or, if you would like to apply a [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes), you may use the `withPromotionCode` method: -->
または、[Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes) を適用したい場合は、`withPromotionCode` メソッドを使用できます。

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

<!-- The given promotion code ID should be the Stripe API ID assigned to the promotion code and not the customer facing promotion code. If you need to find a promotion code ID based on a given customer facing promotion code, you may use the `findPromotionCode` method: -->
指定されたプロモーション コード ID は、顧客向けのプロモーション コードではなく、プロモーション コードに割り当てられた Stripe API ID である必要があります。特定の顧客向けプロモーション コードに基づいてプロモーション コード ID を検索する必要がある場合は、`findPromotionCode` メソッドを使用できます。

```php
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

<!-- In the example above, the returned `$promotionCode` object is an instance of `Laravel\Cashier\PromotionCode`. This class decorates an underlying `Stripe\PromotionCode` object. You can retrieve the coupon related to the promotion code by invoking the `coupon` method: -->
上の例では、返される `$promotionCode` オブジェクトは `Laravel\Cashier\PromotionCode` のインスタンスです。このクラスは、基礎となる `Stripe\PromotionCode` オブジェクトを装飾します。 `coupon` メソッドを呼び出して、プロモーション コードに関連するクーポンを取得できます。

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

<!-- The coupon instance allows you to determine the discount amount and whether the coupon represents a fixed discount or percentage based discount: -->
クーポン インスタンスを使用すると、割引額と、クーポンが固定割引を表すかパーセントベースの割引を表すかを決定できます。

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

<!-- You can also retrieve the discounts that are currently applied to a customer or subscription: -->
顧客またはサブスクリプションに現在適用されている割引を取得することもできます。

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

<!-- The returned `Laravel\Cashier\Discount` instances decorate an underlying `Stripe\Discount` object instance. You may retrieve the coupon related to this discount by invoking the `coupon` method: -->
返された `Laravel\Cashier\Discount` インスタンスは、基になる `Stripe\Discount` オブジェクト インスタンスを装飾します。 `coupon` メソッドを呼び出して、この割引に関連するクーポンを取得できます。

```php
$coupon = $subscription->discount()->coupon();
```

<!-- If you would like to apply a new coupon or promotion code to a customer or subscription, you may do so via the `applyCoupon` or `applyPromotionCode` methods: -->
新しいクーポンまたはプロモーション コードを顧客またはサブスクリプションに適用したい場合は、`applyCoupon` または `applyPromotionCode` メソッドを使用して適用できます。

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

<!-- Remember, you should use the Stripe API ID assigned to the promotion code and not the customer facing promotion code. Only one coupon or promotion code can be applied to a customer or subscription at a given time. -->
顧客向けのプロモーション コードではなく、プロモーション コードに割り当てられた Stripe API ID を使用する必要があることに注意してください。特定の時点で顧客またはサブスクリプションに適用できるクーポンまたはプロモーション コードは 1 つだけです。

<!-- For more info on this subject, please consult the Stripe documentation regarding [coupons](https://stripe.com/docs/billing/subscriptions/coupons) and [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes). -->
この件に関する詳細については、[coupons](https://stripe.com/docs/billing/subscriptions/coupons) および [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes) に関する Stripe ドキュメントを参照してください。

<a name="adding-subscriptions"></a>
<!-- #### Adding Subscriptions -->
#### Adding Subscriptions

<!-- If you would like to add a subscription to a customer who already has a default payment method you may invoke the `add` method on the subscription builder: -->
すでにデフォルトの支払い方法を持っている顧客にサブスクリプションを追加したい場合は、サブスクリプション ビルダで `add` メソッドを呼び出すことができます。

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
<!-- #### Creating Subscriptions From the Stripe Dashboard -->
#### Creating Subscriptions From the Stripe Dashboard

<!-- You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a type of `default`. To customize the subscription type that is assigned to dashboard created subscriptions, [define webhook event handlers](#defining-webhook-event-handlers). -->
Stripe ダッシュボード自体からサブスクリプションを作成することもできます。これを行うと、Cashier は新しく追加されたサブスクリプションを同期し、それらに `default` のタイプを割り当てます。ダッシュボードで作成されたサブスクリプションに割り当てられるサブスクリプション タイプをカスタマイズするには、[define webhook event handlers](#defining-webhook-event-handlers)。

<!-- In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different types, only one type of subscription may be added through the Stripe dashboard. -->
さらに、Stripe ダッシュボードから作成できるサブスクリプションは 1 種類のみです。アプリケーションが異なるタイプを使用する複数のサブスクリプションを提供している場合、Stripe ダッシュボードから追加できるサブスクリプションのタイプは 1 つだけです。

<!-- Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If a customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database. -->
最後に、アプリケーションによって提供されるサブスクリプションの種類ごとに、アクティブなサブスクリプションを 1 つだけ追加するように常に注意する必要があります。顧客が 2 つの `default` サブスクリプションを持っている場合、両方がアプリケーションのデータベースと同期されるとしても、最後に追加されたサブスクリプションのみが Cashier によって使用されます。

<a name="checking-subscription-status"></a>
<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the type of the subscription as its first argument: -->
顧客がアプリケーションを購読すると、さまざまな便利な方法を使用して顧客の購読ステータスを簡単に確認できます。まず、顧客がアクティブなサブスクリプションを持っている場合、サブスクリプションが現在試用期間内であっても、`subscribed` メソッドは `true` を返します。 `subscribed` メソッドは、最初の引数としてサブスクリプションのタイプを受け入れます。

```php
if ($user->subscribed('default')) {
    // ...
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/12.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` メソッドも [route middleware](/docs/12.x/middleware) の有力な候補となり、ユーザーのサブスクリプション ステータスに基づいてルートとコントローラへのアクセスをフィルタリングできます。

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
ユーザーがまだ試用期間内であるかどうかを確認したい場合は、`onTrial` メソッドを使用できます。このメソッドは、ユーザーがまだ試用期間中であることをユーザーに警告するかどうかを決定するのに役立ちます。

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

<!-- The `subscribedToProduct` method may be used to determine if the user is subscribed to a given product based on a given Stripe product's identifier. In Stripe, products are collections of prices. In this example, we will determine if the user's `default` subscription is actively subscribed to the application's "premium" product. The given Stripe product identifier should correspond to one of your product's identifiers in the Stripe dashboard: -->
`subscribedToProduct` メソッドは、特定の Stripe 製品の識別子に基づいて、ユーザーが特定の製品を購読しているかどうかを判断するために使用できます。 Stripe では、製品は価格の集合です。この例では、ユーザーの `default` サブスクリプションがアプリケーションの「プレミアム」製品にアクティブにサブスクライブされているかどうかを判断します。指定された Stripe 製品 ID は、Stripe ダッシュボード内の製品 ID の 1 つに対応する必要があります。

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

<!-- By passing an array to the `subscribedToProduct` method, you may determine if the user's `default` subscription is actively subscribed to the application's "basic" or "premium" product: -->
配列を `subscribedToProduct` メソッドに渡すことによって、ユーザーの `default` サブスクリプションがアプリケーションの「ベーシック」製品または「プレミアム」製品にアクティブにサブスクライブされているかどうかを判断できます。

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

<!-- The `subscribedToPrice` method may be used to determine if a customer's subscription corresponds to a given price ID: -->
`subscribedToPrice` メソッドは、顧客のサブスクリプションが特定の価格 ID に対応するかどうかを判断するために使用できます。

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
`recurring` メソッドは、ユーザーが現在購読中であり、試用期間中でないかどうかを判断するために使用できます。

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> ユーザーが同じタイプの 2 つのサブスクリプションを持っている場合、`subscription` メソッドによって常に最新のサブスクリプションが返されます。たとえば、ユーザーは `default` タイプのサブスクリプション レコードを 2 つ持っているとします。ただし、サブスクリプションの 1 つは期限切れの古いサブスクリプションであり、もう 1 つは現在のアクティブなサブスクリプションである可能性があります。最新のサブスクリプションは常に返されますが、古いサブスクリプションは履歴レビューのためにデータベースに保存されます。

<a name="cancelled-subscription-status"></a>
<!-- #### Canceled Subscription Status -->
#### Canceled Subscription Status

<!-- To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method: -->
ユーザーがかつてはアクティブなサブスクライバだったが、サブスクリプションをキャンセルしたかどうかを確認するには、`canceled` メソッドを使用できます。

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

<!-- You may also determine if a user has canceled their subscription but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
また、ユーザーがサブスクリプションをキャンセルしたが、サブスクリプションが完全に期限切れになるまでまだ「猶予期間」中であるかどうかを判断することもできます。たとえば、ユーザーが元々 3 月 10 日に期限切れになる予定だったサブスクリプションを 3 月 5 日にキャンセルした場合、ユーザーは 3 月 10 日まで「猶予期間」に入ります。この間も、`subscribed` メソッドは `true` を返すことに注意してください。

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

<!-- To determine if the user has canceled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
ユーザーがサブスクリプションをキャンセルし、「猶予期間」に入っていないかどうかを確認するには、`ended` メソッドを使用できます。

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
<!-- #### Incomplete and Past Due Status -->
#### Incomplete and Past Due Status

<!-- If a subscription requires a secondary payment action after creation the subscription will be marked as `incomplete`. Subscription statuses are stored in the `stripe_status` column of Cashier's `subscriptions` database table. -->
サブスクリプションの作成後に 2 番目の支払いアクションが必要な場合、サブスクリプションは `incomplete` としてマークされます。サブスクリプションのステータスは、Cashier の `subscriptions` データベース テーブルの `stripe_status` 列に保存されます。

<!-- Similarly, if a secondary payment action is required when swapping prices the subscription will be marked as `past_due`. When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Determining if a subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
同様に、価格を交換するときに 2 番目の支払いアクションが必要な場合、サブスクリプションは `past_due` としてマークされます。サブスクリプションがこれらの状態のいずれかにある場合、顧客が支払いを確認するまでアクティブになりません。サブスクリプションに支払いが完了していないかどうかを判断するには、請求可能モデルまたはサブスクリプション インスタンスで `hasIncompletePayment` メソッドを使用します。

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

<!-- When a subscription has an incomplete payment, you should direct the user to Cashier's payment confirmation page, passing the `latestPayment` identifier. You may use the `latestPayment` method available on subscription instance to retrieve this identifier: -->
サブスクリプションの支払いが完了していない場合は、`latestPayment` 識別子を渡して、ユーザーをCashierの支払い確認ページに誘導する必要があります。サブスクリプション インスタンスで利用可能な `latestPayment` メソッドを使用して、この識別子を取得できます。

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

<!-- If you would like the subscription to still be considered active when it's in a `past_due` or `incomplete` state, you may use the `keepPastDueSubscriptionsActive` and `keepIncompleteSubscriptionsActive` methods provided by Cashier. Typically, these methods should be called in the `register` method of your `App\Providers\AppServiceProvider`: -->
サブスクリプションが `past_due` または `incomplete` 状態にあるときにもアクティブであると見なしたい場合は、Cashier が提供する `keepPastDueSubscriptionsActive` および `keepIncompleteSubscriptionsActive` メソッドを使用できます。通常、これらのメソッドは、`App\Providers\AppServiceProvider` の `register` メソッドで呼び出す必要があります。

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
> サブスクリプションが `incomplete` 状態の場合、支払いが確認されるまで変更することはできません。したがって、サブスクリプションが `incomplete` 状態にある場合、`swap` メソッドと `updateQuantity` メソッドは例外をスローします。

<a name="subscription-scopes"></a>
<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
ほとんどのサブスクリプション状態はクエリ スコープとしても使用できるため、特定の状態にあるサブスクリプションについてデータベースを簡単にクエリできます。

```php
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

<!-- A complete list of available scopes is available below: -->
利用可能なスコープの完全なリストは以下で入手できます。

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
顧客がアプリケーションをサブスクライブした後、新しいサブスクリプション価格への変更を希望する場合があります。顧客を新しい価格に切り替えるには、Stripe 価格の識別子を `swap` メソッドに渡します。価格を交換するときは、ユーザーが以前にサブスクリプションをキャンセルした場合にそのサブスクリプションを再アクティブ化したいと考えていると想定されます。指定された価格識別子は、Stripe ダッシュボードで使用可能な Stripe 価格識別子に対応する必要があります。

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

<!-- If the customer is on trial, the trial period will be maintained. Additionally, if a "quantity" exists for the subscription, that quantity will also be maintained. -->
お客様が試用中の場合、試用期間は維持されます。さらに、サブスクリプションに「数量」が存在する場合、その数量も維持されます。

<!-- If you would like to swap prices and cancel any trial period the customer is currently on, you may invoke the `skipTrial` method: -->
価格を交換し、顧客が現在参加している試用期間をキャンセルしたい場合は、`skipTrial` メソッドを呼び出すことができます。

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

<!-- If you would like to swap prices and immediately invoice the customer instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
価格を交換して、次の請求サイクルを待たずにすぐに顧客に請求したい場合は、`swapAndInvoice` メソッドを使用できます。

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
<!-- #### Prorations -->
#### Prorations

<!-- By default, Stripe prorates charges when swapping between prices. The `noProrate` method may be used to update the subscription's price without prorating the charges: -->
デフォルトでは、Stripe は価格を切り替えるときに料金を日割り計算します。 `noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションの価格を更新できます。

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

<!-- For more information on subscription proration, consult the [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations). -->
サブスクリプションの日割り計算の詳細については、[Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations) を参照してください。

> [!WARNING]
> `swapAndInvoice` メソッドの前に `noProrate` メソッドを実行しても、比例配分には影響しません。請求書は必ず発行されます。

<a name="subscription-quantity"></a>
<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. You may use the `incrementQuantity` and `decrementQuantity` methods to easily increment or decrement your subscription quantity: -->
サブスクリプションは「数量」の影響を受ける場合があります。たとえば、プロジェクト管理アプリケーションでは、プロジェクトごとに月額 10 ドルを請求する場合があります。 `incrementQuantity` および `decrementQuantity` メソッドを使用して、サブスクリプション数量を簡単に増減できます。

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
あるいは、`updateQuantity` メソッドを使用して特定の数量を設定することもできます。

```php
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
`noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションの数量を更新できます。

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<!-- For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities). -->
サブスクリプション数量の詳細については、[Stripe documentation](https://stripe.com/docs/subscriptions/quantities) を参照してください。

<a name="quantities-for-subscription-with-multiple-products"></a>
<!-- #### Quantities for Subscriptions With Multiple Products -->
#### Quantities for Subscriptions With Multiple Products

<!-- If your subscription is a [subscription with multiple products](#subscriptions-with-multiple-products), you should pass the ID of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods: -->
サブスクリプションが [subscription with multiple products](#subscriptions-with-multiple-products) の場合は、増分または減分する数量の価格の ID を 2 番目の引数として増分 / 減分メソッドに渡す必要があります。

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
<!-- ### Subscriptions With Multiple Products -->
### Subscriptions With Multiple Products

<!-- [Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products) allow you to assign multiple billing products to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on product for an additional $15 per month. Information for subscriptions with multiple products is stored in Cashier's `subscription_items` database table. -->
[Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products) を使用すると、複数の課金製品を 1 つのサブスクリプションに割り当てることができます。たとえば、基本サブスクリプション価格が月額 10 ドルであるが、月額 15 ドルの追加料金でライブ チャット アドオン製品を提供するカスタマー サービスの「ヘルプデスク」アプリケーションを構築していると想像してください。複数の製品のサブスクリプションの情報は、Cashier の `subscription_items` データベース テーブルに保存されます。

<!-- You may specify multiple products for a given subscription by passing an array of prices as the second argument to the `newSubscription` method: -->
価格の配列を `newSubscription` メソッドの 2 番目の引数として渡すことで、特定のサブスクリプションに複数の製品を指定できます。

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
上の例では、顧客は `default` サブスクリプションに 2 つの価格を設定します。どちらの価格も、それぞれの請求間隔で請求されます。必要に応じて、`quantity` メソッドを使用して、各価格の特定の数量を指定できます。

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

<!-- If you would like to add another price to an existing subscription, you may invoke the subscription's `addPrice` method: -->
既存のサブスクリプションに別の価格を追加したい場合は、サブスクリプションの `addPrice` メソッドを呼び出します。

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

<!-- The example above will add the new price and the customer will be billed for it on their next billing cycle. If you would like to bill the customer immediately you may use the `addPriceAndInvoice` method: -->
上記の例では、新しい価格が追加され、顧客は次の請求サイクルでその料金を請求されます。顧客にすぐに請求したい場合は、`addPriceAndInvoice` メソッドを使用できます。

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

<!-- If you would like to add a price with a specific quantity, you can pass the quantity as the second argument of the `addPrice` or `addPriceAndInvoice` methods: -->
特定の数量を含む価格を追加したい場合は、`addPrice` メソッドまたは `addPriceAndInvoice` メソッドの 2 番目の引数として数量を渡すことができます。

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

<!-- You may remove prices from subscriptions using the `removePrice` method: -->
`removePrice` メソッドを使用して、サブスクリプションから価格を削除できます。

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> サブスクリプションの最後の価格を削除することはできません。代わりに、サブスクリプションをキャンセルするだけです。

<a name="swapping-prices"></a>
<!-- #### Swapping Prices -->
#### Swapping Prices

<!-- You may also change the prices attached to a subscription with multiple products. For example, imagine a customer has a `price_basic` subscription with a `price_chat` add-on product and you want to upgrade the customer from the `price_basic` to the `price_pro` price: -->
複数の製品のサブスクリプションに関連付けられている価格を変更することもできます。たとえば、顧客が `price_chat` アドオン製品を含む `price_basic` サブスクリプションを持っており、顧客を `price_basic` から `price_pro` 価格にアップグレードしたいとします。

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

<!-- When executing the example above, the underlying subscription item with the `price_basic` is deleted and the one with the `price_chat` is preserved. Additionally, a new subscription item for the `price_pro` is created. -->
上記の例を実行すると、`price_basic` を持つ基になるサブスクリプション アイテムが削除され、`price_chat` を持つサブスクリプション アイテムは保持されます。さらに、`price_pro` の新しいサブスクリプション アイテムが作成されます。

<!-- You can also specify subscription item options by passing an array of key / value pairs to the `swap` method. For example, you may need to specify the subscription price quantities: -->
キーと値のペアの配列を `swap` メソッドに渡すことで、サブスクリプション項目オプションを指定することもできます。たとえば、サブスクリプション価格の数量を指定する必要がある場合があります。

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

<!-- If you want to swap a single price on a subscription, you may do so using the `swap` method on the subscription item itself. This approach is particularly useful if you would like to preserve all of the existing metadata on the subscription's other prices: -->
サブスクリプションの単一の価格を交換したい場合は、サブスクリプション項目自体で `swap` メソッドを使用して行うことができます。このアプローチは、サブスクリプションの他の価格に関する既存のメタデータをすべて保持したい場合に特に便利です。

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
デフォルトでは、Stripe は複数の製品のサブスクリプションに価格を追加または削除するときに料金を日割り計算します。日割りなしで価格調整を行いたい場合は、価格操作に `noProrate` メソッドをチェーンする必要があります。

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
<!-- #### Quantities -->
#### Quantities

<!-- If you would like to update quantities on individual subscription prices, you may do so using the [existing quantity methods](#subscription-quantity) by passing the ID of the price as an additional argument to the method: -->
個々のサブスクリプション価格の数量を更新したい場合は、[existing quantity methods](#subscription-quantity) を使用して価格の ID を追加の引数としてメソッドに渡します。

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> サブスクリプションに複数の価格がある場合、`Subscription` モデルの `stripe_price` 属性と `quantity` 属性は `null` になります。個々の価格属性にアクセスするには、`Subscription` モデルで使用可能な `items` 関係を使用する必要があります。

<a name="subscription-items"></a>
<!-- #### Subscription Items -->
#### Subscription Items

<!-- When a subscription has multiple prices, it will have multiple subscription "items" stored in your database's `subscription_items` table. You may access these via the `items` relationship on the subscription: -->
サブスクリプションに複数の価格がある場合、データベースの `subscription_items` テーブルに複数のサブスクリプション「アイテム」が保存されます。これらには、サブスクリプションの `items` 関係を介してアクセスできます。

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

<!-- You can also retrieve a specific price using the `findItemOrFail` method: -->
`findItemOrFail` メソッドを使用して特定の価格を取得することもできます。

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
<!-- ### Multiple Subscriptions -->
### Multiple Subscriptions

<!-- Stripe allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans. -->
Stripe を使用すると、顧客は複数のサブスクリプションを同時に持つことができます。たとえば、水泳のサブスクリプションとウェイトリフティングのサブスクリプションを提供するジムを運営しており、各サブスクリプションの価格が異なる場合があります。もちろん、顧客はどちらかまたは両方のプランに加入できる必要があります。

<!-- When your application creates subscriptions, you may provide the type of the subscription to the `newSubscription` method. The type may be any string that represents the type of subscription the user is initiating: -->
アプリケーションがサブスクリプションを作成するとき、`newSubscription` メソッドにサブスクリプションのタイプを指定できます。タイプには、ユーザーが開始しているサブスクリプションのタイプを表す任意の文字列を指定できます。

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
この例では、顧客に対して毎月の水泳サブスクリプションを開始しました。ただし、後で年間サブスクリプションに切り替えたい場合もあります。顧客のサブスクリプションを調整するときは、`swimming` サブスクリプションの価格を単純に交換できます。

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

<!-- Of course, you may also cancel the subscription entirely: -->
もちろん、サブスクリプションを完全にキャンセルすることもできます。

```php
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
<!-- ### Usage Based Billing -->
### Usage Based Billing

<!-- [Usage based billing](https://stripe.com/docs/billing/subscriptions/metered-billing) allows you to charge customers based on their product usage during a billing cycle. For example, you may charge customers based on the number of text messages or emails they send per month. -->
[Usage based billing](https://stripe.com/docs/billing/subscriptions/metered-billing) を使用すると、請求サイクル中の製品の使用量に基づいて顧客に請求できます。たとえば、顧客が毎月送信するテキスト メッセージや電子メールの数に基づいて顧客に請求できます。

<!-- To start using usage billing, you will first need to create a new product in your Stripe dashboard with a [usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) and a [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter). After creating the meter, store the associated event name and meter ID, which you will need to report and retrieve usage. Then, use the `meteredPrice` method to add the metered price ID to a customer subscription: -->
従量課金の使用を開始するには、まず、[usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) と [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter) を使用して、Stripe ダッシュボードに新しい製品を作成する必要があります。メーターを作成した後、関連するイベント名とメーター ID を保存します。これらは、使用状況をレポートおよび取得するために必要になります。次に、`meteredPrice` メソッドを使用して、従量制価格 ID を顧客のサブスクリプションに追加します。

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
[Stripe Checkout](#checkout) 経由で従量制サブスクリプションを開始することもできます。

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
顧客がアプリケーションを使用すると、正確に請求できるように、その使用状況を Stripe に報告します。計測イベントの使用状況をレポートするには、`Billable` モデルで `reportMeterEvent` メソッドを使用できます。

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

<!-- By default, a "usage quantity" of 1 is added to the billing period. Alternatively, you may pass a specific amount of "usage" to add to the customer's usage for the billing period: -->
デフォルトでは、「使用数量」1 が請求期間に追加されます。あるいは、特定の「使用量」を渡して、請求期間中の顧客の使用量に追加することもできます。

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

<!-- To retrieve a customer's event summary for a meter, you may use a `Billable` instance's `meterEventSummaries` method: -->
メーターの顧客のイベント概要を取得するには、`Billable` インスタンスの `meterEventSummaries` メソッドを使用できます。

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

<!-- Please refer to Stripe's [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object) for more information on meter event summaries. -->
メーターイベントの概要の詳細については、Stripe の [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object) を参照してください。

<!-- To [list all meters](https://docs.stripe.com/api/billing/meter/list), you may use a `Billable` instance's `meters` method: -->
[list all meters](https://docs.stripe.com/api/billing/meter/list) には、`Billable` インスタンスの `meters` メソッドを使用できます。

```php
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>
<!-- ### Subscription Taxes -->
### Subscription Taxes

> [!WARNING]
> 税率を手動で計算する代わりに、[automatically calculate taxes using Stripe Tax](#tax-configuration) を実行できます。

<!-- To specify the tax rates a user pays on a subscription, you should implement the `taxRates` method on your billable model and return an array containing the Stripe tax rate IDs. You can define these tax rates in [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates): -->
ユーザーがサブスクリプションに対して支払う税率を指定するには、請求可能モデルに `taxRates` メソッドを実装し、Stripe 税率 ID を含む配列を返す必要があります。これらの税率は [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates) で定義できます。

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
`taxRates` メソッドを使用すると、顧客ごとに税率を適用できます。これは、複数の国や税率にまたがるユーザー ベースに役立つ場合があります。

<!-- If you're offering subscriptions with multiple products, you may define different tax rates for each price by implementing a `priceTaxRates` method on your billable model: -->
複数の製品のサブスクリプションを提供している場合は、請求対象モデルに `priceTaxRates` メソッドを実装することで、価格ごとに異なる税率を定義できます。

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
> `taxRates` メソッドは、サブスクリプション料金にのみ適用されます。 Cashier を使用して「1 回限り」の請求を行う場合は、その時点で税率を手動で指定する必要があります。

<a name="syncing-tax-rates"></a>
<!-- #### Syncing Tax Rates -->
#### Syncing Tax Rates

<!-- When changing the hard-coded tax rate IDs returned by the `taxRates` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the new `taxRates` values, you should call the `syncTaxRates` method on the user's subscription instance: -->
`taxRates` メソッドによって返されるハードコードされた税率 ID を変更する場合、ユーザーの既存のサブスクリプションの税金設定は同じままになります。既存のサブスクリプションの税額を新しい `taxRates` 値で更新する場合は、ユーザーのサブスクリプション インスタンスで `syncTaxRates` メソッドを呼び出す必要があります。

```php
$user->subscription('default')->syncTaxRates();
```

<!-- This will also sync any item tax rates for a subscription with multiple products. If your application is offering subscriptions with multiple products, you should ensure that your billable model implements the `priceTaxRates` method [discussed above](#subscription-taxes). -->
これにより、複数の商品のサブスクリプションの商品税率も同期されます。アプリケーションが複数の製品のサブスクリプションを提供している場合は、課金対象モデルが `priceTaxRates` メソッド [discussed above](#subscription-taxes) を実装していることを確認する必要があります。

<a name="tax-exemption"></a>
<!-- #### Tax Exemption -->
#### Tax Exemption

<!-- Cashier also offers the `isNotTaxExempt`, `isTaxExempt`, and `reverseChargeApplies` methods to determine if the customer is tax exempt. These methods will call the Stripe API to determine a customer's tax exemption status: -->
Cashier は、顧客が非課税かどうかを判断するための `isNotTaxExempt`、`isTaxExempt`、および `reverseChargeApplies` メソッドも提供します。これらのメソッドは、Stripe API を呼び出して、顧客の免税ステータスを判断します。

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]
> これらのメソッドは、任意の `Laravel\Cashier\Invoice` オブジェクトでも使用できます。ただし、`Invoice` オブジェクトで呼び出された場合、メソッドは請求書の作成時の免除ステータスを決定します。

<a name="subscription-anchor-date"></a>
<!-- ### Subscription Anchor Date -->
### Subscription Anchor Date

<!-- By default, the billing cycle anchor is the date the subscription was created or, if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method: -->
デフォルトでは、請求サイクルアンカーはサブスクリプションが作成された日付、または試用期間が使用されている場合は試用が終了する日付です。請求アンカー日を変更したい場合は、`anchorBillingCycleOn` メソッドを使用できます。

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
サブスクリプションの請求サイクルの管理の詳細については、[Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle) を参照してください。

<a name="cancelling-subscriptions"></a>
<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
サブスクリプションをキャンセルするには、ユーザーのサブスクリプションで `cancel` メソッドを呼び出します。

```php
$user->subscription('default')->cancel();
```

<!-- When a subscription is canceled, Cashier will automatically set the `ends_at` column in your `subscriptions` database table. This column is used to know when the `subscribed` method should begin returning `false`. -->
サブスクリプションがキャンセルされると、Cashier は `subscriptions` データベース テーブルに `ends_at` 列を自動的に設定します。この列は、`subscribed` メソッドが `false` を返し始める時期を知るために使用されます。

<!-- For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
たとえば、顧客が 3 月 1 日にサブスクリプションをキャンセルしたが、そのサブスクリプションが 3 月 5 日まで終了する予定ではなかった場合、`subscribed` メソッドは 3 月 5 日まで `true` を返し続けます。これは、ユーザーが通常、請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているために行われます。

<!-- You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
`onGracePeriod` メソッドを使用して、ユーザーがサブスクリプションをキャンセルしたがまだ「猶予期間」中であるかどうかを確認できます。

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

<!-- If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription: -->
サブスクリプションをすぐにキャンセルしたい場合は、ユーザーのサブスクリプションで `cancelNow` メソッドを呼び出します。

```php
$user->subscription('default')->cancelNow();
```

<!-- If you wish to cancel a subscription immediately and invoice any remaining un-invoiced metered usage or new / pending proration invoice items, call the `cancelNowAndInvoice` method on the user's subscription: -->
サブスクリプションをすぐにキャンセルし、残りの未請求の従量制使用量または新規/保留中の日割り請求書アイテムを請求したい場合は、ユーザーのサブスクリプションで `cancelNowAndInvoice` メソッドを呼び出します。

```php
$user->subscription('default')->cancelNowAndInvoice();
```

<!-- You may also choose to cancel the subscription at a specific moment in time: -->
特定の時点でサブスクリプションをキャンセルすることもできます。

```php
$user->subscription('default')->cancelAt(
    now()->plus(days: 10)
);
```

<!-- Finally, you should always cancel user subscriptions before deleting the associated user model: -->
最後に、関連するユーザー モデルを削除する前に、常にユーザー サブスクリプションをキャンセルする必要があります。

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
<!-- ### Resuming Subscriptions -->
### Resuming Subscriptions

<!-- If a customer has canceled their subscription and you wish to resume it, you may invoke the `resume` method on the subscription. The customer must still be within their "grace period" in order to resume a subscription: -->
顧客がサブスクリプションをキャンセルし、それを再開したい場合は、サブスクリプションで `resume` メソッドを呼び出すことができます。顧客がサブスクリプションを再開するには、「猶予期間」内である必要があります。

```php
$user->subscription('default')->resume();
```

<!-- If the customer cancels a subscription and then resumes that subscription before the subscription has fully expired the customer will not be billed immediately. Instead, their subscription will be re-activated and they will be billed on the original billing cycle. -->
顧客がサブスクリプションをキャンセルし、サブスクリプションの有効期限が完全に切れる前にそのサブスクリプションを再開した場合、顧客にはすぐには請求されません。代わりに、サブスクリプションが再度アクティブ化され、元の請求サイクルで請求されます。

<a name="subscription-trials"></a>
<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>
<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions: -->
支払い方法情報を事前に収集しながら顧客に試用期間を提供したい場合は、サブスクリプションの作成時に `trialDays` メソッドを使用する必要があります。

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
このメソッドは、データベース内のサブスクリプション レコードに試用期間の終了日を設定し、この日以降になるまで顧客への請求を開始しないように Stripe に指示します。 `trialDays` メソッドを使用すると、Cashier は Stripe の価格に設定されたデフォルトの試用期間を上書きします。

> [!WARNING]
> 試用期間の終了日までに顧客のサブスクリプションがキャンセルされなかった場合、試用期間が終了するとすぐに料金が請求されるため、ユーザーに試用期間の終了日を必ず通知する必要があります。

<!-- The `trialUntil` method allows you to provide a `DateTime` instance that specifies when the trial period should end: -->
`trialUntil` メソッドを使用すると、試用期間の終了時期を指定する `DateTime` インスタンスを提供できます。

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->plus(days: 10))
    ->create($paymentMethod);
```

<!-- You may determine if a user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
ユーザー インスタンスの `onTrial` メソッドまたはサブスクリプション インスタンスの `onTrial` メソッドを使用して、ユーザーが試用期間内かどうかを判断できます。以下の 2 つの例は同等です。

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

<!-- You may use the `endTrial` method to immediately end a subscription trial: -->
`endTrial` メソッドを使用して、サブスクリプションのトライアルをすぐに終了できます。

```php
$user->subscription('default')->endTrial();
```

<!-- To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods: -->
既存の試用版の有効期限が切れているかどうかを確認するには、`hasExpiredTrial` メソッドを使用できます。

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
Stripe ダッシュボードで価格を受け取るトライアル日数を定義するか、Cashier を使用して常に明示的に渡すかを選択できます。 Stripe で価格の試用期間を定義することを選択した場合は、明示的に `skipTrial()` メソッドを呼び出さない限り、過去にサブスクリプションを持っていた顧客の新規サブスクリプションを含む、新しいサブスクリプションには常に試用期間が設定されることに注意する必要があります。

<a name="without-payment-method-up-front"></a>
<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration: -->
ユーザーの支払い方法情報を事前に収集せずに試用期間を提供したい場合は、ユーザー レコードの `trial_ends_at` 列を希望する試用終了日に設定できます。これは通常、ユーザー登録時に行われます。

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->plus(days: 10),
]);
```

> [!WARNING]
> 課金対象モデルのクラス定義内の `trial_ends_at` 属性に [date cast](/docs/12.x/eloquent-mutators#date-casting) を必ず追加してください。

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the billable model instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
既存のサブスクリプションに関連付けられていないため、Cashier はこのタイプのトライアルを「一般トライアル」と呼びます。現在の日付が `trial_ends_at` の値を超えていない場合、請求可能モデル インスタンスの `onTrial` メソッドは `true` を返します。

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
ユーザーの実際のサブスクリプションを作成する準備ができたら、通常どおり `newSubscription` メソッドを使用できます。

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription type parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
ユーザーの試用終了日を取得するには、`trialEndsAt` メソッドを使用できます。このメソッドは、ユーザーが試用中の場合は Carbon date インスタンスを返し、試用中でない場合は `null` を返します。デフォルト以外の特定のサブスクリプションの試用終了日を取得したい場合は、オプションのサブスクリプション タイプ パラメーターを渡すこともできます。

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not yet created an actual subscription: -->
ユーザーが「一般的な」試用期間内であり、実際のサブスクリプションをまだ作成していないことを具体的に知りたい場合は、`onGenericTrial` メソッドを使用することもできます。

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>
<!-- ### Extending Trials -->
### Extending Trials

<!-- The `extendTrial` method allows you to extend the trial period of a subscription after the subscription has been created. If the trial has already expired and the customer is already being billed for the subscription, you can still offer them an extended trial. The time spent within the trial period will be deducted from the customer's next invoice: -->
`extendTrial` メソッドを使用すると、サブスクリプションの作成後にサブスクリプションの試用期間を延長できます。トライアルの有効期限がすでに切れており、顧客にサブスクリプションの料金がすでに請求されている場合でも、延長トライアルを提供できます。試用期間内に費やした時間は、お客様の次回の請求書から差し引かれます。

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
> [the Stripe CLI](https://stripe.com/docs/stripe-cli) を使用すると、ローカル開発中に Webhook をテストできます。

<!-- Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Stripe は、Webhook 経由でさまざまなイベントをアプリケーションに通知できます。デフォルトでは、Cashier の Webhook コントローラを指すルートは、Cashier サービスプロバイダによって自動的に登録されます。このコントローラは、受信したすべての Webhook リクエストを処理します。

<!-- By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like. -->
デフォルトでは、Cashier Webhook コントローラは、失敗した請求 (Stripe 設定で定義されている) が多すぎるサブスクリプションのキャンセル、顧客の更新、顧客の削除、サブスクリプションの更新、支払い方法の変更を自動的に処理します。ただし、すぐにわかりますが、このコントローラを拡張して、任意の Stripe Webhook イベントを処理できます。

<!-- To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are: -->
アプリケーションが Stripe Webhook を処理できるようにするには、Stripe コントロール パネルで Webhook URL を構成してください。デフォルトでは、Cashier の Webhook コントローラは `/stripe/webhook` URL パスに応答します。 Stripe コントロール パネルで有効にする必要があるすべての Webhook の完全なリストは次のとおりです。

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
便宜上、Cashier には `cashier:webhook` Artisan コマンドが含まれています。このコマンドは、Cashier が必要とするすべてのイベントをリッスンする Webhook を Stripe に作成します。

```shell
php artisan cashier:webhook
```

<!-- By default, the created webhook will point to the URL defined by the `APP_URL` environment variable and the `cashier.webhook` route that is included with Cashier. You may provide the `--url` option when invoking the command if you would like to use a different URL: -->
デフォルトでは、作成された Webhook は、`APP_URL` 環境変数によって定義された URL と、Cashier に含まれる `cashier.webhook` ルートを指します。別の URL を使用したい場合は、コマンドを呼び出すときに `--url` オプションを指定できます。

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

<!-- The webhook that is created will use the Stripe API version that your version of Cashier is compatible with. If you would like to use a different Stripe version, you may provide the `--api-version` option: -->
作成される Webhook は、Cashier のバージョンと互換性のある Stripe API バージョンを使用します。別の Stripe バージョンを使用したい場合は、`--api-version` オプションを指定できます。

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

<!-- After creation, the webhook will be immediately active. If you wish to create the webhook but have it disabled until you're ready, you may provide the `--disabled` option when invoking the command: -->
作成後、Webhook はすぐにアクティブになります。 Webhook を作成したいが、準備が完了するまで無効にしておく場合は、コマンドを呼び出すときに `--disabled` オプションを指定できます。

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Cashier に含まれる [webhook signature verification](#verifying-webhook-signatures) ミドルウェアを使用して、受信した Stripe Webhook リクエストを必ず保護してください。

<a name="webhooks-csrf-protection"></a>
<!-- #### Webhooks and CSRF Protection -->
#### Webhooks and CSRF Protection

<!-- Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/12.x/csrf), you should ensure that Laravel does not attempt to validate the CSRF token for incoming Stripe webhooks. To accomplish this, you should exclude `stripe/*` from CSRF protection in your application's `bootstrap/app.php` file: -->
Stripe Webhook は Laravel の [CSRF protection](/docs/12.x/csrf) をバイパスする必要があるため、Laravel が受信 Stripe Webhook の CSRF トークンを検証しないようにする必要があります。これを実現するには、アプリケーションの `bootstrap/app.php` ファイルで CSRF 保護から `stripe/*` を除外する必要があります。

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
Cashier は、失敗した請求やその他の一般的な Stripe Webhook イベントによるサブスクリプションのキャンセルを自動的に処理します。ただし、追加の Webhook イベントを処理したい場合は、Cashier によって送出される次のイベントをリッスンすることで処理できます。

<!--
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`
-->
- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

<!-- Both events contain the full payload of the Stripe webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/12.x/events#defining-listeners) that will handle the event: -->
どちらのイベントにも、Stripe Webhook の完全なペイロードが含まれています。たとえば、`invoice.payment_succeeded` Webhook を処理したい場合は、イベントを処理する [listener](/docs/12.x/events#defining-listeners) を登録できます。

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
Webhook を保護するには、[Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures) を使用できます。便宜上、Cashier には、受信した Stripe Webhook リクエストが有効であることを検証するミドルウェアが自動的に組み込まれています。

<!-- To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is set in your application's `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard. -->
Webhook 検証を有効にするには、アプリケーションの `.env` ファイルに `STRIPE_WEBHOOK_SECRET` 環境変数が設定されていることを確認してください。 Webhook `secret` は、Stripe アカウントのダッシュボードから取得できます。

<a name="single-charges"></a>
<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>
<!-- ### Simple Charge -->
### Simple Charge

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance. You will need to [provide a payment method identifier](#payment-methods-for-single-charges) as the second argument to the `charge` method: -->
顧客に対して 1 回限りの請求を行う場合は、請求可能モデル インスタンスで `charge` メソッドを使用できます。 `charge` メソッドの 2 番目の引数として [provide a payment method identifier](#payment-methods-for-single-charges) を指定する必要があります。

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
`charge` メソッドは 3 番目の引数として配列を受け入れ、基になる Stripe チャージ作成に必要なオプションを渡すことができます。料金作成時に利用できるオプションの詳細については、[Stripe documentation](https://stripe.com/docs/api/charges/create) を参照してください。

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

<!-- You may also use the `charge` method without an underlying customer or user. To accomplish this, invoke the `charge` method on a new instance of your application's billable model: -->
基になる顧客またはユーザーなしで `charge` メソッドを使用することもできます。これを実現するには、アプリケーションの課金対象モデルの新しいインスタンスで `charge` メソッドを呼び出します。

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

<!-- The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method: -->
請求が失敗すると、`charge` メソッドは例外をスローします。チャージが成功すると、`Laravel\Cashier\Payment` のインスタンスがメソッドから返されます。

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]
> `charge` メソッドは、アプリケーションで使用される通貨の最小分母で支払い金額を受け入れます。たとえば、顧客が米ドルで支払う場合は、金額をペニー単位で指定する必要があります。

<a name="charge-with-invoice"></a>
<!-- ### Charge With Invoice -->
### Charge With Invoice

<!-- Sometimes you may need to make a one-time charge and offer a PDF invoice to your customer. The `invoicePrice` method lets you do just that. For example, let's invoice a customer for five new shirts: -->
場合によっては、1 回限りの請求を行って、PDF の請求書を顧客に提供する必要がある場合があります。 `invoicePrice` メソッドを使用すると、まさにそれが可能になります。たとえば、顧客に新しいシャツ 5 枚の請求書を発行してみましょう。

```php
$user->invoicePrice('price_tshirt', 5);
```

<!-- The invoice will be immediately charged against the user's default payment method. The `invoicePrice` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array which should contain the billing options for the invoice itself: -->
請求書は、ユーザーのデフォルトの支払い方法に対して直ちに請求されます。 `invoicePrice` メソッドは、3 番目の引数として配列も受け入れます。この配列には、請求書アイテムの請求オプションが含まれています。このメソッドで受け入れられる 4 番目の引数も、請求書自体の請求オプションを含む配列です。

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
`invoicePrice` と同様に、`tabPrice` メソッドを使用して、顧客の「タブ」にアイテムを追加して顧客に請求することにより、複数のアイテム (請求書ごとに最大 250 アイテム) に対する 1 回限りの請求を作成できます。たとえば、顧客にシャツ 5 枚とマグカップ 2 個の請求を行うとします。

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

<!-- Alternatively, you may use the `invoiceFor` method to make a "one-off" charge against the customer's default payment method: -->
あるいは、`invoiceFor` メソッドを使用して、顧客のデフォルトの支払い方法に対して「1 回限り」の請求を行うこともできます。

```php
$user->invoiceFor('One Time Fee', 500);
```

<!-- Although the `invoiceFor` method is available for you to use, it is recommended that you use the `invoicePrice` and `tabPrice` methods with pre-defined prices. By doing so, you will have access to better analytics and data within your Stripe dashboard regarding your sales on a per-product basis. -->
`invoiceFor` メソッドを使用することもできますが、事前定義された価格で `invoicePrice` および `tabPrice` メソッドを使用することをお勧めします。そうすることで、Stripe ダッシュボード内で製品ごとの売上に関するより優れた分析とデータにアクセスできるようになります。

> [!WARNING]
> `invoice`、`invoicePrice`、および `invoiceFor` メソッドは、失敗した請求を再試行する Stripe 請求書を作成します。失敗した請求書を再試行したくない場合は、最初の請求失敗後に Stripe API を使用して請求書を閉じる必要があります。

<a name="creating-payment-intents"></a>
<!-- ### Creating Payment Intents -->
### Creating Payment Intents

<!-- You can create a new Stripe payment intent by invoking the `pay` method on a billable model instance. Calling this method will create a payment intent that is wrapped in a `Laravel\Cashier\Payment` instance: -->
新しい Stripe 支払いインテントを作成するには、請求可能モデル インスタンスで `pay` メソッドを呼び出します。このメソッドを呼び出すと、`Laravel\Cashier\Payment` インスタンスにラップされた支払いインテントが作成されます。

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
支払いインテントを作成した後、ユーザーがブラウザーで支払いを完了できるように、クライアント シークレットをアプリケーションのフロントエンドに返すことができます。 Stripe 支払いインテントを使用した支払いフロー全体の構築の詳細については、[Stripe documentation](https://stripe.com/docs/payments/accept-a-payment?platform=web) を参照してください。

<!-- When using the `pay` method, the default payment methods that are enabled within your Stripe dashboard will be available to the customer. Alternatively, if you only want to allow for some specific payment methods to be used, you may use the `payWith` method: -->
`pay` メソッドを使用する場合、顧客は Stripe ダッシュボード内で有効になっているデフォルトの支払い方法を利用できるようになります。あるいは、特定の支払い方法のみの使用を許可したい場合は、`payWith` メソッドを使用することもできます。

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
> `pay` メソッドと `payWith` メソッドは、アプリケーションで使用される通貨の最小分母で支払い金額を受け入れます。たとえば、顧客が米ドルで支払う場合は、金額をペニー単位で指定する必要があります。

<a name="refunding-charges"></a>
<!-- ### Refunding Charges -->
### Refunding Charges

<!-- If you need to refund a Stripe charge, you may use the `refund` method. This method accepts the Stripe [payment intent ID](#payment-methods-for-single-charges) as its first argument: -->
Stripe 料金を返金する必要がある場合は、`refund` メソッドを使用できます。このメソッドは、最初の引数として Stripe [payment intent ID](#payment-methods-for-single-charges) を受け入れます。

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
`invoices` メソッドを使用すると、請求可能なモデルの請求書の配列を簡単に取得できます。 `invoices` メソッドは、`Laravel\Cashier\Invoice` インスタンスのコレクションを返します。

```php
$invoices = $user->invoices();
```

<!-- If you would like to include pending invoices in the results, you may use the `invoicesIncludingPending` method: -->
結果に保留中の請求書を含めたい場合は、`invoicesIncludingPending` メソッドを使用できます。

```php
$invoices = $user->invoicesIncludingPending();
```

<!-- You may use the `findInvoice` method to retrieve a specific invoice by its ID: -->
`findInvoice` メソッドを使用して、ID で特定の請求書を取得できます。

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
<!-- #### Displaying Invoice Information -->
#### Displaying Invoice Information

<!-- When listing the invoices for the customer, you may use the invoice's methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them: -->
顧客の請求書をリストする場合、請求書のメソッドを使用して、関連する請求書情報を表示できます。たとえば、すべての請求書を表にリストして、ユーザーが請求書を簡単にダウンロードできるようにしたい場合があります。

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
顧客の今後の請求書を取得するには、`upcomingInvoice` メソッドを使用できます。

```php
$invoice = $user->upcomingInvoice();
```

<!-- Similarly, if the customer has multiple subscriptions, you can also retrieve the upcoming invoice for a specific subscription: -->
同様に、顧客が複数のサブスクリプションを持っている場合は、特定のサブスクリプションの今後の請求書を取得することもできます。

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
<!-- ### Previewing Subscription Invoices -->
### Previewing Subscription Invoices

<!-- Using the `previewInvoice` method, you can preview an invoice before making price changes. This will allow you to determine what your customer's invoice will look like when a given price change is made: -->
`previewInvoice` メソッドを使用すると、価格を変更する前に請求書をプレビューできます。これにより、特定の価格変更が行われたときに顧客の請求書がどのようになるかを判断できます。

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

<!-- You may pass an array of prices to the `previewInvoice` method in order to preview invoices with multiple new prices: -->
複数の新しい価格で請求書をプレビューするために、価格の配列を `previewInvoice` メソッドに渡すことができます。

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
<!-- ### Generating Invoice PDFs -->
### Generating Invoice PDFs

<!-- Before generating invoice PDFs, you should use Composer to install the Dompdf library, which is the default invoice renderer for Cashier: -->
請求書 PDF を生成する前に、Composer を使用して、Cashier のデフォルトの請求書レンダラーである Dompdf ライブラリをインストールする必要があります。

```shell
composer require dompdf/dompdf
```

<!-- From within a route or controller, you may use the `downloadInvoice` method to generate a PDF download of a given invoice. This method will automatically generate the proper HTTP response needed to download the invoice: -->
ルートまたはコントローラ内から、`downloadInvoice` メソッドを使用して、特定の請求書の PDF ダウンロードを生成できます。このメソッドは、請求書のダウンロードに必要な適切な HTTP 応答を自動的に生成します。

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

<!-- By default, all data on the invoice is derived from the customer and invoice data stored in Stripe. The filename is based on your `app.name` config value. However, you can customize some of this data by providing an array as the second argument to the `downloadInvoice` method. This array allows you to customize information such as your company and product details: -->
デフォルトでは、請求書のすべてのデータは、Stripe に保存されている顧客データと請求書のデータから取得されます。ファイル名は、`app.name` 構成値に基づいています。ただし、`downloadInvoice` メソッドの 2 番目の引数として配列を指定することで、このデータの一部をカスタマイズできます。この配列を使用すると、会社や製品の詳細などの情報をカスタマイズできます。

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
`downloadInvoice` メソッドでは、3 番目の引数を使用してカスタム ファイル名を指定することもできます。このファイル名には、自動的に `.pdf` という接尾辞が付けられます。

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
<!-- #### Custom Invoice Renderer -->
#### Custom Invoice Renderer

<!-- Cashier also makes it possible to use a custom invoice renderer. By default, Cashier uses the `DompdfInvoiceRenderer` implementation, which utilizes the [dompdf](https://github.com/dompdf/dompdf) PHP library to generate Cashier's invoices. However, you may use any renderer you wish by implementing the `Laravel\Cashier\Contracts\InvoiceRenderer` interface. For example, you may wish to render an invoice PDF using an API call to a third-party PDF rendering service: -->
Cashier では、カスタムの請求書レンダラーを使用することもできます。デフォルトでは、Cashier は `DompdfInvoiceRenderer` 実装を使用します。これは、[dompdf](https://github.com/dompdf/dompdf) PHP ライブラリを利用して Cashier の請求書を生成します。ただし、`Laravel\Cashier\Contracts\InvoiceRenderer` インターフェイスを実装することで、任意のレンダラーを使用できます。たとえば、サードパーティの PDF レンダリング サービスへの API 呼び出しを使用して、請求書の PDF をレンダリングしたい場合があります。

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
請求書レンダラー コントラクトを実装したら、アプリケーションの `config/cashier.php` 構成ファイル内の `cashier.invoices.renderer` 構成値を更新する必要があります。この構成値は、カスタム レンダラー実装のクラス名に設定する必要があります。

<a name="checkout"></a>
<!-- ## Checkout -->
## Checkout

<!-- Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page. -->
Cashier Stripe は、[Stripe Checkout](https://stripe.com/payments/checkout) のサポートも提供します。 Stripe Checkout は、事前に構築されたホストされた支払いページを提供することで、支払いを受け入れるためのカスタム ページを実装する手間を省きます。

<!-- The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout). -->
次のドキュメントには、Cashier で Stripe Checkout の使用を開始する方法に関する情報が含まれています。 Stripe Checkout について詳しく知りたい場合は、[Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout) を確認することも検討してください。

<a name="product-checkouts"></a>
<!-- ### Product Checkouts -->
### Product Checkouts

<!-- You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID: -->
課金対象モデルで `checkout` メソッドを使用して、Stripe ダッシュボード内で作成された既存の製品のチェックアウトを実行できます。 `checkout` メソッドは、新しい Stripe Checkout セッションを開始します。デフォルトでは、Stripe Price ID を渡す必要があります。

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

<!-- If needed, you may also specify a product quantity: -->
必要に応じて、製品の数量を指定することもできます。

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

<!-- When a customer visits this route they will be redirected to Stripe's Checkout page. By default, when a user successfully completes or cancels a purchase they will be redirected to your `home` route location, but you may specify custom callback URLs using the `success_url` and `cancel_url` options: -->
顧客がこのルートを訪問すると、Stripe のチェックアウト ページにリダイレクトされます。デフォルトでは、ユーザーが購入を正常に完了またはキャンセルすると、`home` ルートの場所にリダイレクトされますが、`success_url` および `cancel_url` オプションを使用してカスタム コールバック URL を指定することもできます。

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
`success_url` チェックアウト オプションを定義するときに、URL を呼び出すときにチェックアウト セッション ID をクエリ文字列パラメータとして追加するように Stripe に指示できます。これを行うには、リテラル文字列 `{CHECKOUT_SESSION_ID}` を `success_url` クエリ文字列に追加します。 Stripe は、このプレースホルダーを実際のチェックアウト セッション ID に置き換えます。

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
デフォルトでは、Stripe Checkout は [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes) を許可しません。幸いなことに、チェックアウト ページでこれらを有効にする簡単な方法があります。これを行うには、`allowPromotionCodes` メソッドを呼び出します。

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
Stripe ダッシュボードで作成されていないアドホック製品に対して簡単な課金を実行することもできます。これを行うには、請求可能なモデルで `checkoutCharge` メソッドを使用し、請求可能な金額、製品名、およびオプションの数量を渡します。顧客がこのルートにアクセスすると、Stripe のチェックアウト ページにリダイレクトされます。

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` メソッドを使用すると、Stripe は常に Stripe ダッシュボードに新しい製品と価格を作成します。したがって、Stripe ダッシュボードで事前に製品を作成し、代わりに `checkout` メソッドを使用することをお勧めします。

<a name="subscription-checkouts"></a>
<!-- ### Subscription Checkouts -->
### Subscription Checkouts

> [!WARNING]
> サブスクリプションに Stripe Checkout を使用するには、Stripe ダッシュボードで `customer.subscription.created` Webhook を有効にする必要があります。この Webhook は、データベースにサブスクリプション レコードを作成し、関連するすべてのサブスクリプション アイテムを保存します。

<!-- You may also use Stripe Checkout to initiate subscriptions. After defining your subscription with Cashier's subscription builder methods, you may call the `checkout `method. When a customer visits this route they will be redirected to Stripe's Checkout page: -->
Stripe Checkout を使用してサブスクリプションを開始することもできます。 Cashier のサブスクリプション ビルダ メソッドを使用してサブスクリプションを定義した後、`checkout ` メソッドを呼び出すことができます。顧客がこのルートにアクセスすると、Stripe のチェックアウト ページにリダイレクトされます。

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

<!-- Just as with product checkouts, you may customize the success and cancellation URLs: -->
製品のチェックアウトと同様に、成功 URL とキャンセル URL をカスタマイズできます。

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
もちろん、サブスクリプションのチェックアウト用のプロモーション コードを有効にすることもできます。

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
> 残念ながら、Stripe Checkout は、サブスクリプションの開始時にすべてのサブスクリプション請求オプションをサポートしているわけではありません。サブスクリプションビルダでの `anchorBillingCycleOn` メソッドの使用、比例配分動作の設定、または支払い動作の設定は、Stripe Checkout セッション中には影響しません。使用可能なパラメータを確認するには、[the Stripe Checkout Session API documentation](https://stripe.com/docs/api/checkout/sessions/create) を参照してください。

<a name="stripe-checkout-trial-periods"></a>
<!-- #### Stripe Checkout and Trial Periods -->
#### Stripe Checkout and Trial Periods

<!-- Of course, you can define a trial period when building a subscription that will be completed using Stripe Checkout: -->
もちろん、Stripe Checkout を使用して完了するサブスクリプションを構築するときに、試用期間を定義できます。

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<!-- However, the trial period must be at least 48 hours, which is the minimum amount of trial time supported by Stripe Checkout. -->
ただし、試用期間は少なくとも 48 時間である必要があります。これは、Stripe Checkout でサポートされる最小試用時間です。

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
<!-- #### Subscriptions and Webhooks -->
#### Subscriptions and Webhooks

<!-- Remember, Stripe and Cashier update subscription statuses via webhooks, so there's a possibility a subscription might not yet be active when the customer returns to the application after entering their payment information. To handle this scenario, you may wish to display a message informing the user that their payment or subscription is pending. -->
Stripe と Cashier は Webhook 経由でサブスクリプションのステータスを更新するため、顧客が支払い情報を入力した後にアプリケーションに戻った時点では、サブスクリプションがまだ有効になっていない可能性があることに注意してください。このシナリオに対処するには、支払いまたはサブスクリプションが保留中であることをユーザーに通知するメッセージを表示することができます。

<a name="collecting-tax-ids"></a>
<!-- ### Collecting Tax IDs -->
### Collecting Tax IDs

<!-- Checkout also supports collecting a customer's Tax ID. To enable this on a checkout session, invoke the `collectTaxIds` method when creating the session: -->
Checkout では、顧客の納税者 ID の収集もサポートされています。チェックアウト セッションでこれを有効にするには、セッションの作成時に `collectTaxIds` メソッドを呼び出します。

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

<!-- When this method is invoked, a new checkbox will be available to the customer that allows them to indicate if they're purchasing as a company. If so, they will have the opportunity to provide their Tax ID number. -->
このメソッドを呼び出すと、顧客は会社として購入するかどうかを示す新しいチェックボックスが利用できるようになります。その場合、納税者 ID 番号を提供する機会が得られます。

> [!WARNING]
> アプリケーションのサービスプロバイダで [automatic tax collection](#tax-configuration) をすでに構成している場合、この機能は自動的に有効になり、`collectTaxIds` メソッドを呼び出す必要はありません。

<a name="guest-checkouts"></a>
<!-- ### Guest Checkouts -->
### Guest Checkouts

<!-- Using the `Checkout::guest` method, you may initiate checkout sessions for guests of your application that do not have an "account": -->
`Checkout::guest` メソッドを使用すると、「アカウント」を持たないアプリケーションのゲストに対してチェックアウト セッションを開始できます。

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
既存のユーザーのチェックアウト セッションを作成する場合と同様に、`Laravel\Cashier\CheckoutBuilder` インスタンスで利用可能な追加のメソッドを利用して、ゲスト チェックアウト セッションをカスタマイズできます。

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
ゲストのチェックアウトが完了すると、Stripe は `checkout.session.completed` Webhook イベントを送信できるため、必ず [configure your Stripe webhook](https://dashboard.stripe.com/webhooks) を実行してこのイベントを実際にアプリケーションに送信してください。 Stripe ダッシュボード内で Webhook が有効になったら、[handle the webhook with Cashier](#handling-stripe-webhooks) を行うことができます。 Webhook ペイロードに含まれるオブジェクトは [checkout object](https://stripe.com/docs/api/checkout/sessions/object) となり、顧客の注文を満たすために検査できます。

<a name="handling-failed-payments"></a>
<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed. -->
場合によっては、サブスクリプションまたは単一料金の支払いが失敗することがあります。これが発生すると、Cashier はこれが発生したことを通知する `Laravel\Cashier\Exceptions\IncompletePayment` 例外をスローします。この例外をキャッチした後、続行する方法には 2 つのオプションがあります。

<!-- First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page: -->
まず、顧客を Cashier に含まれる専用の支払い確認ページにリダイレクトできます。このページには、Cashier のサービスプロバイダを介して登録された、関連付けられた名前付きルートがすでに存在します。したがって、`IncompletePayment` 例外をキャッチして、ユーザーを支払い確認ページにリダイレクトできます。

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
支払い確認ページで、顧客はクレジット カード情報を再度入力し、「3D セキュア」確認など、Stripe で必要な追加のアクションを実行するよう求められます。支払いを確認した後、ユーザーは上で指定した `redirect` パラメータで指定された URL にリダイレクトされます。リダイレクト時に、`message` (文字列) および `success` (整数) クエリ文字列変数が URL に追加されます。支払いページでは現在、次のタイプの支払い方法がサポートされています。

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
- クレジットカード
- アリペイ
- バンコンタクト
- BECS 口座振替
- EPS
- ギロペイ
- iDEAL
- SEPA 口座振替

<!-- </div> -->
</div>

<!-- Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions. -->
あるいは、Stripe が支払い確認を処理できるようにすることもできます。この場合、支払い確認ページにリダイレクトする代わりに、Stripe ダッシュボードで [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) を実行できます。ただし、`IncompletePayment` 例外がキャッチされた場合でも、支払い確認の手順が記載された電子メールを受け取ることをユーザーに通知する必要があります。

<!-- Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions. -->
支払い例外は、`Billable` トレイトを使用するモデルの `charge`、`invoiceFor`、および `invoice` のメソッドに対してスローされる可能性があります。サブスクリプションを操作するとき、`SubscriptionBuilder` の `create` メソッド、および `Subscription` および `SubscriptionItem` モデルの `incrementAndInvoice` および `swapAndInvoice` メソッドは、不完全な支払い例外をスローする場合があります。

<!-- Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance: -->
既存のサブスクリプションに支払いが完了していないかどうかを判断するには、請求可能モデルまたはサブスクリプション インスタンスで `hasIncompletePayment` メソッドを使用します。

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

<!-- You can derive the specific status of an incomplete payment by inspecting the `payment` property on the exception instance: -->
例外インスタンスの `payment` プロパティを検査することで、未完了の支払いの特定のステータスを取得できます。

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
一部の支払い方法では、支払いを確認するために追加のデータが必要です。たとえば、SEPA 支払い方法では、支払いプロセス中に追加の「委任」データが必要になります。 `withPaymentConfirmationOptions` メソッドを使用して、このデータをCashierに提供できます。

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

<!-- You may consult the [Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm) to review all of the options accepted when confirming payments. -->
[Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm) を参照して、支払いを確認するときに受け入れられるすべてのオプションを確認することができます。

<a name="strong-customer-authentication"></a>
<!-- ## Strong Customer Authentication -->
## Strong Customer Authentication

<!-- If your business or one of your customers is based in Europe you will need to abide by the EU's Strong Customer Authentication (SCA) regulations. These regulations were imposed in September 2019 by the European Union to prevent payment fraud. Luckily, Stripe and Cashier are prepared for building SCA compliant applications. -->
あなたのビジネスまたは顧客のいずれかがヨーロッパに拠点を置いている場合は、EU の強力な顧客認証 (SCA) 規制に従う必要があります。これらの規制は、支払い詐欺を防止するために 2019 年 9 月に欧州連合によって課されました。幸いなことに、Stripe と Cashier は SCA 準拠のアプリケーションを構築する準備ができています。

> [!WARNING]
> 始める前に、[Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication) と [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication) を確認してください。

<a name="payments-requiring-additional-confirmation"></a>
<!-- ### Payments Requiring Additional Confirmation -->
### Payments Requiring Additional Confirmation

<!-- SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions can be found in the documentation on [handling failed payments](#handling-failed-payments). -->
SCA 規制では、支払いを確認して処理するために追加の検証が必要になることがよくあります。これが発生すると、Cashier は追加の検証が必要であることを通知する `Laravel\Cashier\Exceptions\IncompletePayment` 例外をスローします。これらの例外を処理する方法の詳細については、[handling failed payments](#handling-failed-payments) のドキュメントを参照してください。

<!-- Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
Stripe または Cashier によって表示される支払い確認画面は、特定の銀行またはカード発行会社の支払いフローに合わせて調整することができ、追加のカード確認、一時的な少額請求、個別のデバイス認証、またはその他の形式の確認を含めることができます。

<a name="incomplete-and-past-due-state"></a>
<!-- #### Incomplete and Past Due State -->
#### Incomplete and Past Due State

<!-- When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion. -->
支払いに追加の確認が必要な場合、サブスクリプションは、`stripe_status` データベース列で示されるように、`incomplete` または `past_due` 状態のままになります。支払い確認が完了し、Stripe から Webhook 経由でアプリケーションに完了が通知されると、Cashier は顧客のサブスクリプションを自動的にアクティブ化します。

<!-- For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status). -->
`incomplete` および `past_due` 状態の詳細については、[our additional documentation on these states](#incomplete-and-past-due-status) を参照してください。

<a name="off-session-payment-notifications"></a>
<!-- ### Off-Session Payment Notifications -->
### Off-Session Payment Notifications

<!-- Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to a notification class. By default, this notification is disabled. Of course, Cashier includes a notification class you may use for this purpose, but you are free to provide your own notification class if desired: -->
SCA 規制により、顧客はサブスクリプションがアクティブな間でも支払いの詳細を時折確認する必要があるため、セッション外の支払い確認が必要な場合、Cashierは顧客に通知を送信できます。たとえば、これはサブスクリプションの更新時に発生する可能性があります。Cashierの支払い通知は、`CASHIER_PAYMENT_NOTIFICATION` 環境変数を通知クラスに設定することで有効にできます。デフォルトでは、この通知は無効になっています。もちろん、Cashier にはこの目的に使用できる通知クラスが含まれていますが、必要に応じて独自の通知クラスを自由に提供できます。

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

<!-- To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait. -->
セッション外の支払い確認通知が確実に配信されるようにするには、アプリケーションの [Stripe webhooks are configured](#handling-stripe-webhooks) と `invoice.payment_action_required` Webhook が Stripe ダッシュボードで有効になっていることを確認してください。さらに、`Billable` モデルは Laravel の `Illuminate\Notifications\Notifiable` トレイトも使用する必要があります。

> [!WARNING]
> 顧客が追加の確認が必要な支払いを手動で行っている場合でも、通知は送信されます。残念ながら、Stripe には支払いが手動で行われたのか、または「オフセッション」で行われたのかを知る方法がありません。ただし、顧客が支払いを確認した後に支払いページにアクセスすると、単に「支払いが成功しました」というメッセージが表示されます。顧客が誤って同じ支払いを 2 回確認して、誤って 2 回目の請求が発生することは許されません。

<a name="stripe-sdk"></a>
<!-- ## Stripe SDK -->
## Stripe SDK

<!-- Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method: -->
Cashier のオブジェクトの多くは、Stripe SDK オブジェクトのラッパーです。 Stripe オブジェクトを直接操作したい場合は、`asStripe` メソッドを使用してオブジェクトを簡単に取得できます。

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

<!-- You may also use the `updateStripeSubscription` method to update a Stripe subscription directly: -->
`updateStripeSubscription` メソッドを使用して、Stripe サブスクリプションを直接更新することもできます。

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

<!-- You may invoke the `stripe` method on the `Cashier` class if you would like to use the `Stripe\StripeClient` client directly. For example, you could use this method to access the `StripeClient` instance and retrieve a list of prices from your Stripe account: -->
`Stripe\StripeClient` クライアントを直接使用したい場合は、`Cashier` クラスの `stripe` メソッドを呼び出すことができます。たとえば、このメソッドを使用して `StripeClient` インスタンスにアクセスし、Stripe アカウントから価格のリストを取得できます。

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- When testing an application that uses Cashier, you may mock the actual HTTP requests to the Stripe API; however, this requires you to partially re-implement Cashier's own behavior. Therefore, we recommend allowing your tests to hit the actual Stripe API. While this is slower, it provides more confidence that your application is working as expected and any slow tests may be placed within their own Pest / PHPUnit testing group. -->
Cashier を使用するアプリケーションをテストする場合、Stripe API への実際の HTTP リクエストをモックすることができます。ただし、これには、Cashier 自体の動作を部分的に再実装する必要があります。したがって、テストが実際の Stripe API にアクセスできるようにすることをお勧めします。これは遅くなりますが、アプリケーションが期待どおりに動作しているという信頼性が高まり、遅いテストは独自の Pest / PHPUnit テスト グループ内に配置される可能性があります。

<!-- When testing, remember that Cashier itself already has a great test suite, so you should only focus on testing the subscription and payment flow of your own application and not every underlying Cashier behavior. -->
テストするときは、Cashier 自体に優れたテスト スイートがすでに用意されているため、基礎となる Cashier の動作をすべてテストするのではなく、独自のアプリケーションのサブスクリプションと支払いフローのテストにのみ重点を置く必要があることに注意してください。

<!-- To get started, add the **testing** version of your Stripe secret to your `phpunit.xml` file: -->
まず、**テスト** バージョンの Stripe シークレットを `phpunit.xml` ファイルに追加します。

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

<!-- Now, whenever you interact with Cashier while testing, it will send actual API requests to your Stripe testing environment. For convenience, you should pre-fill your Stripe testing account with subscriptions / prices that you may use during testing. -->
これで、テスト中に Cashier と対話するたびに、実際の API リクエストが Stripe テスト環境に送信されます。便宜上、Stripe テスト アカウントにテスト中に使用するサブスクリプション/価格を事前に入力しておく必要があります。

> [!NOTE]
> クレジット カードの拒否や失敗など、さまざまな請求シナリオをテストするために、Stripe が提供する幅広い [testing card numbers and tokens](https://stripe.com/docs/testing) を使用できます。

