<!-- # Laravel Cashier (Paddle) -->
# Laravel Cashier (Paddle)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
    - [Database Migrations](#database-migrations)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Paddle JS](#paddle-js)
    - [Currency Configuration](#currency-configuration)
    - [Overriding Default Models](#overriding-default-models)
- [Core Concepts](#core-concepts)
    - [Pay Links](#pay-links)
    - [Inline Checkout](#inline-checkout)
    - [User Identification](#user-identification)
- [Prices](#prices)
- [Customers](#customers)
    - [Customer Defaults](#customer-defaults)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Subscription Single Charges](#subscription-single-charges)
    - [Updating Payment Information](#updating-payment-information)
    - [Changing Plans](#changing-plans)
    - [Subscription Quantity](#subscription-quantity)
    - [Subscription Modifiers](#subscription-modifiers)
    - [Multiple Subscriptions](#multiple-subscriptions)
    - [Pausing Subscriptions](#pausing-subscriptions)
    - [Cancelling Subscriptions](#cancelling-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Payment Method Up Front](#with-payment-method-up-front)
    - [Without Payment Method Up Front](#without-payment-method-up-front)
- [Handling Paddle Webhooks](#handling-paddle-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
    - [Simple Charge](#simple-charge)
    - [Charging Products](#charging-products)
    - [Refunding Orders](#refunding-orders)
- [Receipts](#receipts)
    - [Past & Upcoming Payments](#past-and-upcoming-payments)
- [Handling Failed Payments](#handling-failed-payments)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) provides an expressive, fluent interface to [Paddle's](https://paddle.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading. In addition to basic subscription management, Cashier can handle: coupons, swapping subscription, subscription "quantities", cancellation grace periods, and more. -->
[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) は、[Paddle's](https://paddle.com) サブスクリプション請求サービスへの表現力豊かで流暢なインターフェイスを提供します。あなたが恐れている定型的なサブスクリプション請求コードのほぼすべてを処理します。基本的なサブスクリプション管理に加えて、Cashier はクーポン、サブスクリプションの交換、サブスクリプションの「数量」、キャンセル猶予期間などを処理できます。

<!-- While working with Cashier we recommend you also review Paddle's [user guides](https://developer.paddle.com/guides) and [API documentation](https://developer.paddle.com/api-reference). -->
Cashier を使用する際には、Paddle の [user guides](https://developer.paddle.com/guides) および [API documentation](https://developer.paddle.com/api-reference) も確認することをお勧めします。

<a name="upgrading-cashier"></a>
<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md). -->
Cashier の新しいバージョンにアップグレードする場合は、[the upgrade guide](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Paddle using the Composer package manager: -->
まず、Composer パッケージ マネージャーを使用して Paddle の Cashier パッケージをインストールします。

```shell
composer require laravel/cashier-paddle
```

> [!WARNING]
> Cashier がすべての Paddle イベントを適切に処理できるようにするには、[set up Cashier's webhook handling](#handling-paddle-webhooks) を忘れないでください。

<a name="paddle-sandbox"></a>
<!-- ### Paddle Sandbox -->
### Paddle Sandbox

<!-- During local and staging development, you should [register a Paddle Sandbox account](https://developer.paddle.com/getting-started/sandbox). This account will give you a sandboxed environment to test and develop your applications without making actual payments. You may use Paddle's [test card numbers](https://developer.paddle.com/getting-started/sandbox#test-cards) to simulate various payment scenarios. -->
ローカルおよびステージング開発中は、[register a Paddle Sandbox account](https://developer.paddle.com/getting-started/sandbox) を実行する必要があります。このアカウントでは、実際に支払いを行わずにアプリケーションのテストと開発を行うためのサンドボックス環境が提供されます。 Paddle の [test card numbers](https://developer.paddle.com/getting-started/sandbox#test-cards) を使用して、さまざまな支払いシナリオをシミュレートできます。

<!-- When using the Paddle Sandbox environment, you should set the `PADDLE_SANDBOX` environment variable to `true` within your application's `.env` file: -->
Paddle Sandbox 環境を使用する場合は、アプリケーションの `.env` ファイル内で `PADDLE_SANDBOX` 環境変数を `true` に設定する必要があります。

```ini
PADDLE_SANDBOX=true
```

<!-- After you have finished developing your application you may [apply for a Paddle vendor account](https://paddle.com). Before your application is placed into production, Paddle will need to approve your application's domain. -->
アプリケーションの開発が完了したら、[apply for a Paddle vendor account](https://paddle.com) を実行できます。アプリケーションを運用環境に導入する前に、Paddle はアプリケーションのドメインを承認する必要があります。

<a name="database-migrations"></a>
<!-- ### Database Migrations -->
### Database Migrations

<!-- The Cashier service provider registers its own database migration directory, so remember to migrate your database after installing the package. The Cashier migrations will create a new `customers` table. In addition, a new `subscriptions` table will be created to store all of your customer's subscriptions. Finally, a new `receipts` table will be created to store all of your application's receipt information: -->
Cashier サービスプロバイダは独自のデータベース移行ディレクトリを登録するため、パッケージのインストール後にデータベースを移行することを忘れないでください。 Cashier の移行により、新しい `customers` テーブルが作成されます。さらに、顧客のすべてのサブスクリプションを保存するために、新しい `subscriptions` テーブルが作成されます。最後に、アプリケーションのすべての受信情報を保存するための新しい `receipts` テーブルが作成されます。

```shell
php artisan migrate
```

<!-- If you need to overwrite the migrations that are included with Cashier, you can publish them using the `vendor:publish` Artisan command: -->
Cashier に含まれる移行を上書きする必要がある場合は、`vendor:publish` Artisan コマンドを使用して公開できます。

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- If you would like to prevent Cashier's migrations from running entirely, you may use the `ignoreMigrations` provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
Cashier の移行が完全に実行されないようにする場合は、Cashier が提供する `ignoreMigrations` を使用できます。通常、このメソッドは、`AppServiceProvider` の `register` メソッドで呼び出す必要があります。

```
use Laravel\Paddle\Cashier;

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

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>
<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, you must add the `Billable` trait to your user model definition. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons and updating payment method information: -->
Cashier を使用する前に、`Billable` 特性をユーザー モデル定義に追加する必要があります。この特性は、サブスクリプションの作成、クーポンの適用、支払い方法情報の更新などの一般的な請求タスクを実行できるようにするさまざまなメソッドを提供します。

```
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- If you have billable entities that are not users, you may also add the trait to those classes: -->
ユーザーではない請求可能なエンティティがある場合は、それらのクラスに特性を追加することもできます。

```
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
<!-- ### API Keys -->
### API Keys

<!-- Next, you should configure your Paddle keys in your application's `.env` file. You can retrieve your Paddle API keys from the Paddle control panel: -->
次に、アプリケーションの `.env` ファイルでPaddle キーを構成する必要があります。 Paddle コントロール パネルから Paddle API キーを取得できます。

```ini
PADDLE_VENDOR_ID=your-paddle-vendor-id
PADDLE_VENDOR_AUTH_CODE=your-paddle-vendor-auth-code
PADDLE_PUBLIC_KEY="your-paddle-public-key"
PADDLE_SANDBOX=true
```

<!-- The `PADDLE_SANDBOX` environment variable should be set to `true` when you are using [Paddle's Sandbox environment](#paddle-sandbox). The `PADDLE_SANDBOX` variable should be set to `false` if you are deploying your application to production and are using Paddle's live vendor environment. -->
[Paddle's Sandbox environment](#paddle-sandbox) を使用する場合は、`PADDLE_SANDBOX` 環境変数を `true` に設定する必要があります。アプリケーションを運用環境にデプロイし、Paddle のライブ ベンダー環境を使用している場合は、`PADDLE_SANDBOX` 変数を `false` に設定する必要があります。

<a name="paddle-js"></a>
<!-- ### Paddle JS -->
### Paddle JS

<!-- Paddle relies on its own JavaScript library to initiate the Paddle checkout widget. You can load the JavaScript library by placing the `@paddleJS` Blade directive right before your application layout's closing `</head>` tag: -->
Paddle は、独自の JavaScript ライブラリを利用して Paddle チェックアウト ウィジェットを開始します。アプリケーション レイアウトの `</head>` 終了タグの直前に `@paddleJS` Blade ディレクティブを配置することで、JavaScript ライブラリをロードできます。

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by defining a `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
デフォルトのCashier通貨は米ドル (USD) です。アプリケーションの `.env` ファイル内で `CASHIER_CURRENCY` 環境変数を定義することで、デフォルトの通貨を変更できます。

```ini
CASHIER_CURRENCY=EUR
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
Cashier の通貨を構成することに加えて、請求書に表示する金額の書式を設定するときに使用するロケールを指定することもできます。内部的には、Cashier は [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) を使用して通貨ロケールを設定します。

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 以外のロケールを使用するには、`ext-intl` PHP 拡張機能がサーバーにインストールされ、構成されていることを確認してください。

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
独自のモデルを定義し、対応する Cashier モデルを拡張することで、Cashier によって内部的に使用されるモデルを自由に拡張できます。

```
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Paddle\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
モデルを定義した後、`Laravel\Paddle\Cashier` クラスを介してカスタム モデルを使用するように Cashier に指示できます。通常、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドでカスタム モデルについて Cashier に通知する必要があります。

```
use App\Models\Cashier\Receipt;
use App\Models\Cashier\Subscription;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Cashier::useReceiptModel(Receipt::class);
    Cashier::useSubscriptionModel(Subscription::class);
}
```

<a name="core-concepts"></a>
<!-- ## Core Concepts -->
## Core Concepts

<a name="pay-links"></a>
<!-- ### Pay Links -->
### Pay Links

<!-- Paddle lacks an extensive CRUD API to perform subscription state changes. Therefore, most interactions with Paddle are done through its [checkout widget](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout). Before we can display the checkout widget, we must generate a "pay link" using Cashier. A "pay link" will inform the checkout widget of the billing operation we wish to perform: -->
Paddle には、サブスクリプション状態の変更を実行するための広範な CRUD API がありません。したがって、Paddle とのほとんどの対話は、[checkout widget](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout) を通じて行われます。チェックアウト ウィジェットを表示する前に、Cashier を使用して「支払いリンク」を生成する必要があります。 「有料リンク」は、実行したい請求操作をチェックアウト ウィジェットに通知します。

```
use App\Models\User;
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $premium = 34567)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- Cashier includes a `paddle-button` [Blade component](/docs/9.x/blade#components). We may pass the pay link URL to this component as a "prop". When this button is clicked, Paddle's checkout widget will be displayed: -->
Cashier には、`paddle-button` [Blade component](/docs/9.x/blade#components) が含まれます。有料リンク URL を「小道具」としてこのコンポーネントに渡すことができます。このボタンをクリックすると、Paddle のチェックアウト ウィジェットが表示されます。

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- By default, this will display a button with the standard Paddle styling. You can remove all Paddle styling by adding the `data-theme="none"` attribute to the component: -->
デフォルトでは、標準のPaddleスタイルのボタンが表示されます。 `data-theme="none"` 属性をコンポーネントに追加することで、すべてのPaddle スタイルを削除できます。

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="none">
    Subscribe
</x-paddle-button>
```

<!-- The Paddle checkout widget is asynchronous. Once the user creates or updates a subscription within the widget, Paddle will send your application webhooks so that you may properly update the subscription state in our own database. Therefore, it's important that you properly [set up webhooks](#handling-paddle-webhooks) to accommodate for state changes from Paddle. -->
Paddle チェックアウト ウィジェットは非同期です。ユーザーがウィジェット内でサブスクリプションを作成または更新すると、Paddle はアプリケーション Webhook を送信し、ユーザーが独自のデータベース内のサブスクリプション状態を適切に更新できるようにします。したがって、Paddle からの状態変化に対応できるように [set up webhooks](#handling-paddle-webhooks) を適切に設定することが重要です。

<!-- For more information on pay links, you may review [the Paddle API documentation on pay link generation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink). -->
有料リンクの詳細については、[the Paddle API documentation on pay link generation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) をご覧ください。

> [!WARNING]
> サブスクリプションの状態が変更された後、対応する Webhook を受信するまでの遅延は通常最小限ですが、ユーザーのサブスクリプションがチェックアウト完了後にすぐに利用できない可能性があることを考慮して、アプリケーションでこれを考慮する必要があります。

<a name="manually-rendering-pay-links"></a>
<!-- #### Manually Rendering Pay Links -->
#### Manually Rendering Pay Links

<!-- You may also manually render a pay link without using Laravel's built-in Blade components. To get started, generate the pay link URL as demonstrated in previous examples: -->
Laravel の組み込み Blade コンポーネントを使用せずに、有料リンクを手動でレンダリングすることもできます。まず、前の例で示したように有料リンク URL を生成します。

```
$payLink = $request->user()->newSubscription('default', $premium = 34567)
    ->returnTo(route('home'))
    ->create();
```

<!-- Next, simply attach the pay link URL to an `a` element in your HTML: -->
次に、有料リンク URL を HTML の `a` 要素に添付するだけです。

```
<a href="#!" class="ml-4 paddle_button" data-override="{{ $payLink }}">
    Paddle Checkout
</a>
```

<a name="payments-requiring-additional-confirmation"></a>
<!-- #### Payments Requiring Additional Confirmation -->
#### Payments Requiring Additional Confirmation

<!-- Sometimes additional verification is required in order to confirm and process a payment. When this happens, Paddle will present a payment confirmation screen. Payment confirmation screens presented by Paddle or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
支払いを確認して処理するために追加の検証が必要になる場合があります。これが発生すると、Paddle に支払い確認画面が表示されます。 Paddle または Cashier によって表示される支払い確認画面は、特定の銀行またはカード発行会社の支払いフローに合わせて調整することができ、追加のカード確認、一時的な少額請求、個別のデバイス認証、またはその他の形式の確認を含めることができます。

<a name="inline-checkout"></a>
<!-- ### Inline Checkout -->
### Inline Checkout

<!-- If you don't want to make use of Paddle's "overlay" style checkout widget, Paddle also provides the option to display the widget inline. While this approach does not allow you to adjust any of the checkout's HTML fields, it allows you to embed the widget within your application. -->
Paddle の「オーバーレイ」スタイルのチェックアウト ウィジェットを利用したくない場合、Paddle にはウィジェットをインラインで表示するオプションも用意されています。この方法では、チェックアウトの HTML フィールドを調整することはできませんが、アプリケーション内にウィジェットを埋め込むことができます。

<!-- To make it easy for you to get started with inline checkout, Cashier includes a `paddle-checkout` Blade component. To get started, you should [generate a pay link](#pay-links) and pass the pay link to the component's `override` attribute: -->
インライン チェックアウトを簡単に開始できるように、Cashier には `paddle-checkout` Blade コンポーネントが含まれています。開始するには、[generate a pay link](#pay-links) を実行し、有料リンクをコンポーネントの `override` 属性に渡す必要があります。

```blade
<x-paddle-checkout :override="$payLink" class="w-full" />
```

<!-- To adjust the height of the inline checkout component, you may pass the `height` attribute to the Blade component: -->
インライン チェックアウト コンポーネントの高さを調整するには、`height` 属性を Blade コンポーネントに渡すことができます。

```blade
<x-paddle-checkout :override="$payLink" class="w-full" height="500" />
```

<a name="inline-checkout-without-pay-links"></a>
<!-- #### Inline Checkout Without Pay Links -->
#### Inline Checkout Without Pay Links

<!-- Alternatively, you may customize the widget with custom options instead of using a pay link: -->
あるいは、有料リンクを使用する代わりに、カスタム オプションを使用してウィジェットをカスタマイズすることもできます。

```blade
@php
$options = [
    'product' => $productId,
    'title' => 'Product Title',
];
@endphp

<x-paddle-checkout :options="$options" class="w-full" />
```

<!-- Please consult Paddle's [guide on Inline Checkout](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout) as well as their [parameter reference](https://developer.paddle.com/reference/paddle-js/parameters) for further details on the inline checkout's available options. -->
インライン チェックアウトで利用可能なオプションの詳細については、Paddle の [guide on Inline Checkout](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout) および [parameter reference](https://developer.paddle.com/reference/paddle-js/parameters) を参照してください。

> [!WARNING]
> カスタム オプションを指定するときに `passthrough` オプションも使用したい場合は、その値としてキー/値配列を指定する必要があります。 Cashier は配列の JSON 文字列への変換を自動的に処理します。さらに、`customer_id` パススルー オプションは、内部 Cashier での使用のために予約されています。

<a name="manually-rendering-an-inline-checkout"></a>
<!-- #### Manually Rendering An Inline Checkout -->
#### Manually Rendering An Inline Checkout

<!-- You may also manually render an inline checkout without using Laravel's built-in Blade components. To get started, generate the pay link URL [as demonstrated in previous examples](#pay-links). -->
Laravel の組み込み Blade コンポーネントを使用せずに、インライン チェックアウトを手動でレンダリングすることもできます。まず、有料リンク URL [as demonstrated in previous examples](#pay-links) を生成します。

<!-- Next, you may use Paddle.js to initialize the checkout. To keep this example simple, we will demonstrate this using [Alpine.js](https://github.com/alpinejs/alpine); however, you are free to translate this example to your own frontend stack: -->
次に、Paddle.js を使用してチェックアウトを初期化します。この例を単純にするために、[Alpine.js](https://github.com/alpinejs/alpine) を使用してこれを示します。ただし、この例を独自のフロントエンド スタックに自由に変換できます。

```alpine
<div class="paddle-checkout" x-data="{}" x-init="
    Paddle.Checkout.open({
        override: {{ $payLink }},
        method: 'inline',
        frameTarget: 'paddle-checkout',
        frameInitialHeight: 366,
        frameStyle: 'width: 100%; background-color: transparent; border: none;'
    });
">
</div>
```

<a name="user-identification"></a>
<!-- ### User Identification -->
### User Identification

<!-- In contrast to Stripe, Paddle users are unique across all of Paddle, not unique per Paddle account. Because of this, Paddle's API's do not currently provide a method to update a user's details such as their email address. When generating pay links, Paddle identifies users using the `customer_email` parameter. When creating a subscription, Paddle will try to match the user provided email to an existing Paddle user. -->
Stripe とは対照的に、Paddle ユーザーは Paddle アカウントごとに一意ではなく、Paddle 全体で一意です。このため、Paddle の API には現在、電子メール アドレスなどのユーザーの詳細を更新するメソッドが提供されていません。有料リンクを生成するとき、Paddle は `customer_email` パラメーターを使用してユーザーを識別します。サブスクリプションを作成するとき、Paddle はユーザーが提供した電子メールを既存の Paddle ユーザーと照合しようとします。

<!-- In light of this behavior, there are some important things to keep in mind when using Cashier and Paddle. First, you should be aware that even though subscriptions in Cashier are tied to the same application user, **they could be tied to different users within Paddle's internal systems**. Secondly, each subscription has its own connected payment method information and could also have different email addresses within Paddle's internal systems (depending on which email was assigned to the user when the subscription was created). -->
この動作を考慮して、Cashier と Paddle を使用するときに留意すべき重要な点がいくつかあります。まず、Cashier のサブスクリプションは同じアプリケーション ユーザーに関連付けられているとしても、**Paddle の内部システム内の異なるユーザーに関連付けられる可能性がある**ことに注意する必要があります。第 2 に、各サブスクリプションには独自の接続された支払い方法情報があり、Paddle の内部システム内で異なる電子メール アドレスを持つこともできます (サブスクリプションの作成時にどの電子メールがユーザーに割り当てられたかによって異なります)。

<!-- Therefore, when displaying subscriptions you should always inform the user which email address or payment method information is connected to the subscription on a per-subscription basis. Retrieving this information can be done with the following methods provided by the `Laravel\Paddle\Subscription` model: -->
したがって、サブスクリプションを表示するときは、サブスクリプションごとにどの電子メール アドレスまたは支払い方法情報がサブスクリプションに関連付けられているかを常にユーザーに通知する必要があります。この情報の取得は、`Laravel\Paddle\Subscription` モデルによって提供される次のメソッドを使用して実行できます。

```
$subscription = $user->subscription('default');

$subscription->paddleEmail();
$subscription->paymentMethod();
$subscription->cardBrand();
$subscription->cardLastFour();
$subscription->cardExpirationDate();
```

<!-- There is currently no way to modify a user's email address through the Paddle API. When a user wants to update their email address within Paddle, the only way for them to do so is to contact Paddle customer support. When communicating with Paddle, they need to provide the `paddleEmail` value of the subscription to assist Paddle in updating the correct user. -->
現在、Paddle API を通じてユーザーの電子メール アドレスを変更する方法はありません。ユーザーが Paddle 内で自分の電子メール アドレスを更新したい場合、その唯一の方法は、Paddle カスタマー サポートに連絡することです。 Paddle と通信するときは、Paddle が正しいユーザーを更新できるように、サブスクリプションの `paddleEmail` 値を提供する必要があります。

<a name="prices"></a>
<!-- ## Prices -->
## Prices

<!-- Paddle allows you to customize prices per currency, essentially allowing you to configure different prices for different countries. Cashier Paddle allows you to retrieve all of the prices for a given product using the `productPrices` method. This method accepts the product IDs of the products you wish to retrieve prices for: -->
Paddle を使用すると、通貨ごとに価格をカスタマイズできるため、基本的に国ごとに異なる価格を設定できます。 Cashier Paddle を使用すると、`productPrices` メソッドを使用して、特定の製品のすべての価格を取得できます。このメソッドは、価格を取得したい製品の製品 ID を受け入れます。

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456]);
```

<!-- The currency will be determined based on the IP address of the request; however, you may optionally provide a specific country to retrieve prices for: -->
通貨はリクエストの IP アドレスに基づいて決定されます。ただし、オプションで特定の国を指定して次の価格を取得することもできます。

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], ['customer_country' => 'BE']);
```

<!-- After retrieving the prices you may display them however you wish: -->
価格を取得した後、必要に応じて価格を表示できます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

<!-- You may also display the net price (excludes tax) and display the tax amount separately: -->
正味価格 (税抜) を表示し、税額を個別に表示することもできます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->net() }} (+ {{ $price->price()->tax() }} tax)</li>
    @endforeach
</ul>
```

<!-- If you retrieved prices for subscription plans you can display their initial and recurring price separately: -->
サブスクリプション プランの価格を取得した場合は、初回価格と定期価格を個別に表示できます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - Initial: {{ $price->initialPrice()->gross() }} - Recurring: {{ $price->recurringPrice()->gross() }}</li>
    @endforeach
</ul>
```

<!-- For more information, [check Paddle's API documentation on prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices). -->
詳細については、[check Paddle's API documentation on prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices) をご覧ください。

<a name="prices-customers"></a>
<!-- #### Customers -->
#### Customers

<!-- If a user is already a customer and you would like to display the prices that apply to that customer, you may do so by retrieving the prices directly from the customer instance: -->
ユーザーがすでに顧客であり、その顧客に適用される価格を表示したい場合は、顧客インスタンスから直接価格を取得して表示できます。

```
use App\Models\User;

$prices = User::find(1)->productPrices([123, 456]);
```

<!-- Internally, Cashier will use the user's [`paddleCountry` method](#customer-defaults) to retrieve the prices in their currency. So, for example, a user living in the United States will see prices in USD while a user in Belgium will see prices in EUR. If no matching currency can be found the default currency of the product will be used. You can customize all prices of a product or subscription plan in the Paddle control panel. -->
内部的には、Cashier はユーザーの [`paddleCountry` method](#customer-defaults) を使用して、ユーザーの通貨で価格を取得します。したがって、たとえば、米国に住んでいるユーザーには価格が米ドルで表示され、ベルギーのユーザーには価格がユーロで表示されます。一致する通貨が見つからない場合は、製品のデフォルトの通貨が使用されます。Paddle コントロール パネルで、製品またはサブスクリプション プランのすべての価格をカスタマイズできます。

<a name="prices-coupons"></a>
<!-- #### Coupons -->
#### Coupons

<!-- You may also choose to display prices after a coupon reduction. When calling the `productPrices` method, coupons may be passed as a comma delimited string: -->
クーポン割引後の価格を表示することもできます。 `productPrices` メソッドを呼び出すとき、クーポンはカンマ区切りの文字列として渡される場合があります。

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], [
    'coupons' => 'SUMMERSALE,20PERCENTOFF'
]);
```

<!-- Then, display the calculated prices using the `price` method: -->
次に、`price` メソッドを使用して計算された価格を表示します。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

<!-- You may display the original listed prices (without coupon discounts) using the `listPrice` method: -->
`listPrice` メソッドを使用して、元の表示価格 (クーポン割引なし) を表示できます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->listPrice()->gross() }}</li>
    @endforeach
</ul>
```

> [!WARNING]
> 価格 API を使用する場合、Paddle ではクーポンの適用を 1 回限りの購入製品にのみ許可し、サブスクリプション プランには適用できません。

<a name="customers"></a>
<!-- ## Customers -->
## Customers

<a name="customer-defaults"></a>
<!-- ### Customer Defaults -->
### Customer Defaults

<!-- Cashier allows you to define some useful defaults for your customers when creating pay links. Setting these defaults allow you to pre-fill a customer's email address, country, and postal code so that they can immediately move on to the payment portion of the checkout widget. You can set these defaults by overriding the following methods on your billable model: -->
Cashier を使用すると、有料リンクを作成するときに顧客向けにいくつかの便利なデフォルトを定義できます。これらのデフォルトを設定すると、顧客の電子メール アドレス、国、郵便番号を事前に入力できるため、顧客はすぐにチェックアウト ウィジェットの支払い部分に進むことができます。これらのデフォルトは、請求可能なモデルで次のメソッドをオーバーライドすることで設定できます。

```
/**
 * Get the customer's email address to associate with Paddle.
 *
 * @return string|null
 */
public function paddleEmail()
{
    return $this->email;
}

/**
 * Get the customer's country to associate with Paddle.
 *
 * This needs to be a 2 letter code. See the link below for supported countries.
 *
 * @return string|null
 * @link https://developer.paddle.com/reference/platform-parameters/supported-countries
 */
public function paddleCountry()
{
    //
}

/**
 * Get the customer's postal code to associate with Paddle.
 *
 * See the link below for countries which require this.
 *
 * @return string|null
 * @link https://developer.paddle.com/reference/platform-parameters/supported-countries#countries-requiring-postcode
 */
public function paddlePostcode()
{
    //
}
```

<!-- These defaults will be used for every action in Cashier that generates a [pay link](#pay-links). -->
これらのデフォルトは、[pay link](#pay-links) を生成する Cashier のすべてのアクションに使用されます。

<a name="subscriptions"></a>
<!-- ## Subscriptions -->
## Subscriptions

<a name="creating-subscriptions"></a>
<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model from your database, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription pay link: -->
サブスクリプションを作成するには、まず課金対象モデルのインスタンスをデータベースから取得します。これは通常、`App\Models\User` のインスタンスになります。モデル インスタンスを取得したら、`newSubscription` メソッドを使用してモデルのサブスクリプション有料リンクを作成できます。

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $premium = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- The first argument passed to the `newSubscription` method should be the internal name of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription name is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument given to the `newSubscription` method is the specific plan the user is subscribing to. This value should correspond to the plan's identifier in Paddle. The `returnTo` method accepts a URL that your user will be redirected to after they successfully complete the checkout. -->
`newSubscription` メソッドに渡される最初の引数は、サブスクリプションの内部名である必要があります。アプリケーションが単一のサブスクリプションのみを提供する場合は、これを `default` または `primary` と呼びます。このサブスクリプション名はアプリケーション内部でのみ使用され、ユーザーに表示されることを意図したものではありません。また、スペースを含めることはできません。また、サブスクリプションの作成後に変更しないでください。 `newSubscription` メソッドに指定される 2 番目の引数は、ユーザーが購読している特定のプランです。この値は、Paddle のプランの識別子に対応する必要があります。 `returnTo` メソッドは、ユーザーがチェックアウトを正常に完了した後にリダイレクトされる URL を受け入れます。

<!-- The `create` method will create a pay link which you can use to generate a payment button. The payment button can be generated using the `paddle-button` [Blade component](/docs/9.x/blade#components) that is included with Cashier Paddle: -->
`create` メソッドは、支払いボタンの生成に使用できる支払いリンクを作成します。支払いボタンは、Cashier Paddle に含まれる `paddle-button` [Blade component](/docs/9.x/blade#components) を使用して生成できます。

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- After the user has finished their checkout, a `subscription_created` webhook will be dispatched from Paddle. Cashier will receive this webhook and setup the subscription for your customer. In order to make sure all webhooks are properly received and handled by your application, ensure you have properly [setup webhook handling](#handling-paddle-webhooks). -->
ユーザーがチェックアウトを完了すると、`subscription_created` Webhook が Paddle からディスパッチされます。Cashier はこの Webhook を受信し、顧客のサブスクリプションをセットアップします。すべての Webhook が適切に受信され、アプリケーションによって処理されることを確認するには、[setup webhook handling](#handling-paddle-webhooks) が適切に設定されていることを確認してください。

<a name="additional-details"></a>
<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional customer or subscription details, you may do so by passing them as an array of key / value pairs to the `create` method. To learn more about the additional fields supported by Paddle, check out Paddle's documentation on [generating pay links](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink): -->
追加の顧客またはサブスクリプションの詳細を指定したい場合は、それらをキーと値のペアの配列として `create` メソッドに渡すことで指定できます。 Paddle でサポートされている追加フィールドの詳細については、[generating pay links](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) にある Paddle のドキュメントを参照してください。

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->create([
        'vat_number' => $vatNumber,
    ]);
```

<a name="subscriptions-coupons"></a>
<!-- #### Coupons -->
#### Coupons

<!-- If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method: -->
サブスクリプションの作成時にクーポンを適用したい場合は、`withCoupon` メソッドを使用できます。

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withCoupon('code')
    ->create();
```

<a name="metadata"></a>
<!-- #### Metadata -->
#### Metadata

<!-- You can also pass an array of metadata using the `withMetadata` method: -->
`withMetadata` メソッドを使用してメタデータの配列を渡すこともできます。

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withMetadata(['key' => 'value'])
    ->create();
```

> [!WARNING]
> メタデータを提供するときは、メタデータ キーとして `subscription_name` を使用しないでください。このキーは、Cashierによる内部使用のために予約されています。

<a name="checking-subscription-status"></a>
<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a user is subscribed to your application, you may check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the user has an active subscription, even if the subscription is currently within its trial period: -->
ユーザーがアプリケーションを購読すると、さまざまな便利な方法を使用してその購読ステータスを確認できます。まず、ユーザーがアクティブなサブスクリプションを持っている場合、サブスクリプションが現在試用期間内であっても、`subscribed` メソッドは `true` を返します。

```
if ($user->subscribed('default')) {
    //
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/9.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` メソッドも [route middleware](/docs/9.x/middleware) の有力な候補となり、ユーザーのサブスクリプション ステータスに基づいてルートとコントローラへのアクセスをフィルタリングできます。

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
ユーザーがまだ試用期間内であるかどうかを確認したい場合は、`onTrial` メソッドを使用できます。このメソッドは、ユーザーがまだ試用期間中であることをユーザーに警告するかどうかを決定するのに役立ちます。

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- The `subscribedToPlan` method may be used to determine if the user is subscribed to a given plan based on a given Paddle plan ID. In this example, we will determine if the user's `default` subscription is actively subscribed to the monthly plan: -->
`subscribedToPlan` メソッドは、特定のPaddle プラン ID に基づいて、ユーザーが特定のプランに加入しているかどうかを判断するために使用できます。この例では、ユーザーの `default` サブスクリプションが月次プランにアクティブにサブスクライブされているかどうかを判断します。

```
if ($user->subscribedToPlan($monthly = 12345, 'default')) {
    //
}
```

<!-- By passing an array to the `subscribedToPlan` method, you may determine if the user's `default` subscription is actively subscribed to the monthly or the yearly plan: -->
配列を `subscribedToPlan` メソッドに渡すことによって、ユーザーの `default` サブスクリプションが月次プランまたは年次プランにアクティブにサブスクライブされているかどうかを判断できます。

```
if ($user->subscribedToPlan([$monthly = 12345, $yearly = 54321], 'default')) {
    //
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
`recurring` メソッドは、ユーザーが現在購読中であり、試用期間中でないかどうかを判断するために使用できます。

```
if ($user->subscription('default')->recurring()) {
    //
}
```

<a name="cancelled-subscription-status"></a>
<!-- #### Cancelled Subscription Status -->
#### Cancelled Subscription Status

<!-- To determine if the user was once an active subscriber but has cancelled their subscription, you may use the `cancelled` method: -->
ユーザーがかつてはアクティブなサブスクライバだったが、サブスクリプションをキャンセルしたかどうかを確認するには、`cancelled` メソッドを使用できます。

```
if ($user->subscription('default')->cancelled()) {
    //
}
```

<!-- You may also determine if a user has cancelled their subscription, but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
また、ユーザーがサブスクリプションをキャンセルしたが、サブスクリプションが完全に期限切れになるまでまだ「猶予期間」中であるかどうかを判断することもできます。たとえば、ユーザーが元々 3 月 10 日に期限切れになる予定だったサブスクリプションを 3 月 5 日にキャンセルした場合、ユーザーは 3 月 10 日まで「猶予期間」に入ります。この間も、`subscribed` メソッドは `true` を返すことに注意してください。

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- To determine if the user has cancelled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
ユーザーがサブスクリプションをキャンセルし、「猶予期間」に入っていないかどうかを確認するには、`ended` メソッドを使用できます。

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="past-due-status"></a>
<!-- #### Past Due Status -->
#### Past Due Status

<!-- If a payment fails for a subscription, it will be marked as `past_due`. When your subscription is in this state it will not be active until the customer has updated their payment information. You may determine if a subscription is past due using the `pastDue` method on the subscription instance: -->
サブスクリプションの支払いが失敗した場合、`past_due` としてマークされます。サブスクリプションがこの状態にある場合、顧客が支払い情報を更新するまでアクティブになりません。サブスクリプション インスタンスの `pastDue` メソッドを使用して、サブスクリプションの期限が過ぎているかどうかを確認できます。

```
if ($user->subscription('default')->pastDue()) {
    //
}
```

<!-- When a subscription is past due, you should instruct the user to [update their payment information](#updating-payment-information). You may configure how past due subscriptions are handled in your [Paddle subscription settings](https://vendors.paddle.com/subscription-settings). -->
サブスクリプションの期限を過ぎた場合は、ユーザーに [update their payment information](#updating-payment-information) を指示する必要があります。 [Paddle subscription settings](https://vendors.paddle.com/subscription-settings) で期限を過ぎたサブスクリプションをどのように処理するかを構成できます。

<!-- If you would like subscriptions to still be considered active when they are `past_due`, you may use the `keepPastDueSubscriptionsActive` method provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
サブスクリプションが `past_due` の場合でもアクティブであると見なされたい場合は、Cashier が提供する `keepPastDueSubscriptionsActive` メソッドを使用できます。通常、このメソッドは、`AppServiceProvider` の `register` メソッドで呼び出す必要があります。

```
use Laravel\Paddle\Cashier;

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

> [!WARNING]
> サブスクリプションが `past_due` 状態にある場合、支払い情報が更新されるまで変更することはできません。したがって、サブスクリプションが `past_due` 状態にある場合、`swap` メソッドと `updateQuantity` メソッドは例外をスローします。

<a name="subscription-scopes"></a>
<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
ほとんどのサブスクリプション状態はクエリ スコープとしても使用できるため、特定の状態にあるサブスクリプションについてデータベースを簡単にクエリできます。

```
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the cancelled subscriptions for a user...
$subscriptions = $user->subscriptions()->cancelled()->get();
```

<!-- A complete list of available scopes is available below: -->
利用可能なスコープの完全なリストは以下で入手できます。

```
Subscription::query()->active();
Subscription::query()->onTrial();
Subscription::query()->notOnTrial();
Subscription::query()->pastDue();
Subscription::query()->recurring();
Subscription::query()->ended();
Subscription::query()->paused();
Subscription::query()->notPaused();
Subscription::query()->onPausedGracePeriod();
Subscription::query()->notOnPausedGracePeriod();
Subscription::query()->cancelled();
Subscription::query()->notCancelled();
Subscription::query()->onGracePeriod();
Subscription::query()->notOnGracePeriod();
```

<a name="subscription-single-charges"></a>
<!-- ### Subscription Single Charges -->
### Subscription Single Charges

<!-- Subscription single charges allow you to charge subscribers with a one-time charge on top of their subscriptions: -->
サブスクリプションの単一料金を使用すると、サブスクリプションに加えて 1 回限りの料金をサブスクライバに請求できます。

```
$response = $user->subscription('default')->charge(12.99, 'Support Add-on');
```

<!-- In contrast to [single charges](#single-charges), this method will immediately charge the customer's stored payment method for the subscription. The charge amount should always be defined in the currency of the subscription. -->
[single charges](#single-charges) とは対照的に、この方法では、顧客が保存した支払い方法にすぐにサブスクリプションの料金が請求されます。請求額は常にサブスクリプションの通貨で定義する必要があります。

<a name="updating-payment-information"></a>
<!-- ### Updating Payment Information -->
### Updating Payment Information

<!-- Paddle always saves a payment method per subscription. If you want to update the default payment method for a subscription, you should first generate a subscription "update URL" using the `updateUrl` method on the subscription model: -->
Paddle は常にサブスクリプションごとに支払い方法を保存します。サブスクリプションのデフォルトの支払い方法を更新する場合は、最初にサブスクリプション モデルで `updateUrl` メソッドを使用してサブスクリプションの「更新 URL」を生成する必要があります。

```
use App\Models\User;

$user = User::find(1);

$updateUrl = $user->subscription('default')->updateUrl();
```

<!-- Then, you may use the generated URL in combination with Cashier's provided `paddle-button` Blade component to allow the user to initiate the Paddle widget and update their payment information: -->
次に、生成された URL を Cashier が提供する `paddle-button` Blade コンポーネントと組み合わせて使用​​すると、ユーザーがPaddle ウィジェットを開始して支払い情報を更新できるようになります。

```html
<x-paddle-button :url="$updateUrl" class="px-8 py-4">
    Update Card
</x-paddle-button>
```

<!-- When a user has finished updating their information, a `subscription_updated` webhook will be dispatched by Paddle and the subscription details will be updated in your application's database. -->
ユーザーが情報の更新を完了すると、`subscription_updated` Webhook が Paddle によって送出され、サブスクリプションの詳細がアプリケーションのデータベースで更新されます。

<a name="changing-plans"></a>
<!-- ### Changing Plans -->
### Changing Plans

<!-- After a user has subscribed to your application, they may occasionally want to change to a new subscription plan. To update the subscription plan for a user, you should pass the Paddle plan's identifier to the subscription's `swap` method: -->
ユーザーがアプリケーションを購読した後、新しい購読プランへの変更を希望する場合があります。ユーザーのサブスクリプション プランを更新するには、Paddle プランの識別子をサブスクリプションの `swap` メソッドに渡す必要があります。

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap($premium = 34567);
```

<!-- If you would like to swap plans and immediately invoice the user instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
プランを交換して、次の請求サイクルを待たずにすぐにユーザーに請求を行いたい場合は、`swapAndInvoice` メソッドを使用できます。

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice($premium = 34567);
```

> [!WARNING]
> 試用期間中はプランを切り替えることはできません。この制限に関する追加情報については、[Paddle documentation](https://developer.paddle.com/api-reference/subscription-api/users/updateuser#usage-notes) を参照してください。

<a name="prorations"></a>
<!-- #### Prorations -->
#### Prorations

<!-- By default, Paddle prorates charges when swapping between plans. The `noProrate` method may be used to update the subscriptions without prorating the charges: -->
デフォルトでは、Paddle はプラン間を切り替えるときに料金を日割り計算します。 `noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションを更新できます。

```
$user->subscription('default')->noProrate()->swap($premium = 34567);
```

<a name="subscription-quantity"></a>
<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. To easily increment or decrement your subscription's quantity, use the `incrementQuantity` and `decrementQuantity` methods: -->
サブスクリプションは「数量」の影響を受ける場合があります。たとえば、プロジェクト管理アプリケーションでは、プロジェクトごとに月額 10 ドルを請求する場合があります。サブスクリプションの数量を簡単に増減するには、`incrementQuantity` メソッドと `decrementQuantity` メソッドを使用します。

```
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

```
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
`noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションの数量を更新できます。

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<a name="subscription-modifiers"></a>
<!-- ### Subscription Modifiers -->
### Subscription Modifiers

<!-- Subscription modifiers allow you to implement [metered billing](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers) or extend subscriptions with add-ons. -->
サブスクリプション修飾子を使用すると、[metered billing](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers) を実装したり、アドオンを使用してサブスクリプションを拡張したりできます。

<!-- For example, you might want to offer a "Premium Support" add-on with your standard subscription. You can create this modifier like so: -->
たとえば、標準サブスクリプションで「プレミアム サポート」アドオンを提供したい場合があります。この修飾子は次のように作成できます。

```
$modifier = $user->subscription('default')->newModifier(12.99)->create();
```

<!-- The example above will add a $12.99 add-on to the subscription. By default, this charge will recur on every interval you have configured for the subscription. If you would like, you can add a readable description to the modifier using the modifier's `description` method: -->
上の例では、12.99 ドルのアドオンをサブスクリプションに追加します。デフォルトでは、この料金はサブスクリプションに設定した間隔ごとに繰り返し発生します。必要に応じて、モディファイアの `description` メソッドを使用して、モディファイアに読みやすい説明を追加できます。

```
$modifier = $user->subscription('default')->newModifier(12.99)
    ->description('Premium Support')
    ->create();
```

<!-- To illustrate how to implement metered billing using modifiers, imagine your application charges per SMS message sent by the user. First, you should create a $0 plan in your Paddle dashboard. Once the user has been subscribed to this plan, you can add modifiers representing each individual charge to the subscription: -->
修飾子を使用して従量課金を実装する方法を説明するために、ユーザーが送信した SMS メッセージごとにアプリケーションが料金を請求することを想像してください。まず、Paddle ダッシュボードで $0 プランを作成する必要があります。ユーザーがこのプランにサブスクライブすると、個々の料金を表す修飾子をサブスクリプションに追加できます。

```
$modifier = $user->subscription('default')->newModifier(0.99)
    ->description('New text message')
    ->oneTime()
    ->create();
```

<!-- As you can see, we invoked the `oneTime` method when creating this modifier. This method will ensure the modifier is only charged once and does not recur every billing interval. -->
ご覧のとおり、このモディファイアを作成するときに `oneTime` メソッドを呼び出しました。この方法により、モディファイアは 1 回だけ請求され、請求間隔ごとに繰り返されなくなります。

<a name="retrieving-modifiers"></a>
<!-- #### Retrieving Modifiers -->
#### Retrieving Modifiers

<!-- You may retrieve a list of all modifiers for a subscription via the `modifiers` method: -->
`modifiers` メソッドを使用して、サブスクリプションのすべての修飾子のリストを取得できます。

```
$modifiers = $user->subscription('default')->modifiers();

foreach ($modifiers as $modifier) {
    $modifier->amount(); // $0.99
    $modifier->description; // New text message.
}
```

<a name="deleting-modifiers"></a>
<!-- #### Deleting Modifiers -->
#### Deleting Modifiers

<!-- Modifiers may be deleted by invoking the `delete` method on a `Laravel\Paddle\Modifier` instance: -->
修飾子は、`Laravel\Paddle\Modifier` インスタンスで `delete` メソッドを呼び出すことで削除できます。

```
$modifier->delete();
```

<a name="multiple-subscriptions"></a>
<!-- ### Multiple Subscriptions -->
### Multiple Subscriptions

<!-- Paddle allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans. -->
Paddle を使用すると、顧客は同時に複数のサブスクリプションを持つことができます。たとえば、水泳のサブスクリプションとウェイトリフティングのサブスクリプションを提供するジムを運営しており、各サブスクリプションの価格が異なる場合があります。もちろん、顧客はどちらかまたは両方のプランに加入できる必要があります。

<!-- When your application creates subscriptions, you may provide the name of the subscription to the `newSubscription` method. The name may be any string that represents the type of subscription the user is initiating: -->
アプリケーションがサブスクリプションを作成するとき、`newSubscription` メソッドにサブスクリプションの名前を指定できます。名前には、ユーザーが開始するサブスクリプションのタイプを表す任意の文字列を指定できます。

```
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()
        ->newSubscription('swimming', $swimmingMonthly = 12345)
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- In this example, we initiated a monthly swimming subscription for the customer. However, they may want to swap to a yearly subscription at a later time. When adjusting the customer's subscription, we can simply swap the price on the `swimming` subscription: -->
この例では、顧客に対して毎月の水泳サブスクリプションを開始しました。ただし、後で年間サブスクリプションに切り替えたい場合もあります。顧客のサブスクリプションを調整するときは、`swimming` サブスクリプションの価格を単純に交換できます。

```
$user->subscription('swimming')->swap($swimmingYearly = 34567);
```

<!-- Of course, you may also cancel the subscription entirely: -->
もちろん、サブスクリプションを完全にキャンセルすることもできます。

```
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
<!-- ### Pausing Subscriptions -->
### Pausing Subscriptions

<!-- To pause a subscription, call the `pause` method on the user's subscription: -->
サブスクリプションを一時停止するには、ユーザーのサブスクリプションで `pause` メソッドを呼び出します。

```
$user->subscription('default')->pause();
```

<!-- When a subscription is paused, Cashier will automatically set the `paused_from` column in your database. This column is used to know when the `paused` method should begin returning `true`. For example, if a customer pauses a subscription on March 1st, but the subscription was not scheduled to recur until March 5th, the `paused` method will continue to return `false` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
サブスクリプションが一時停止されると、Cashier はデータベースに `paused_from` 列を自動的に設定します。この列は、`paused` メソッドが `true` を返し始める時期を知るために使用されます。たとえば、顧客が 3 月 1 日にサブスクリプションを一時停止したが、そのサブスクリプションが 3 月 5 日まで繰り返されるようにスケジュールされていなかった場合、`paused` メソッドは 3 月 5 日まで `false` を返し続けます。これは、ユーザーが通常、請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているために行われます。

<!-- You may determine if a user has paused their subscription but are still on their "grace period" using the `onPausedGracePeriod` method: -->
ユーザーがサブスクリプションを一時停止しているが、まだ「猶予期間」中であるかどうかを、`onPausedGracePeriod` メソッドを使用して判断できます。

```
if ($user->subscription('default')->onPausedGracePeriod()) {
    //
}
```

<!-- To resume a paused a subscription, you may call the `unpause` method on the user's subscription: -->
一時停止したサブスクリプションを再開するには、ユーザーのサブスクリプションで `unpause` メソッドを呼び出すことができます。

```
$user->subscription('default')->unpause();
```

> [!WARNING]
> 一時停止中はサブスクリプションを変更できません。別のプランに切り替えたり、数量を更新したりする場合は、まずサブスクリプションを再開する必要があります。

<a name="cancelling-subscriptions"></a>
<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
サブスクリプションをキャンセルするには、ユーザーのサブスクリプションで `cancel` メソッドを呼び出します。

```
$user->subscription('default')->cancel();
```

<!-- When a subscription is cancelled, Cashier will automatically set the `ends_at` column in your database. This column is used to know when the `subscribed` method should begin returning `false`. For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
サブスクリプションがキャンセルされると、Cashier はデータベースに `ends_at` 列を自動的に設定します。この列は、`subscribed` メソッドが `false` を返し始める時期を知るために使用されます。たとえば、顧客が 3 月 1 日にサブスクリプションをキャンセルしたが、そのサブスクリプションが 3 月 5 日まで終了する予定ではなかった場合、`subscribed` メソッドは 3 月 5 日まで `true` を返し続けます。これは、ユーザーが通常、請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているために行われます。

<!-- You may determine if a user has cancelled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
`onGracePeriod` メソッドを使用して、ユーザーがサブスクリプションをキャンセルしたがまだ「猶予期間」中であるかどうかを確認できます。

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- If you wish to cancel a subscription immediately, you may call the `cancelNow` method on the user's subscription: -->
サブスクリプションをすぐにキャンセルしたい場合は、ユーザーのサブスクリプションで `cancelNow` メソッドを呼び出すことができます。

```
$user->subscription('default')->cancelNow();
```

> [!WARNING]
> Paddle のサブスクリプションは、キャンセル後に再開することはできません。顧客がサブスクリプションの再開を希望する場合は、新しいサブスクリプションを購読する必要があります。

<a name="subscription-trials"></a>
<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>
<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

> [!WARNING]
> 事前に支払い方法の詳細を試用して収集している間、Paddle はプランの交換や数量の更新などのサブスクリプションの変更を防ぎます。試用期間中に顧客がプランを交換できるようにするには、サブスクリプションをキャンセルして再作成する必要があります。

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscription pay links: -->
支払い方法情報を事前に収集しながら顧客に試用期間を提供したい場合は、サブスクリプション有料リンクを作成するときに `trialDays` メソッドを使用する必要があります。

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $monthly = 12345)
                ->returnTo(route('home'))
                ->trialDays(10)
                ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- This method will set the trial period ending date on the subscription record within your application's database, as well as instruct Paddle to not begin billing the customer until after this date. -->
このメソッドは、アプリケーションのデータベース内のサブスクリプション レコードに試用期間の終了日を設定し、この日以降になるまで顧客への請求を開始しないように Paddle に指示します。

> [!WARNING]
> 試用期間の終了日までに顧客のサブスクリプションがキャンセルされなかった場合、試用期間が終了するとすぐに料金が請求されるため、ユーザーに試用期間の終了日を必ず通知する必要があります。

<!-- You may determine if the user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
ユーザー インスタンスの `onTrial` メソッドまたはサブスクリプション インスタンスの `onTrial` メソッドを使用して、ユーザーが試用期間内かどうかを判断できます。以下の 2 つの例は同等です。

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods: -->
既存の試用版の有効期限が切れているかどうかを確認するには、`hasExpiredTrial` メソッドを使用できます。

```
if ($user->hasExpiredTrial('default')) {
    //
}

if ($user->subscription('default')->hasExpiredTrial()) {
    //
}
```

<a name="defining-trial-days-in-paddle-cashier"></a>
<!-- #### Defining Trial Days In Paddle / Cashier -->
#### Defining Trial Days In Paddle / Cashier

<!-- You may choose to define how many trial days your plan's receive in the Paddle dashboard or always pass them explicitly using Cashier. If you choose to define your plan's trial days in Paddle you should be aware that new subscriptions, including new subscriptions for a customer that had a subscription in the past, will always receive a trial period unless you explicitly call the `trialDays(0)` method. -->
Paddle ダッシュボードでプランの試用日数を定義することも、Cashier を使用して常に明示的に試用日数を渡すこともできます。 Paddle でプランの試用日を定義することを選択した場合は、`trialDays(0)` メソッドを明示的に呼び出さない限り、過去にサブスクリプションを持っていた顧客の新しいサブスクリプションを含む、新しいサブスクリプションには常に試用期間が与えられることに注意する必要があります。

<a name="without-payment-method-up-front"></a>
<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the customer record attached to your user to your desired trial ending date. This is typically done during user registration: -->
ユーザーの支払い方法情報を事前に収集せずに試用期間を提供したい場合は、ユーザーに添付されている顧客レコードの `trial_ends_at` 列を希望する試用終了日に設定できます。これは通常、ユーザー登録時に行われます。

```
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the `User` instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
既存のサブスクリプションに関連付けられていないため、Cashier はこのタイプのトライアルを「一般トライアル」と呼びます。現在の日付が `trial_ends_at` の値を超えていない場合、`User` インスタンスの `onTrial` メソッドは `true` を返します。

```
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
ユーザーの実際のサブスクリプションを作成する準備ができたら、通常どおり `newSubscription` メソッドを使用できます。

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription name parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
ユーザーの試用終了日を取得するには、`trialEndsAt` メソッドを使用できます。このメソッドは、ユーザーが試用中の場合は Carbon date インスタンスを返し、試用中でない場合は `null` を返します。デフォルト以外の特定のサブスクリプションの試用終了日を取得したい場合は、オプションのサブスクリプション名パラメーターを渡すこともできます。

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not created an actual subscription yet: -->
ユーザーが「一般的な」試用期間内であり、実際のサブスクリプションをまだ作成していないことを具体的に知りたい場合は、`onGenericTrial` メソッドを使用できます。

```
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

> [!WARNING]
> Paddle サブスクリプションの作成後に試用期間を延長または変更する方法はありません。

<a name="handling-paddle-webhooks"></a>
<!-- ## Handling Paddle Webhooks -->
## Handling Paddle Webhooks

<!-- Paddle can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Paddle は、Webhook 経由でさまざまなイベントをアプリケーションに通知できます。デフォルトでは、Cashier の Webhook コントローラを指すルートが Cashier サービスプロバイダによって登録されます。このコントローラは、受信したすべての Webhook リクエストを処理します。

<!-- By default, this controller will automatically handle cancelling subscriptions that have too many failed charges ([as defined by your Paddle dunning settings](https://vendors.paddle.com/recover-settings#dunning-form-id)), subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Paddle webhook event you like. -->
デフォルトでは、このコントローラは、失敗した請求 ([as defined by your Paddle dunning settings](https://vendors.paddle.com/recover-settings#dunning-form-id)) が多すぎるサブスクリプションのキャンセル、サブスクリプションの更新、および支払い方法の変更を自動的に処理します。ただし、すぐにわかりますが、このコントローラを拡張して、任意の Paddle Webhook イベントを処理できます。

<!-- To ensure your application can handle Paddle webhooks, be sure to [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/alerts-webhooks). By default, Cashier's webhook controller responds to the `/paddle/webhook` URL path. The full list of all webhooks you should enable in the Paddle control panel are: -->
アプリケーションが Paddle Webhook を処理できることを確認するには、必ず [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/alerts-webhooks) を実行してください。デフォルトでは、Cashier の Webhook コントローラは `/paddle/webhook` URL パスに応答します。Paddle コントロール パネルで有効にする必要があるすべての Webhook の完全なリストは次のとおりです。

<!--
- Subscription Created
- Subscription Updated
- Subscription Cancelled
- Payment Succeeded
- Subscription Payment Succeeded
-->
- サブスクリプションが作成されました
- サブスクリプションが更新されました
- サブスクリプションがキャンセルされました
- 支払いが完了しました
- 定期購入の支払いが完了しました

> [!WARNING]
> Cashier に含まれる [webhook signature verification](/docs/9.x/cashier-paddle#verifying-webhook-signatures) ミドルウェアを使用して、受信リクエストを必ず保護してください。

<a name="webhooks-csrf-protection"></a>
<!-- #### Webhooks & CSRF Protection -->
#### Webhooks & CSRF Protection

<!-- Since Paddle webhooks need to bypass Laravel's [CSRF protection](/docs/9.x/csrf), be sure to list the URI as an exception in your `App\Http\Middleware\VerifyCsrfToken` middleware or list the route outside of the `web` middleware group: -->
Paddle Webhook は Laravel の [CSRF protection](/docs/9.x/csrf) をバイパスする必要があるため、必ず `App\Http\Middleware\VerifyCsrfToken` ミドルウェアの例外として URI をリストするか、`web` ミドルウェア グループの外側のルートをリストしてください。

```
protected $except = [
    'paddle/*',
];
```

<a name="webhooks-local-development"></a>
<!-- #### Webhooks & Local Development -->
#### Webhooks & Local Development

<!-- For Paddle to be able to send your application webhooks during local development, you will need to expose your application via a site sharing service such as [Ngrok](https://ngrok.com/) or [Expose](https://expose.dev/docs/introduction). If you are developing your application locally using [Laravel Sail](/docs/9.x/sail), you may use Sail's [site sharing command](/docs/9.x/sail#sharing-your-site). -->
Paddle がローカル開発中にアプリケーション Webhook を送信できるようにするには、[Ngrok](https://ngrok.com/) や [Expose](https://expose.dev/docs/introduction) などのサイト共有サービスを介してアプリケーションを公開する必要があります。 [Laravel Sail](/docs/9.x/sail) を使用してアプリケーションをローカルで開発している場合は、Sail の [site sharing command](/docs/9.x/sail#sharing-your-site) を使用できます。

<a name="defining-webhook-event-handlers"></a>
<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancellation on failed charges and other common Paddle webhooks. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier は、失敗した請求やその他の一般的な Paddle Webhook によるサブスクリプションのキャンセルを自動的に処理します。ただし、追加の Webhook イベントを処理したい場合は、Cashier によって送出される次のイベントをリッスンすることで処理できます。

<!--
- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`
-->
- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

<!-- Both events contain the full payload of the Paddle webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/9.x/events#defining-listeners) that will handle the event: -->
どちらのイベントにも、Paddle Webhook の完全なペイロードが含まれています。たとえば、`invoice.payment_succeeded` Webhook を処理したい場合は、イベントを処理する [listener](/docs/9.x/events#defining-listeners) を登録できます。

```
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Handle received Paddle webhooks.
     *
     * @param  \Laravel\Paddle\Events\WebhookReceived  $event
     * @return void
     */
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['alert_name'] === 'payment_succeeded') {
            // Handle the incoming event...
        }
    }
}
```

<!-- Once your listener has been defined, you may register it within your application's `EventServiceProvider`: -->
リスナを定義したら、アプリケーションの `EventServiceProvider` 内にリスナを登録できます。

```
<?php

namespace App\Providers;

use App\Listeners\PaddleEventListener;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Laravel\Paddle\Events\WebhookReceived;

class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        WebhookReceived::class => [
            PaddleEventListener::class,
        ],
    ];
}
```

<!-- Cashier also emit events dedicated to the type of the received webhook. In addition to the full payload from Paddle, they also contain the relevant models that were used to process the webhook such as the billable model, the subscription, or the receipt: -->
Cashier は、受信した Webhook のタイプ専用のイベントも発行します。 Paddle からの完全なペイロードに加えて、請求可能なモデル、サブスクリプション、レシートなど、Webhook の処理に使用された関連モデルも含まれています。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`
-->
- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`

<!-- </div> -->
</div>

<!-- You can also override the default, built-in webhook route by defining the `CASHIER_WEBHOOK` environment variable in your application's `.env` file. This value should be the full URL to your webhook route and needs to match the URL set in your Paddle control panel: -->
アプリケーションの `.env` ファイルで `CASHIER_WEBHOOK` 環境変数を定義することで、デフォルトの組み込み Webhook ルートをオーバーライドすることもできます。この値は Webhook ルートの完全な URL である必要があり、Paddle コントロール パネルで設定された URL と一致する必要があります。

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
<!-- ### Verifying Webhook Signatures -->
### Verifying Webhook Signatures

<!-- To secure your webhooks, you may use [Paddle's webhook signatures](https://developer.paddle.com/webhook-reference/verifying-webhooks). For convenience, Cashier automatically includes a middleware which validates that the incoming Paddle webhook request is valid. -->
Webhook を保護するには、[Paddle's webhook signatures](https://developer.paddle.com/webhook-reference/verifying-webhooks) を使用できます。便宜上、Cashier には、受信した Paddle Webhook リクエストが有効であることを検証するミドルウェアが自動的に組み込まれています。

<!-- To enable webhook verification, ensure that the `PADDLE_PUBLIC_KEY` environment variable is defined in your application's `.env` file. The public key may be retrieved from your Paddle account dashboard. -->
Webhook 検証を有効にするには、`PADDLE_PUBLIC_KEY` 環境変数がアプリケーションの `.env` ファイルで定義されていることを確認してください。公開キーは、Paddle アカウントのダッシュボードから取得できます。

<a name="single-charges"></a>
<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>
<!-- ### Simple Charge -->
### Simple Charge

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance to generate a pay link for the charge. The `charge` method accepts the charge amount (float) as its first argument and a charge description as its second argument: -->
顧客に対して 1 回限りの請求を行う場合は、請求可能なモデル インスタンスで `charge` メソッドを使用して、請求用の有料リンクを生成できます。 `charge` メソッドは、最初の引数として請求金額 (浮動小数点数) を受け入れ、2 番目の引数として請求の説明を受け入れます。

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $user->charge(12.99, 'Action Figure')
    ]);
});
```

<!-- After generating the pay link, you may use Cashier's provided `paddle-button` Blade component to allow the user to initiate the Paddle widget and complete the charge: -->
有料リンクを生成した後、Cashier が提供する `paddle-button` Blade コンポーネントを使用して、ユーザーがPaddle ウィジェットを開始してチャージを完了できるようにすることができます。

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

<!-- The `charge` method accepts an array as its third argument, allowing you to pass any options you wish to the underlying Paddle pay link creation. Please consult [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) to learn more about the options available to you when creating charges: -->
`charge` メソッドは 3 番目の引数として配列を受け入れ、基になるPaddle有料リンクの作成に必要なオプションを渡すことができます。料金作成時に利用できるオプションの詳細については、[the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) を参照してください。

```
$payLink = $user->charge(12.99, 'Action Figure', [
    'custom_option' => $value,
]);
```

<!-- Charges happen in the currency specified in the `cashier.currency` configuration option. By default, this is set to USD. You may override the default currency by defining the `CASHIER_CURRENCY` environment variable in your application's `.env` file: -->
料金は、`cashier.currency` 構成オプションで指定された通貨で発生します。デフォルトでは、これは USD に設定されています。アプリケーションの `.env` ファイルで `CASHIER_CURRENCY` 環境変数を定義することで、デフォルトの通貨をオーバーライドできます。

```ini
CASHIER_CURRENCY=EUR
```

<!-- You can also [override prices per currency](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink#price-overrides) using Paddle's dynamic pricing matching system. To do so, pass an array of prices instead of a fixed amount: -->
Paddle の動的価格マッチング システムを使用して [override prices per currency](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink#price-overrides) することもできます。これを行うには、固定金額の代わりに価格の配列を渡します。

```
$payLink = $user->charge([
    'USD:19.99',
    'EUR:15.99',
], 'Action Figure');
```

<a name="charging-products"></a>
<!-- ### Charging Products -->
### Charging Products

<!-- If you would like to make a one-time charge against a specific product configured within Paddle, you may use the `chargeProduct` method on a billable model instance to generate a pay link: -->
Paddle 内で構成された特定の製品に対して 1 回限りの請求を行いたい場合は、請求可能なモデル インスタンスで `chargeProduct` メソッドを使用して有料リンクを生成できます。

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $request->user()->chargeProduct($productId = 123)
    ]);
});
```

<!-- Then, you may provide the pay link to the `paddle-button` component to allow the user to initialize the Paddle widget: -->
次に、`paddle-button` コンポーネントへの有料リンクを提供して、ユーザーがPaddle ウィジェットを初期化できるようにします。

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

<!-- The `chargeProduct` method accepts an array as its second argument, allowing you to pass any options you wish to the underlying Paddle pay link creation. Please consult [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) regarding the options that are available to you when creating charges: -->
`chargeProduct` メソッドは 2 番目の引数として配列を受け入れ、基になるPaddle有料リンクの作成に必要なオプションを渡すことができます。料金作成時に利用できるオプションについては、[the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) を参照してください。

```
$payLink = $user->chargeProduct($productId, [
    'custom_option' => $value,
]);
```

<a name="refunding-orders"></a>
<!-- ### Refunding Orders -->
### Refunding Orders

<!-- If you need to refund a Paddle order, you may use the `refund` method. This method accepts the Paddle order ID as its first argument. You may retrieve the receipts for a given billable model using the `receipts` method: -->
Paddle の注文を返金する必要がある場合は、`refund` メソッドを使用できます。このメソッドは、最初の引数としてPaddle注文 ID を受け入れます。 `receipts` メソッドを使用して、特定の請求可能モデルの領収書を取得できます。

```
use App\Models\User;

$user = User::find(1);

$receipt = $user->receipts()->first();

$refundRequestId = $user->refund($receipt->order_id);
```

<!-- You may optionally specify a specific amount to refund as well as a reason for the refund: -->
オプションで、特定の返金金額と返金の理由を指定できます。

```
$receipt = $user->receipts()->first();

$refundRequestId = $user->refund(
    $receipt->order_id, 5.00, 'Unused product time'
);
```

> [!NOTE]
> Paddle サポートに連絡するときに、`$refundRequestId` を返金の参照として使用できます。

<a name="receipts"></a>
<!-- ## Receipts -->
## Receipts

<!-- You may easily retrieve an array of a billable model's receipts via the `receipts` property: -->
`receipts` プロパティを使用して、請求可能なモデルの領収書の配列を簡単に取得できます。

```
use App\Models\User;

$user = User::find(1);

$receipts = $user->receipts;
```

<!-- When listing the receipts for the customer, you may use the receipt instance's methods to display the relevant receipt information. For example, you may wish to list every receipt in a table, allowing the user to easily download any of the receipts: -->
顧客の領収書をリストする場合、領収書インスタンスのメソッドを使用して、関連する領収書情報を表示できます。たとえば、すべての領収書を表にリストして、ユーザーが任意の領収書を簡単にダウンロードできるようにすることができます。

```html
<table>
    @foreach ($receipts as $receipt)
        <tr>
            <td>{{ $receipt->paid_at->toFormattedDateString() }}</td>
            <td>{{ $receipt->amount() }}</td>
            <td><a href="{{ $receipt->receipt_url }}" target="_blank">Download</a></td>
        </tr>
    @endforeach
</table>
```

<a name="past-and-upcoming-payments"></a>
<!-- ### Past & Upcoming Payments -->
### Past & Upcoming Payments

<!-- You may use the `lastPayment` and `nextPayment` methods to retrieve and display a customer's past or upcoming payments for recurring subscriptions: -->
`lastPayment` メソッドと `nextPayment` メソッドを使用して、定期購読に対する顧客の過去または今後の支払いを取得して表示できます。

```
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription('default');

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

<!-- Both of these methods will return an instance of `Laravel\Paddle\Payment`; however, `nextPayment` will return `null` when the billing cycle has ended (such as when a subscription has been cancelled): -->
これらのメソッドは両方とも、`Laravel\Paddle\Payment` のインスタンスを返します。ただし、請求サイクルが終了すると (サブスクリプションがキャンセルされた場合など)、`nextPayment` は `null` を返します。

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="handling-failed-payments"></a>
<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Subscription payments fail for various reasons, such as expired cards or a card having insufficient funds. When this happens, we recommend that you let Paddle handle payment failures for you. Specifically, you may [setup Paddle's automatic billing emails](https://vendors.paddle.com/subscription-settings) in your Paddle dashboard. -->
カードの有効期限が切れたり、カードの残高が不足したりするなど、さまざまな理由でサブスクリプションの支払いが失敗します。このような場合は、Paddle に支払い失敗の処理を任せることをお勧めします。具体的には、Paddle ダッシュボードで [setup Paddle's automatic billing emails](https://vendors.paddle.com/subscription-settings) を行うことができます。

<!-- Alternatively, you can perform more precise customization by [listening](/docs/9.x/events) for the `subscription_payment_failed` Paddle event via the `WebhookReceived` event dispatched by Cashier. You should also ensure the "Subscription Payment Failed" option is enabled in the Webhook settings of your Paddle dashboard: -->
あるいは、Cashier によってディスパッチされる `WebhookReceived` イベントを介して、`subscription_payment_failed` Paddle イベントの [listening](/docs/9.x/events) により、より正確なカスタマイズを実行することもできます。また、Paddle ダッシュボードの Webhook 設定で「サブスクリプションの支払いに失敗しました」オプションが有効になっていることを確認する必要があります。

```
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Handle received Paddle webhooks.
     *
     * @param  \Laravel\Paddle\Events\WebhookReceived  $event
     * @return void
     */
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['alert_name'] === 'subscription_payment_failed') {
            // Handle the failed subscription payment...
        }
    }
}
```

<!-- Once your listener has been defined, you should register it within your application's `EventServiceProvider`: -->
リスナを定義したら、それをアプリケーションの `EventServiceProvider` 内に登録する必要があります。

```
<?php

namespace App\Providers;

use App\Listeners\PaddleEventListener;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Laravel\Paddle\Events\WebhookReceived;

class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        WebhookReceived::class => [
            PaddleEventListener::class,
        ],
    ];
}
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- While testing, you should manually test your billing flow to make sure your integration works as expected. -->
テスト中に、請求フローを手動でテストして、統合が期待どおりに機能することを確認する必要があります。

<!-- For automated tests, including those executed within a CI environment, you may use [Laravel's HTTP Client](/docs/9.x/http-client#testing) to fake HTTP calls made to Paddle. Although this does not test the actual responses from Paddle, it does provide a way to test your application without actually calling Paddle's API. -->
CI 環境内で実行されるテストを含む自動テストの場合、[Laravel's HTTP Client](/docs/9.x/http-client#testing) を使用して Paddle に対して行われた HTTP 呼び出しを偽装できます。これは Paddle からの実際の応答をテストしませんが、実際に Paddle の API を呼び出さずにアプリケーションをテストする方法を提供します。

