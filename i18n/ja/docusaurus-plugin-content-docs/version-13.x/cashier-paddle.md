<!-- # Laravel Cashier (Paddle) -->
# Laravel Cashier (Paddle)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Paddle JS](#paddle-js)
    - [Currency Configuration](#currency-configuration)
    - [Overriding Default Models](#overriding-default-models)
- [Quickstart](#quickstart)
    - [Selling Products](#quickstart-selling-products)
    - [Selling Subscriptions](#quickstart-selling-subscriptions)
- [Checkout Sessions](#checkout-sessions)
    - [Overlay Checkout](#overlay-checkout)
    - [Inline Checkout](#inline-checkout)
    - [Guest Checkouts](#guest-checkouts)
- [Price Previews](#price-previews)
    - [Customer Price Previews](#customer-price-previews)
    - [Discounts](#price-discounts)
- [Customers](#customers)
    - [Customer Defaults](#customer-defaults)
    - [Retrieving Customers](#retrieving-customers)
    - [Creating Customers](#creating-customers)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Subscription Single Charges](#subscription-single-charges)
    - [Updating Payment Information](#updating-payment-information)
    - [Changing Plans](#changing-plans)
    - [Subscription Quantity](#subscription-quantity)
    - [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)
    - [Multiple Subscriptions](#multiple-subscriptions)
    - [Pausing Subscriptions](#pausing-subscriptions)
    - [Canceling Subscriptions](#canceling-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Payment Method Up Front](#with-payment-method-up-front)
    - [Without Payment Method Up Front](#without-payment-method-up-front)
    - [Extend or Activate a Trial](#extend-or-activate-a-trial)
- [Handling Paddle Webhooks](#handling-paddle-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
    - [Charging for Products](#charging-for-products)
    - [Refunding Transactions](#refunding-transactions)
    - [Crediting Transactions](#crediting-transactions)
- [Transactions](#transactions)
    - [Past and Upcoming Payments](#past-and-upcoming-payments)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!WARNING]
> このドキュメントは、Cashier Paddle 2.x と Paddle Billing の統合に関するものです。まだ Paddle Classic を使用している場合は、[Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x) を使用する必要があります。

<!-- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) provides an expressive, fluent interface to [Paddle's](https://paddle.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading. In addition to basic subscription management, Cashier can handle: swapping subscriptions, subscription "quantities", subscription pausing, cancelation grace periods, and more. -->
[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) は、[Paddle's](https://paddle.com) サブスクリプション請求サービスへの表現力豊かで流暢なインターフェイスを提供します。あなたが恐れている定型的なサブスクリプション請求コードのほぼすべてを処理します。基本的なサブスクリプション管理に加えて、Cashier はサブスクリプションの交換、サブスクリプションの「数量」、サブスクリプションの一時停止、キャンセルの猶予期間などを処理できます。

<!-- Before digging into Cashier Paddle, we recommend you also review Paddle's [concept guides](https://developer.paddle.com/concepts/overview) and [API documentation](https://developer.paddle.com/api-reference/overview). -->
Cashier Paddle について詳しく説明する前に、Paddle の [concept guides](https://developer.paddle.com/concepts/overview) と [API documentation](https://developer.paddle.com/api-reference/overview) も確認することをお勧めします。

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

<!-- Next, you should publish the Cashier migration files using the `vendor:publish` Artisan command: -->
次に、`vendor:publish` Artisan コマンドを使用して、Cashier 移行ファイルを公開する必要があります。

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- Then, you should run your application's database migrations. The Cashier migrations will create a new `customers` table. In addition, new `subscriptions` and `subscription_items` tables will be created to store all of your customer's subscriptions. Lastly, a new `transactions` table will be created to store all of the Paddle transactions associated with your customers: -->
次に、アプリケーションのデータベース移行を実行する必要があります。 Cashier の移行により、新しい `customers` テーブルが作成されます。さらに、顧客のすべてのサブスクリプションを保存するために、新しい `subscriptions` テーブルと `subscription_items` テーブルが作成されます。最後に、顧客に関連付けられたすべての Paddle トランザクションを保存するための新しい `transactions` テーブルが作成されます。

```shell
php artisan migrate
```

> [!WARNING]
> Cashier がすべての Paddle イベントを適切に処理できるようにするには、[set up Cashier's webhook handling](#handling-paddle-webhooks) を忘れないでください。

<a name="paddle-sandbox"></a>
<!-- ### Paddle Sandbox -->
### Paddle Sandbox

<!-- During local and staging development, you should [register a Paddle Sandbox account](https://sandbox-login.paddle.com/signup). This account will give you a sandboxed environment to test and develop your applications without making actual payments. You may use Paddle's [test card numbers](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method) to simulate various payment scenarios. -->
ローカルおよびステージング開発中は、[register a Paddle Sandbox account](https://sandbox-login.paddle.com/signup) を実行する必要があります。このアカウントでは、実際に支払いを行わずにアプリケーションのテストと開発を行うためのサンドボックス環境が提供されます。 Paddle の [test card numbers](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method) を使用して、さまざまな支払いシナリオをシミュレートできます。

<!-- When using the Paddle Sandbox environment, you should set the `PADDLE_SANDBOX` environment variable to `true` within your application's `.env` file: -->
Paddle Sandbox 環境を使用する場合は、アプリケーションの `.env` ファイル内で `PADDLE_SANDBOX` 環境変数を `true` に設定する必要があります。

```ini
PADDLE_SANDBOX=true
```

<!-- After you have finished developing your application you may [apply for a Paddle vendor account](https://paddle.com). Before your application is placed into production, Paddle will need to approve your application's domain. -->
アプリケーションの開発が完了したら、[apply for a Paddle vendor account](https://paddle.com) を実行できます。アプリケーションを運用環境に導入する前に、Paddle はアプリケーションのドメインを承認する必要があります。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>
<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, you must add the `Billable` trait to your user model definition. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions and updating payment method information: -->
Cashier を使用する前に、`Billable` 特性をユーザー モデル定義に追加する必要があります。この特性は、サブスクリプションの作成や支払い方法情報の更新など、一般的な請求タスクを実行できるようにするさまざまなメソッドを提供します。

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- If you have billable entities that are not users, you may also add the trait to those classes: -->
ユーザーではない請求可能なエンティティがある場合は、それらのクラスに特性を追加することもできます。

```php
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
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

<!-- The `PADDLE_SANDBOX` environment variable should be set to `true` when you are using [Paddle's Sandbox environment](#paddle-sandbox). The `PADDLE_SANDBOX` variable should be set to `false` if you are deploying your application to production and are using Paddle's live vendor environment. -->
[Paddle's Sandbox environment](#paddle-sandbox) を使用する場合は、`PADDLE_SANDBOX` 環境変数を `true` に設定する必要があります。アプリケーションを運用環境にデプロイし、Paddle のライブ ベンダー環境を使用している場合は、`PADDLE_SANDBOX` 変数を `false` に設定する必要があります。

<!-- The `PADDLE_RETAIN_KEY` is optional and should only be set if you're using Paddle with [Retain](https://developer.paddle.com/concepts/retain/overview). -->
`PADDLE_RETAIN_KEY` はオプションであり、[Retain](https://developer.paddle.com/concepts/retain/overview) で Paddle を使用している場合にのみ設定する必要があります。

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

<!-- You can specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
請求書に表示する金額の書式を設定するときに使用するロケールを指定できます。内部的には、Cashier は [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) を使用して通貨ロケールを設定します。

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

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Paddle\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
モデルを定義した後、`Laravel\Paddle\Cashier` クラスを介してカスタム モデルを使用するように Cashier に指示できます。通常、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドでカスタム モデルについて Cashier に通知する必要があります。

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\Transaction;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useTransactionModel(Transaction::class);
}
```

<a name="quickstart"></a>
<!-- ## Quickstart -->
## Quickstart

<a name="quickstart-selling-products"></a>
<!-- ### Selling Products -->
### Selling Products

> [!NOTE]
> Paddle Checkout を利用する前に、Paddle ダッシュボードで固定価格の製品を定義する必要があります。さらに、[configure Paddle's webhook handling](#handling-paddle-webhooks) を実行する必要があります。

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Paddle's Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout), you can easily build modern, robust payment integrations. -->
アプリケーション経由で製品やサブスクリプションの請求を行うのは、威圧的な場合があります。ただし、Cashier と [Paddle's Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) のおかげで、最新の堅牢な支払い統合を簡単に構築できます。

<!-- To charge customers for non-recurring, single-charge products, we'll utilize Cashier to charge customers with Paddle's Checkout Overlay, where they will provide their payment details and confirm their purchase. Once the payment has been made via the Checkout Overlay, the customer will be redirected to a success URL of your choosing within your application: -->
非定期的な 1 回限りの製品に対して顧客に請求するには、Cashier を利用して顧客に Paddle の Checkout Overlay を請求します。顧客はそこで支払いの詳細を提供し、購入を確認します。チェックアウト オーバーレイ経由で支払いが完了すると、顧客はアプリケーション内で選択した成功 URL にリダイレクトされます。

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

<!-- As you can see in the example above, we will utilize Cashier's provided `checkout` method to create a checkout object to present the customer the Paddle Checkout Overlay for a given "price identifier". When using Paddle, "prices" refer to [defined prices for specific products](https://developer.paddle.com/build/products/create-products-prices). -->
上の例でわかるように、Cashierが提供する `checkout` メソッドを利用して、特定の「価格識別子」のPaddle チェックアウト オーバーレイを顧客に提示するチェックアウト オブジェクトを作成します。 Paddle を使用する場合、「価格」は [defined prices for specific products](https://developer.paddle.com/build/products/create-products-prices) を指します。

<!-- If necessary, the `checkout` method will automatically create a customer in Paddle and connect that Paddle customer record to the corresponding user in your application's database. After completing the checkout session, the customer will be redirected to a dedicated success page where you can display an informational message to the customer. -->
必要に応じて、`checkout` メソッドは Paddle に顧客を自動的に作成し、その Paddle 顧客レコードをアプリケーションのデータベース内の対応するユーザーに接続します。チェックアウト セッションが完了すると、顧客は専用の成功ページにリダイレクトされ、そこで顧客に情報メッセージを表示できます。

<!-- In the `buy` view, we will include a button to display the Checkout Overlay. The `paddle-button` Blade component is included with Cashier Paddle; however, you may also [manually render an overlay checkout](#manually-rendering-an-overlay-checkout): -->
`buy` ビューには、チェックアウト オーバーレイを表示するボタンが含まれます。 `paddle-button` Blade コンポーネントは Cashier Paddle に含まれています。ただし、[manually render an overlay checkout](#manually-rendering-an-overlay-checkout) を実行することもできます。

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
<!-- #### Providing Meta Data to Paddle Checkout -->
#### Providing Meta Data to Paddle Checkout

<!-- When selling products, it's common to keep track of completed orders and purchased products via `Cart` and `Order` models defined by your own application. When redirecting customers to Paddle's Checkout Overlay to complete a purchase, you may need to provide an existing order identifier so that you can associate the completed purchase with the corresponding order when the customer is redirected back to your application. -->
製品を販売する場合、独自のアプリケーションで定義された `Cart` および `Order` モデルを介して、完了した注文と購入した製品を追跡するのが一般的です。購入を完了するために顧客を Paddle の Checkout Overlay にリダイレクトする場合、顧客がアプリケーションにリダイレクトされたときに完了した購入を対応する注文に関連付けることができるように、既存の注文 ID を提供する必要がある場合があります。

<!-- To accomplish this, you may provide an array of custom data to the `checkout` method. Let's imagine that a pending `Order` is created within our application when a user begins the checkout process. Remember, the `Cart` and `Order` models in this example are illustrative and not provided by Cashier. You are free to implement these concepts based on the needs of your own application: -->
これを実現するには、カスタム データの配列を `checkout` メソッドに提供します。ユーザーがチェックアウトプロセスを開始したときに、アプリケーション内で保留中の `Order` が作成されると想像してみましょう。この例の `Cart` モデルと `Order` モデルは説明用であり、Cashier によって提供されるものではないことに注意してください。独自のアプリケーションのニーズに基づいて、これらの概念を自由に実装できます。

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

    $checkout = $request->user()->checkout($order->price_ids)
        ->customData(['order_id' => $order->id]);

    return view('billing', ['checkout' => $checkout]);
})->name('checkout');
```

<!-- As you can see in the example above, when a user begins the checkout process, we will provide all of the cart / order's associated Paddle price identifiers to the `checkout` method. Of course, your application is responsible for associating these items with the "shopping cart" or order as a customer adds them. We also provide the order's ID to the Paddle Checkout Overlay via the `customData` method. -->
上の例でわかるように、ユーザーがチェックアウト プロセスを開始すると、カート/注文に関連付けられたすべてのPaddle 価格識別子が `checkout` メソッドに提供されます。もちろん、アプリケーションは、顧客がこれらの商品を追加したときに、これらの商品を「ショッピング カート」または注文に関連付ける責任があります。また、`customData` メソッドを介して注文の ID をPaddle チェックアウト オーバーレイに提供します。

<!-- Of course, you will likely want to mark the order as "complete" once the customer has finished the checkout process. To accomplish this, you may listen to the webhooks dispatched by Paddle and raised via events by Cashier to store order information in your database. -->
もちろん、顧客がチェックアウトプロセスを完了したら、注文を「完了」としてマークすることもできます。これを実現するには、Paddle によってディスパッチされ、Cashier によってイベント経由で発生した Webhook をリッスンして、注文情報をデータベースに保存します。

<!-- To get started, listen for the `TransactionCompleted` event dispatched by Cashier. Typically, you should register the event listener in the `boot` method of your application's `AppServiceProvider`: -->
まず、Cashier によって送出される `TransactionCompleted` イベントをリッスンします。通常、アプリケーションの `AppServiceProvider` の `boot` メソッドにイベント リスナを登録する必要があります。

```php
use App\Listeners\CompleteOrder;
use Illuminate\Support\Facades\Event;
use Laravel\Paddle\Events\TransactionCompleted;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(TransactionCompleted::class, CompleteOrder::class);
}
```

<!-- In this example, the `CompleteOrder` listener might look like the following: -->
この例では、`CompleteOrder` リスナは次のようになります。

```php
namespace App\Listeners;

use App\Models\Order;
use Laravel\Paddle\Cashier;
use Laravel\Paddle\Events\TransactionCompleted;

class CompleteOrder
{
    /**
     * Handle the incoming Cashier webhook event.
     */
    public function handle(TransactionCompleted $event): void
    {
        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

        $order = Order::findOrFail($orderId);

        $order->update(['status' => 'completed']);
    }
}
```

<!-- Please refer to Paddle's documentation for more information on the [data contained by the `transaction.completed` event](https://developer.paddle.com/webhooks/transactions/transaction-completed). -->
[data contained by the `transaction.completed` event](https://developer.paddle.com/webhooks/transactions/transaction-completed) の詳細については、Paddle のドキュメントを参照してください。

<a name="quickstart-selling-subscriptions"></a>
<!-- ### Selling Subscriptions -->
### Selling Subscriptions

> [!NOTE]
> Paddle Checkout を利用する前に、Paddle ダッシュボードで固定価格の製品を定義する必要があります。さらに、[configure Paddle's webhook handling](#handling-paddle-webhooks) を実行する必要があります。

<!-- Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Paddle's Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout), you can easily build modern, robust payment integrations. -->
アプリケーション経由で製品やサブスクリプションの請求を行うのは、威圧的な場合があります。ただし、Cashier と [Paddle's Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) のおかげで、最新の堅牢な支払い統合を簡単に構築できます。

<!-- To learn how to sell subscriptions using Cashier and Paddle's Checkout Overlay, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Paddle dashboard. In addition, our subscription service might offer an "Expert" plan as `pro_expert`. -->
Cashier と Paddle の Checkout Overlay を使用してサブスクリプションを販売する方法を学ぶために、基本的な月次 (`price_basic_monthly`) および年次 (`price_basic_yearly`) プランを持つサブスクリプション サービスの簡単なシナリオを考えてみましょう。これら 2 つの価格は、Paddle ダッシュボードの「Basic」製品 (`pro_basic`) にグループ化できます。さらに、当社のサブスクリプション サービスでは、`pro_expert` として「エキスパート」プランを提供する場合があります。

<!-- First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button will invoke a Paddle Checkout Overlay for their chosen plan. To get started, let's initiate a checkout session via the `checkout` method: -->
まず、顧客がサービスに登録する方法を見てみましょう。もちろん、顧客がアプリケーションの価格設定ページでベーシック プランの「購読」ボタンをクリックする可能性があることは想像できます。このボタンは、選択したプランのPaddle チェックアウト オーバーレイを呼び出します。まず、`checkout` メソッドを使用してチェックアウト セッションを開始しましょう。

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

<!-- In the `subscribe` view, we will include a button to display the Checkout Overlay. The `paddle-button` Blade component is included with Cashier Paddle; however, you may also [manually render an overlay checkout](#manually-rendering-an-overlay-checkout): -->
`subscribe` ビューには、チェックアウト オーバーレイを表示するボタンが含まれます。 `paddle-button` Blade コンポーネントは Cashier Paddle に含まれています。ただし、[manually render an overlay checkout](#manually-rendering-an-overlay-checkout) を実行することもできます。

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- Now, when the Subscribe button is clicked, the customer will be able to enter their payment details and initiate their subscription. To know when their subscription has actually started (since some payment methods require a few seconds to process), you should also [configure Cashier's webhook handling](#handling-paddle-webhooks). -->
「購読」ボタンをクリックすると、顧客は支払いの詳細を入力して購読を開始できるようになります。サブスクリプションが実際にいつ開始されたかを知るには (支払い方法によっては処理に数秒かかるため)、[configure Cashier's webhook handling](#handling-paddle-webhooks) も必要です。

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

<!-- For convenience, you may wish to create a [middleware](/docs/13.x/middleware) which determines if the incoming request is from a subscribed user. Once this middleware has been defined, you may easily assign it to a route to prevent users that are not subscribed from accessing the route: -->
便宜上、受信リクエストが購読ユーザーからのものであるかどうかを判断する [middleware](/docs/13.x/middleware) を作成するとよいでしょう。このミドルウェアを定義したら、それをルートに簡単に割り当てて、サブスクライブされていないユーザーがルートにアクセスできないようにすることができます。

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
            return redirect('/subscribe');
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

<!-- Of course, customers may want to change their subscription plan to another product or "tier". In our example from above, we'd want to allow the customer to change their plan from a monthly subscription to a yearly subscription. For this you'll need to implement something like a button that leads to the below route: -->
もちろん、顧客はサブスクリプション プランを別の製品または「階層」に変更したい場合もあります。上記の例では、顧客が月次サブスクリプションから年次サブスクリプションにプランを変更できるようにしたいと考えています。このためには、以下のルートにつながるボタンのようなものを実装する必要があります。

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // With "$price" being "price_basic_yearly" for this example.

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

<!-- Besides swapping plans you'll also need to allow your customers to cancel their subscription. Like swapping plans, provide a button that leads to the following route: -->
プランを交換するだけでなく、顧客がサブスクリプションをキャンセルできるようにする必要もあります。プランの切り替えと同様に、次のルートにつながるボタンを提供します。

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

<!-- And now your subscription will get canceled at the end of its billing period. -->
そして、請求期間の終了時にサブスクリプションはキャンセルされます。

> [!NOTE]
> Cashier の Webhook 処理を構成している限り、Cashier は Paddle から受信した Webhook を検査することで、アプリケーションの Cashier 関連のデータベース テーブルの同期を自動的に維持します。したがって、たとえば、Paddle のダッシュボード経由で顧客のサブスクリプションをキャンセルすると、Cashier は対応する Webhook を受け取り、アプリケーションのデータベース内でサブスクリプションを「キャンセル済み」としてマークします。

<a name="checkout-sessions"></a>
<!-- ## Checkout Sessions -->
## Checkout Sessions

<!-- Most operations to bill customers are performed using "checkouts" via Paddle's [Checkout Overlay widget](https://developer.paddle.com/build/checkout/build-overlay-checkout) or by utilizing [inline checkout](https://developer.paddle.com/build/checkout/build-branded-inline-checkout). -->
顧客に請求するほとんどの操作は、Paddle の [Checkout Overlay widget](https://developer.paddle.com/build/checkout/build-overlay-checkout) を介した「チェックアウト」を使用するか、[inline checkout](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) を利用して実行されます。

<!-- Before processing checkout payments using Paddle, you should define your application's [default payment link](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link) in your Paddle checkout settings dashboard. -->
Paddle を使用してチェックアウト支払いを処理する前に、Paddle チェックアウト設定ダッシュボードでアプリケーションの [default payment link](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link) を定義する必要があります。

<a name="overlay-checkout"></a>
<!-- ### Overlay Checkout -->
### Overlay Checkout

<!-- Before displaying the Checkout Overlay widget, you must generate a checkout session using Cashier. A checkout session will inform the checkout widget of the billing operation that should be performed: -->
チェックアウト オーバーレイ ウィジェットを表示する前に、Cashier を使用してチェックアウト セッションを生成する必要があります。チェックアウト セッションは、実行する必要がある請求操作をチェックアウト ウィジェットに通知します。

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- Cashier includes a `paddle-button` [Blade component](/docs/13.x/blade#components). You may pass the checkout session to this component as a "prop". Then, when this button is clicked, Paddle's checkout widget will be displayed: -->
Cashier には、`paddle-button` [Blade component](/docs/13.x/blade#components) が含まれます。チェックアウト セッションを「prop」としてこのコンポーネントに渡すことができます。次に、このボタンをクリックすると、Paddle のチェックアウト ウィジェットが表示されます。

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- By default, this will display the widget using Paddle's default styling. You can customize the widget by adding [Paddle supported attributes](https://developer.paddle.com/paddlejs/html-data-attributes) like the  `data-theme='light'` attribute to the component: -->
デフォルトでは、Paddle のデフォルトのスタイルを使用してウィジェットが表示されます。 `data-theme='light'` 属性のような [Paddle supported attributes](https://developer.paddle.com/paddlejs/html-data-attributes) をコンポーネントに追加することで、ウィジェットをカスタマイズできます。

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

<!-- The Paddle checkout widget is asynchronous. Once the user creates a subscription within the widget, Paddle will send your application a webhook so that you may properly update the subscription state in your application's database. Therefore, it's important that you properly [set up webhooks](#handling-paddle-webhooks) to accommodate for state changes from Paddle. -->
Paddle チェックアウト ウィジェットは非同期です。ユーザーがウィジェット内でサブスクリプションを作成すると、アプリケーションのデータベース内のサブスクリプション状態を適切に更新できるように、Paddle がアプリケーションに Webhook を送信します。したがって、Paddle からの状態変化に対応できるように [set up webhooks](#handling-paddle-webhooks) を適切に設定することが重要です。

> [!WARNING]
> サブスクリプションの状態が変更された後、対応する Webhook を受信するまでの遅延は通常最小限ですが、ユーザーのサブスクリプションがチェックアウト完了後にすぐに利用できない可能性があることを考慮して、アプリケーションでこれを考慮する必要があります。

<a name="manually-rendering-an-overlay-checkout"></a>
<!-- #### Manually Rendering an Overlay Checkout -->
#### Manually Rendering an Overlay Checkout

<!-- You may also manually render an overlay checkout without using Laravel's built-in Blade components. To get started, generate the checkout session [as demonstrated in previous examples](#overlay-checkout): -->
Laravel の組み込み Blade コンポーネントを使用せずに、オーバーレイ チェックアウトを手動でレンダリングすることもできます。まず、チェックアウト セッション [as demonstrated in previous examples](#overlay-checkout) を生成します。

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- Next, you may use Paddle.js to initialize the checkout. In this example, we will create a link that is assigned the `paddle_button` class. Paddle.js will detect this class and display the overlay checkout when the link is clicked: -->
次に、Paddle.js を使用してチェックアウトを初期化します。この例では、`paddle_button` クラスが割り当てられたリンクを作成します。 Paddle.js はこのクラスを検出し、リンクをクリックするとオーバーレイ チェックアウトを表示します。

```blade
<?php
$items = $checkout->getItems();
$customer = $checkout->getCustomer();
$custom = $checkout->getCustomData();
?>

<a
    href='#!'
    class='paddle_button'
    data-items='{!! json_encode($items) !!}'
    @if ($customer) data-customer-id='{{ $customer->paddle_id }}' @endif
    @if ($custom) data-custom-data='{{ json_encode($custom) }}' @endif
    @if ($returnUrl = $checkout->getReturnUrl()) data-success-url='{{ $returnUrl }}' @endif
>
    Buy Product
</a>
```

<a name="inline-checkout"></a>
<!-- ### Inline Checkout -->
### Inline Checkout

<!-- If you don't want to make use of Paddle's "overlay" style checkout widget, Paddle also provides the option to display the widget inline. While this approach does not allow you to adjust any of the checkout's HTML fields, it allows you to embed the widget within your application. -->
Paddle の「オーバーレイ」スタイルのチェックアウト ウィジェットを利用したくない場合、Paddle にはウィジェットをインラインで表示するオプションも用意されています。この方法では、チェックアウトの HTML フィールドを調整することはできませんが、アプリケーション内にウィジェットを埋め込むことができます。

<!-- To make it easy for you to get started with inline checkout, Cashier includes a `paddle-checkout` Blade component. To get started, you should [generate a checkout session](#overlay-checkout): -->
インライン チェックアウトを簡単に開始できるように、Cashier には `paddle-checkout` Blade コンポーネントが含まれています。開始するには、[generate a checkout session](#overlay-checkout) を実行する必要があります。

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- Then, you may pass the checkout session to the component's `checkout` attribute: -->
次に、チェックアウト セッションをコンポーネントの `checkout` 属性に渡すことができます。

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

<!-- To adjust the height of the inline checkout component, you may pass the `height` attribute to the Blade component: -->
インライン チェックアウト コンポーネントの高さを調整するには、`height` 属性を Blade コンポーネントに渡すことができます。

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

<!-- Please consult Paddle's [guide on Inline Checkout](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) and [available checkout settings](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings) for further details on the inline checkout's customization options. -->
インライン チェックアウトのカスタマイズ オプションの詳細については、Paddle の [guide on Inline Checkout](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) および [available checkout settings](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings) を参照してください。

<a name="manually-rendering-an-inline-checkout"></a>
<!-- #### Manually Rendering an Inline Checkout -->
#### Manually Rendering an Inline Checkout

<!-- You may also manually render an inline checkout without using Laravel's built-in Blade components. To get started, generate the checkout session [as demonstrated in previous examples](#inline-checkout): -->
Laravel の組み込み Blade コンポーネントを使用せずに、インライン チェックアウトを手動でレンダリングすることもできます。まず、チェックアウト セッション [as demonstrated in previous examples](#inline-checkout) を生成します。

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- Next, you may use Paddle.js to initialize the checkout. In this example, we will demonstrate this using [Alpine.js](https://github.com/alpinejs/alpine); however, you are free to modify this example for your own frontend stack: -->
次に、Paddle.js を使用してチェックアウトを初期化します。この例では、[Alpine.js](https://github.com/alpinejs/alpine) を使用してこれを示します。ただし、この例は独自のフロントエンド スタック用に自由に変更できます。

```blade
<?php
$options = $checkout->options();

$options['settings']['frameTarget'] = 'paddle-checkout';
$options['settings']['frameInitialHeight'] = 366;
?>

<div class="paddle-checkout" x-data="{}" x-init="
    Paddle.Checkout.open(@json($options));
">
</div>
```

<a name="guest-checkouts"></a>
<!-- ### Guest Checkouts -->
### Guest Checkouts

<!-- Sometimes, you may need to create a checkout session for users that do not need an account with your application. To do so, you may use the `guest` method: -->
場合によっては、アプリケーションのアカウントを必要としないユーザーのためにチェックアウト セッションを作成することが必要になる場合があります。これを行うには、`guest` メソッドを使用できます。

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- Then, you may provide the checkout session to the [Paddle button](#overlay-checkout) or [inline checkout](#inline-checkout) Blade components. -->
次に、[Paddle button](#overlay-checkout) または [inline checkout](#inline-checkout) Blade コンポーネントにチェックアウト セッションを提供できます。

<a name="price-previews"></a>
<!-- ## Price Previews -->
## Price Previews

<!-- Paddle allows you to customize prices per currency, essentially allowing you to configure different prices for different countries. Cashier Paddle allows you to retrieve all of these prices using the `previewPrices` method. This method accepts the price IDs you wish to retrieve prices for: -->
Paddle を使用すると、通貨ごとに価格をカスタマイズできるため、基本的に国ごとに異なる価格を設定できます。 Cashier Paddle を使用すると、`previewPrices` メソッドを使用してこれらの価格をすべて取得できます。このメソッドは、価格を取得する価格 ID を受け入れます。

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

<!-- The currency will be determined based on the IP address of the request; however, you may optionally provide a specific country to retrieve prices for: -->
通貨はリクエストの IP アドレスに基づいて決定されます。ただし、オプションで特定の国を指定して次の価格を取得することもできます。

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

<!-- After retrieving the prices you may display them however you wish: -->
価格を取得した後、必要に応じて価格を表示できます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

<!-- You may also display the subtotal price and tax amount separately: -->
小計価格と税額を個別に表示することもできます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

<!-- For more information, [checkout Paddle's API documentation regarding price previews](https://developer.paddle.com/api-reference/pricing-preview/preview-prices). -->
詳細については、[checkout Paddle's API documentation regarding price previews](https://developer.paddle.com/api-reference/pricing-preview/preview-prices) をご覧ください。

<a name="customer-price-previews"></a>
<!-- ### Customer Price Previews -->
### Customer Price Previews

<!-- If a user is already a customer and you would like to display the prices that apply to that customer, you may do so by retrieving the prices directly from the customer instance: -->
ユーザーがすでに顧客であり、その顧客に適用される価格を表示したい場合は、顧客インスタンスから直接価格を取得して表示できます。

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

<!-- Internally, Cashier will use the user's customer ID to retrieve the prices in their currency. So, for example, a user living in the United States will see prices in US dollars while a user in Belgium will see prices in Euros. If no matching currency can be found, the default currency of the product will be used. You can customize all prices of a product or subscription plan in the Paddle control panel. -->
内部的には、Cashier はユーザーの顧客 ID を使用して、その通貨での価格を取得します。したがって、たとえば、米国に住んでいるユーザーには価格が米ドルで表示され、ベルギーのユーザーには価格がユーロで表示されます。一致する通貨が見つからない場合は、製品のデフォルトの通貨が使用されます。Paddle コントロール パネルで、製品またはサブスクリプション プランのすべての価格をカスタマイズできます。

<a name="price-discounts"></a>
<!-- ### Discounts -->
### Discounts

<!-- You may also choose to display prices after a discount. When calling the `previewPrices` method, you provide the discount ID via the `discount_id` option: -->
割引後の価格を表示することもできます。 `previewPrices` メソッドを呼び出すときは、`discount_id` オプションを使用して割引 ID を指定します。

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

<!-- Then, display the calculated prices: -->
次に、計算された価格を表示します。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

<a name="customers"></a>
<!-- ## Customers -->
## Customers

<a name="customer-defaults"></a>
<!-- ### Customer Defaults -->
### Customer Defaults

<!-- Cashier allows you to define some useful defaults for your customers when creating checkout sessions. Setting these defaults allow you to pre-fill a customer's email address and name so that they can immediately move on to the payment portion of the checkout widget. You can set these defaults by overriding the following methods on your billable model: -->
Cashier を使用すると、チェックアウト セッションを作成するときに、顧客にとって役立つデフォルトをいくつか定義できます。これらのデフォルトを設定すると、顧客の電子メール アドレスと名前を事前に入力できるため、顧客はすぐにチェックアウト ウィジェットの支払い部分に進むことができます。これらのデフォルトは、請求可能なモデルで次のメソッドをオーバーライドすることで設定できます。

```php
/**
 * Get the customer's name to associate with Paddle.
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Get the customer's email address to associate with Paddle.
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

<!-- These defaults will be used for every action in Cashier that generates a [checkout session](#checkout-sessions). -->
これらのデフォルトは、[checkout session](#checkout-sessions) を生成する Cashier のすべてのアクションに使用されます。

<a name="retrieving-customers"></a>
<!-- ### Retrieving Customers -->
### Retrieving Customers

<!-- You can retrieve a customer by their Paddle Customer ID using the `Cashier::findBillable` method. This method will return an instance of the billable model: -->
`Cashier::findBillable` メソッドを使用して、Paddle 顧客 ID によって顧客を取得できます。このメソッドは、課金対象モデルのインスタンスを返します。

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
<!-- ### Creating Customers -->
### Creating Customers

<!-- Occasionally, you may wish to create a Paddle customer without beginning a subscription. You may accomplish this using the `createAsCustomer` method: -->
場合によっては、サブスクリプションを開始せずに Paddle 顧客を作成したい場合があります。これは、`createAsCustomer` メソッドを使用して実行できます。

```php
$customer = $user->createAsCustomer();
```

<!-- An instance of `Laravel\Paddle\Customer` is returned. Once the customer has been created in Paddle, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Paddle API](https://developer.paddle.com/api-reference/customers/create-customer): -->
`Laravel\Paddle\Customer` のインスタンスが返されます。 Paddle で顧客を作成したら、後日サブスクリプションを開始できます。オプションの `$options` 配列を指定して、追加の [customer creation parameters that are supported by the Paddle API](https://developer.paddle.com/api-reference/customers/create-customer) を渡すことができます。

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
<!-- ## Subscriptions -->
## Subscriptions

<a name="creating-subscriptions"></a>
<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model from your database, which will typically be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `subscribe` method to create the model's checkout session: -->
サブスクリプションを作成するには、まず課金対象モデルのインスタンスをデータベースから取得します。これは通常、`App\Models\User` のインスタンスになります。モデル インスタンスを取得したら、`subscribe` メソッドを使用してモデルのチェックアウト セッションを作成できます。

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- The first argument given to the `subscribe` method is the specific price the user is subscribing to. This value should correspond to the price's identifier in Paddle. The `returnTo` method accepts a URL that your user will be redirected to after they successfully complete the checkout. The second argument passed to the `subscribe` method should be the internal "type" of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription type is only for internal application usage and is not meant to be displayed to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. -->
`subscribe` メソッドに指定される最初の引数は、ユーザーが購読している特定の価格です。この値は、Paddle の価格の識別子に対応する必要があります。 `returnTo` メソッドは、ユーザーがチェックアウトを正常に完了した後にリダイレクトされる URL を受け入れます。 `subscribe` メソッドに渡される 2 番目の引数は、サブスクリプションの内部「タイプ」である必要があります。アプリケーションが単一のサブスクリプションのみを提供する場合は、これを `default` または `primary` と呼びます。このサブスクリプション タイプはアプリケーション内部でのみ使用され、ユーザーに表示されることを意図したものではありません。また、スペースを含めることはできません。また、サブスクリプションの作成後に変更しないでください。

<!-- You may also provide an array of custom metadata regarding the subscription using the `customData` method: -->
`customData` メソッドを使用して、サブスクリプションに関するカスタム メタデータの配列を提供することもできます。

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

<!-- Once a subscription checkout session has been created, the checkout session may be provided to the `paddle-button` [Blade component](#overlay-checkout) that is included with Cashier Paddle: -->
サブスクリプションのチェックアウト セッションが作成されると、そのチェックアウト セッションは、Cashier Paddle に含まれる `paddle-button` [Blade component](#overlay-checkout) に提供されます。

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- After the user has finished their checkout, a `subscription_created` webhook will be dispatched from Paddle. Cashier will receive this webhook and set up the subscription for your customer. In order to make sure all webhooks are properly received and handled by your application, ensure you have properly [set up webhook handling](#handling-paddle-webhooks). -->
ユーザーがチェックアウトを完了すると、`subscription_created` Webhook が Paddle からディスパッチされます。Cashier はこの Webhook を受信し、顧客のサブスクリプションをセットアップします。すべての Webhook がアプリケーションで適切に受信され、処理されるようにするには、[set up webhook handling](#handling-paddle-webhooks) が正しく設定されていることを確認してください。

<a name="checking-subscription-status"></a>
<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a user is subscribed to your application, you may check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the user has a valid subscription, even if the subscription is currently within its trial period: -->
ユーザーがアプリケーションを購読すると、さまざまな便利な方法を使用してその購読ステータスを確認できます。まず、ユーザーが有効なサブスクリプションを持っている場合、サブスクリプションが現在試用期間内であっても、`subscribed` メソッドは `true` を返します。

```php
if ($user->subscribed()) {
    // ...
}
```

<!-- If your application offers multiple subscriptions, you may specify the subscription when invoking the `subscribed` method: -->
アプリケーションが複数のサブスクリプションを提供する場合、`subscribed` メソッドを呼び出すときにサブスクリプションを指定できます。

```php
if ($user->subscribed('default')) {
    // ...
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/13.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` メソッドも [route middleware](/docs/13.x/middleware) の有力な候補となり、ユーザーのサブスクリプション ステータスに基づいてルートとコントローラへのアクセスをフィルタリングできます。

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
        if ($request->user() && ! $request->user()->subscribed()) {
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
if ($user->subscription()->onTrial()) {
    // ...
}
```

<!-- The `subscribedToPrice` method may be used to determine if the user is subscribed to a given plan based on a given Paddle price ID. In this example, we will determine if the user's `default` subscription is actively subscribed to the monthly price: -->
`subscribedToPrice` メソッドは、特定の Paddle 価格 ID に基づいて、ユーザーが特定のプランに加入しているかどうかを判断するために使用できます。この例では、ユーザーの `default` サブスクリプションが月額料金にアクティブにサブスクライブされているかどうかを判断します。

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

<!-- The `recurring` method may be used to determine if the user is currently on an active subscription and is no longer within their trial period or on a grace period: -->
`recurring` メソッドを使用して、ユーザーが現在アクティブなサブスクリプションに参加していて、もはや試用期間中でも猶予期間中でもないかどうかを判断できます。

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
<!-- #### Canceled Subscription Status -->
#### Canceled Subscription Status

<!-- To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method: -->
ユーザーがかつてはアクティブなサブスクライバだったが、サブスクリプションをキャンセルしたかどうかを確認するには、`canceled` メソッドを使用できます。

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

<!-- You may also determine if a user has canceled their subscription, but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. In addition, the `subscribed` method will still return `true` during this time: -->
また、ユーザーがサブスクリプションをキャンセルしたが、サブスクリプションが完全に期限切れになるまでまだ「猶予期間」中であるかどうかを判断することもできます。たとえば、ユーザーが元々 3 月 10 日に期限切れになる予定だったサブスクリプションを 3 月 5 日にキャンセルした場合、ユーザーは 3 月 10 日まで「猶予期間」に入ります。さらに、`subscribed` メソッドは、この間も `true` を返します。

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
<!-- #### Past Due Status -->
#### Past Due Status

<!-- If a payment fails for a subscription, it will be marked as `past_due`. When your subscription is in this state it will not be active until the customer has updated their payment information. You may determine if a subscription is past due using the `pastDue` method on the subscription instance: -->
サブスクリプションの支払いが失敗した場合、`past_due` としてマークされます。サブスクリプションがこの状態にある場合、顧客が支払い情報を更新するまでアクティブになりません。サブスクリプション インスタンスの `pastDue` メソッドを使用して、サブスクリプションの期限が過ぎているかどうかを確認できます。

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

<!-- When a subscription is past due, you should instruct the user to [update their payment information](#updating-payment-information). -->
サブスクリプションの期限を過ぎた場合は、ユーザーに [update their payment information](#updating-payment-information) を指示する必要があります。

<!-- If you would like subscriptions to still be considered valid when they are `past_due`, you may use the `keepPastDueSubscriptionsActive` method provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
サブスクリプションが `past_due` の場合でも有効であると見なしたい場合は、Cashier が提供する `keepPastDueSubscriptionsActive` メソッドを使用できます。通常、このメソッドは、`AppServiceProvider` の `register` メソッドで呼び出す必要があります。

```php
use Laravel\Paddle\Cashier;

/**
 * Register any application services.
 */
public function register(): void
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

```php
// Get all valid subscriptions...
$subscriptions = Subscription::query()->valid()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

<!-- A complete list of available scopes is available below: -->
利用可能なスコープの完全なリストは以下で入手できます。

```php
Subscription::query()->valid();
Subscription::query()->onTrial();
Subscription::query()->expiredTrial();
Subscription::query()->notOnTrial();
Subscription::query()->active();
Subscription::query()->recurring();
Subscription::query()->pastDue();
Subscription::query()->paused();
Subscription::query()->notPaused();
Subscription::query()->onPausedGracePeriod();
Subscription::query()->notOnPausedGracePeriod();
Subscription::query()->canceled();
Subscription::query()->notCanceled();
Subscription::query()->onGracePeriod();
Subscription::query()->notOnGracePeriod();
```

<a name="subscription-single-charges"></a>
<!-- ### Subscription Single Charges -->
### Subscription Single Charges

<!-- Subscription single charges allow you to charge subscribers with a one-time charge on top of their subscriptions. You must provide one or multiple price ID's when invoking the `charge` method: -->
サブスクリプションの単一料金を使用すると、サブスクリプションに加えて 1 回限りの料金をサブスクライバに請求できます。 `charge` メソッドを呼び出すときは、1 つまたは複数の価格 ID を指定する必要があります。

```php
// Charge a single price...
$response = $user->subscription()->charge('pri_123');

// Charge multiple prices at once...
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

<!-- The `charge` method will not actually charge the customer until the next billing interval of their subscription. If you would like to bill the customer immediately, you may use the `chargeAndInvoice` method instead: -->
`charge` メソッドでは、サブスクリプションの次の請求間隔まで実際には顧客に請求されません。顧客にすぐに請求したい場合は、代わりに `chargeAndInvoice` メソッドを使用できます。

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
<!-- ### Updating Payment Information -->
### Updating Payment Information

<!-- Paddle always saves a payment method per subscription. If you want to update the default payment method for a subscription, you should redirect your customer to Paddle's hosted payment method update page using the `redirectToUpdatePaymentMethod` method on the subscription model: -->
Paddle は常にサブスクリプションごとに支払い方法を保存します。サブスクリプションのデフォルトの支払い方法を更新する場合は、サブスクリプション モデルの `redirectToUpdatePaymentMethod` メソッドを使用して、顧客を Paddle のホスト型支払い方法更新ページにリダイレクトする必要があります。

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

<!-- When a user has finished updating their information, a `subscription_updated` webhook will be dispatched by Paddle and the subscription details will be updated in your application's database. -->
ユーザーが情報の更新を完了すると、`subscription_updated` Webhook が Paddle によって送出され、サブスクリプションの詳細がアプリケーションのデータベースで更新されます。

<a name="changing-plans"></a>
<!-- ### Changing Plans -->
### Changing Plans

<!-- After a user has subscribed to your application, they may occasionally want to change to a new subscription plan. To update the subscription plan for a user, you should pass the Paddle price's identifier to the subscription's `swap` method: -->
ユーザーがアプリケーションを購読した後、新しい購読プランへの変更を希望する場合があります。ユーザーのサブスクリプション プランを更新するには、Paddle 価格の識別子をサブスクリプションの `swap` メソッドに渡す必要があります。

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

<!-- If you would like to swap plans and immediately invoice the user instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
プランを交換して、次の請求サイクルを待たずにすぐにユーザーに請求を行いたい場合は、`swapAndInvoice` メソッドを使用できます。

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
<!-- #### Prorations -->
#### Prorations

<!-- By default, Paddle prorates charges when swapping between plans. The `noProrate` method may be used to update the subscriptions without prorating the charges: -->
デフォルトでは、Paddle はプラン間を切り替えるときに料金を日割り計算します。 `noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションを更新できます。

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

<!-- If you would like to disable proration and invoice customers immediately, you may use the `swapAndInvoice` method in combination with `noProrate`: -->
日割り計算と請求書の顧客をすぐに無効にしたい場合は、`swapAndInvoice` メソッドを `noProrate` と組み合わせて使用​​できます。

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

<!-- Or, to not bill your customer for a subscription change, you may utilize the `doNotBill` method: -->
または、サブスクリプションの変更に対して顧客に請求しないようにするには、`doNotBill` メソッドを利用することもできます。

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

<!-- For more information on Paddle's proration policies, please consult Paddle's [proration documentation](https://developer.paddle.com/concepts/subscriptions/proration). -->
Paddle の比例配分ポリシーの詳細については、Paddle の [proration documentation](https://developer.paddle.com/concepts/subscriptions/proration) を参照してください。

<a name="subscription-quantity"></a>
<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. To easily increment or decrement your subscription's quantity, use the `incrementQuantity` and `decrementQuantity` methods: -->
サブスクリプションは「数量」の影響を受ける場合があります。たとえば、プロジェクト管理アプリケーションでは、プロジェクトごとに月額 10 ドルを請求する場合があります。サブスクリプションの数量を簡単に増減するには、`incrementQuantity` メソッドと `decrementQuantity` メソッドを使用します。

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription()->decrementQuantity(5);
```

<!-- Alternatively, you may set a specific quantity using the `updateQuantity` method: -->
あるいは、`updateQuantity` メソッドを使用して特定の数量を設定することもできます。

```php
$user->subscription()->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
`noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションの数量を更新できます。

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
<!-- #### Quantities for Subscriptions With Multiple Products -->
#### Quantities for Subscriptions With Multiple Products

<!-- If your subscription is a [subscription with multiple products](#subscriptions-with-multiple-products), you should pass the ID of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods: -->
サブスクリプションが [subscription with multiple products](#subscriptions-with-multiple-products) の場合は、増分または減分する数量の価格の ID を 2 番目の引数として増分 / 減分メソッドに渡す必要があります。

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
<!-- ### Subscriptions With Multiple Products -->
### Subscriptions With Multiple Products

<!-- [Subscription with multiple products](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons) allow you to assign multiple billing products to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on product for an additional $15 per month. -->
[Subscription with multiple products](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons) を使用すると、複数の課金製品を 1 つのサブスクリプションに割り当てることができます。たとえば、基本サブスクリプション価格が月額 10 ドルであるが、月額 15 ドルの追加料金でライブ チャット アドオン製品を提供するカスタマー サービスの「ヘルプデスク」アプリケーションを構築していると想像してください。

<!-- When creating subscription checkout sessions, you may specify multiple products for a given subscription by passing an array of prices as the first argument to the `subscribe` method: -->
サブスクリプション チェックアウト セッションを作成するとき、価格の配列を最初の引数として `subscribe` メソッドに渡すことで、特定のサブスクリプションに複数の製品を指定できます。

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe([
        'price_monthly',
        'price_chat',
    ]);

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- In the example above, the customer will have two prices attached to their `default` subscription. Both prices will be charged on their respective billing intervals. If necessary, you may pass an associative array of key / value pairs to indicate a specific quantity for each price: -->
上の例では、顧客は `default` サブスクリプションに 2 つの価格を設定します。どちらの価格も、それぞれの請求間隔で請求されます。必要に応じて、キーと値のペアの連想配列を渡して、各価格の特定の数量を示すことができます。

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

<!-- If you would like to add another price to an existing subscription, you must use the subscription's `swap` method. When invoking the `swap` method, you should also include the subscription's current prices and quantities as well: -->
既存のサブスクリプションに別の価格を追加する場合は、サブスクリプションの `swap` メソッドを使用する必要があります。 `swap` メソッドを呼び出すときは、サブスクリプションの現在の価格と数量も含める必要があります。

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

<!-- The example above will add the new price, but the customer will not be billed for it until their next billing cycle. If you would like to bill the customer immediately you may use the `swapAndInvoice` method: -->
上の例では新しい価格が追加されますが、顧客には次の請求サイクルまで請求されません。顧客にすぐに請求したい場合は、`swapAndInvoice` メソッドを使用できます。

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

<!-- You may remove prices from subscriptions using the `swap` method and omitting the price you want to remove: -->
`swap` メソッドを使用し、削除する価格を省略して、サブスクリプションから価格を削除できます。

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> サブスクリプションの最後の価格を削除することはできません。代わりに、サブスクリプションをキャンセルするだけです。

<a name="multiple-subscriptions"></a>
<!-- ### Multiple Subscriptions -->
### Multiple Subscriptions

<!-- Paddle allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans. -->
Paddle を使用すると、顧客は同時に複数のサブスクリプションを持つことができます。たとえば、水泳のサブスクリプションとウェイトリフティングのサブスクリプションを提供するジムを運営しており、各サブスクリプションの価格が異なる場合があります。もちろん、顧客はどちらかまたは両方のプランに加入できる必要があります。

<!-- When your application creates subscriptions, you may provide the type of the subscription to the `subscribe` method as the second argument. The type may be any string that represents the type of subscription the user is initiating: -->
アプリケーションがサブスクリプションを作成するとき、2 番目の引数として `subscribe` メソッドにサブスクリプションのタイプを指定できます。タイプには、ユーザーが開始しているサブスクリプションのタイプを表す任意の文字列を指定できます。

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- In this example, we initiated a monthly swimming subscription for the customer. However, they may want to swap to a yearly subscription at a later time. When adjusting the customer's subscription, we can simply swap the price on the `swimming` subscription: -->
この例では、顧客に対して毎月の水泳サブスクリプションを開始しました。ただし、後で年間サブスクリプションに切り替えたい場合もあります。顧客のサブスクリプションを調整するときは、`swimming` サブスクリプションの価格を単純に交換できます。

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

<!-- Of course, you may also cancel the subscription entirely: -->
もちろん、サブスクリプションを完全にキャンセルすることもできます。

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
<!-- ### Pausing Subscriptions -->
### Pausing Subscriptions

<!-- To pause a subscription, call the `pause` method on the user's subscription: -->
サブスクリプションを一時停止するには、ユーザーのサブスクリプションで `pause` メソッドを呼び出します。

```php
$user->subscription()->pause();
```

<!-- When a subscription is paused, Cashier will automatically set the `paused_at` column in your database. This column is used to determine when the `paused` method should begin returning `true`. For example, if a customer pauses a subscription on March 1st, but the subscription was not scheduled to recur until March 5th, the `paused` method will continue to return `false` until March 5th. This is because a user is typically allowed to continue using an application until the end of their billing cycle. -->
サブスクリプションが一時停止されると、Cashier はデータベースに `paused_at` 列を自動的に設定します。この列は、`paused` メソッドが `true` を返し始める時期を決定するために使用されます。たとえば、顧客が 3 月 1 日にサブスクリプションを一時停止したが、そのサブスクリプションが 3 月 5 日まで繰り返されるようにスケジュールされていなかった場合、`paused` メソッドは 3 月 5 日まで `false` を返し続けます。これは、通常、ユーザーは請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているためです。

<!-- By default, pausing happens at the next billing interval so the customer can use the remainder of the period they paid for. If you want to pause a subscription immediately, you may use the `pauseNow` method: -->
デフォルトでは、次の請求間隔で一時停止が行われるため、顧客は支払った期間の残りを使用できます。サブスクリプションをすぐに一時停止したい場合は、`pauseNow` メソッドを使用できます。

```php
$user->subscription()->pauseNow();
```

<!-- Using the `pauseUntil` method, you can pause the subscription until a specific moment in time: -->
`pauseUntil` メソッドを使用すると、特定の時点までサブスクリプションを一時停止できます。

```php
$user->subscription()->pauseUntil(now()->plus(months: 1));
```

<!-- Or, you may use the `pauseNowUntil` method to immediately pause the subscription until a given point in time: -->
または、`pauseNowUntil` メソッドを使用して、特定の時点までサブスクリプションをすぐに一時停止することもできます。

```php
$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```

<!-- You may determine if a user has paused their subscription but are still on their "grace period" using the `onPausedGracePeriod` method: -->
ユーザーがサブスクリプションを一時停止しているが、まだ「猶予期間」中であるかどうかを、`onPausedGracePeriod` メソッドを使用して判断できます。

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

<!-- To resume a paused subscription, you may invoke the `resume` method on the subscription: -->
一時停止したサブスクリプションを再開するには、サブスクリプションで `resume` メソッドを呼び出すことができます。

```php
$user->subscription()->resume();
```

> [!WARNING]
> 一時停止中はサブスクリプションを変更できません。別のプランに切り替えたり、数量を更新したりする場合は、まずサブスクリプションを再開する必要があります。

<a name="canceling-subscriptions"></a>
<!-- ### Canceling Subscriptions -->
### Canceling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
サブスクリプションをキャンセルするには、ユーザーのサブスクリプションで `cancel` メソッドを呼び出します。

```php
$user->subscription()->cancel();
```

<!-- When a subscription is canceled, Cashier will automatically set the `ends_at` column in your database. This column is used to determine when the `subscribed` method should begin returning `false`. For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
サブスクリプションがキャンセルされると、Cashier はデータベースに `ends_at` 列を自動的に設定します。この列は、`subscribed` メソッドが `false` を返し始める時期を決定するために使用されます。たとえば、顧客が 3 月 1 日にサブスクリプションをキャンセルしたが、そのサブスクリプションが 3 月 5 日まで終了する予定ではなかった場合、`subscribed` メソッドは 3 月 5 日まで `true` を返し続けます。これは、ユーザーが通常、請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているために行われます。

<!-- You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
`onGracePeriod` メソッドを使用して、ユーザーがサブスクリプションをキャンセルしたがまだ「猶予期間」中であるかどうかを確認できます。

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<!-- If you wish to cancel a subscription immediately, you may call the `cancelNow` method on the subscription: -->
サブスクリプションをすぐにキャンセルしたい場合は、サブスクリプションで `cancelNow` メソッドを呼び出すことができます。

```php
$user->subscription()->cancelNow();
```

<!-- To stop a subscription on its grace period from canceling, you may invoke the `stopCancelation` method: -->
猶予期間中のサブスクリプションのキャンセルを停止するには、`stopCancelation` メソッドを呼び出します。

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle のサブスクリプションは、キャンセル後に再開することはできません。顧客がサブスクリプションの再開を希望する場合は、新しいサブスクリプションを作成する必要があります。

<a name="subscription-trials"></a>
<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>
<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use set a trial time in the Paddle dashboard on the price your customer is subscribing to. Then, initiate the checkout session as normal: -->
支払い方法情報を事前に収集しながら顧客に試用期間を提供したい場合は、顧客が購読している価格に応じて Paddle ダッシュボードで試用期間を設定する必要があります。次に、通常どおりチェックアウト セッションを開始します。

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- When your application receives the `subscription_created` event, Cashier will set the trial period ending date on the subscription record within your application's database as well as instruct Paddle to not begin billing the customer until after this date. -->
アプリケーションが `subscription_created` イベントを受信すると、Cashier はアプリケーションのデータベース内のサブスクリプション レコードに試用期間の終了日を設定し、この日付以降になるまで顧客への請求を開始しないように Paddle に指示します。

> [!WARNING]
> 試用期間の終了日までに顧客のサブスクリプションがキャンセルされなかった場合、試用期間が終了するとすぐに料金が請求されるため、ユーザーに試用期間の終了日を必ず通知する必要があります。

<!-- You may determine if the user is within their trial period using either the `onTrial` method of the user instance: -->
ユーザー インスタンスの `onTrial` メソッドのいずれかを使用して、ユーザーが試用期間内かどうかを判断できます。

```php
if ($user->onTrial()) {
    // ...
}
```

<!-- To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods: -->
既存の試用版の有効期限が切れているかどうかを確認するには、`hasExpiredTrial` メソッドを使用できます。

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

<!-- To determine if a user is on trial for a specific subscription type, you may provide the type to the `onTrial` or `hasExpiredTrial` methods: -->
ユーザーが特定のサブスクリプション タイプの試用中かどうかを判断するには、そのタイプを `onTrial` メソッドまたは `hasExpiredTrial` メソッドに指定できます。

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the customer record attached to your user to your desired trial ending date. This is typically done during user registration: -->
ユーザーの支払い方法情報を事前に収集せずに試用期間を提供したい場合は、ユーザーに添付されている顧客レコードの `trial_ends_at` 列を希望する試用終了日に設定できます。これは通常、ユーザー登録時に行われます。

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->plus(days: 10)
]);
```

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the `User` instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
既存のサブスクリプションに関連付けられていないため、Cashier はこのタイプのトライアルを「一般トライアル」と呼びます。現在の日付が `trial_ends_at` の値を超えていない場合、`User` インスタンスの `onTrial` メソッドは `true` を返します。

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `subscribe` method as usual: -->
ユーザーの実際のサブスクリプションを作成する準備ができたら、通常どおり `subscribe` メソッドを使用できます。

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription type parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
ユーザーの試用終了日を取得するには、`trialEndsAt` メソッドを使用できます。このメソッドは、ユーザーが試用中の場合は Carbon date インスタンスを返し、試用中でない場合は `null` を返します。デフォルト以外の特定のサブスクリプションの試用終了日を取得したい場合は、オプションのサブスクリプション タイプ パラメーターを渡すこともできます。

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

<!-- You may use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not created an actual subscription yet: -->
ユーザーが「一般的な」試用期間内であり、実際のサブスクリプションをまだ作成していないことを具体的に知りたい場合は、`onGenericTrial` メソッドを使用できます。

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extend-or-activate-a-trial"></a>
<!-- ### Extend or Activate a Trial -->
### Extend or Activate a Trial

<!-- You can extend an existing trial period on a subscription by invoking the `extendTrial` method and specifying the moment in time that the trial should end: -->
`extendTrial` メソッドを呼び出し、トライアルを終了する時点を指定することで、サブスクリプションの既存のトライアル期間を延長できます。

```php
$user->subscription()->extendTrial(now()->plus(days: 5));
```

<!-- Or, you may immediately activate a subscription by ending its trial by calling the `activate` method on the subscription: -->
または、サブスクリプションで `activate` メソッドを呼び出してトライアルを終了し、サブスクリプションをすぐにアクティブ化することもできます。

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
<!-- ## Handling Paddle Webhooks -->
## Handling Paddle Webhooks

<!-- Paddle can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Paddle は、Webhook 経由でさまざまなイベントをアプリケーションに通知できます。デフォルトでは、Cashier の Webhook コントローラを指すルートが Cashier サービスプロバイダによって登録されます。このコントローラは、受信したすべての Webhook リクエストを処理します。

<!-- By default, this controller will automatically handle canceling subscriptions that have too many failed charges, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Paddle webhook event you like. -->
デフォルトでは、このコントローラは、請求失敗が多すぎるサブスクリプションのキャンセル、サブスクリプションの更新、支払い方法の変更を自動的に処理します。ただし、すぐにわかりますが、このコントローラを拡張して、任意の Paddle Webhook イベントを処理できます。

<!-- To ensure your application can handle Paddle webhooks, be sure to [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/notifications-v2). By default, Cashier's webhook controller responds to the `/paddle/webhook` URL path. The full list of all webhooks you should enable in the Paddle control panel are: -->
アプリケーションが Paddle Webhook を処理できることを確認するには、必ず [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/notifications-v2) を実行してください。デフォルトでは、Cashier の Webhook コントローラは `/paddle/webhook` URL パスに応答します。Paddle コントロール パネルで有効にする必要があるすべての Webhook の完全なリストは次のとおりです。

<!--
- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled
-->
- 顧客が更新しました
- 取引完了
- トランザクションが更新されました
- サブスクリプションが作成されました
- サブスクリプションが更新されました
- サブスクリプションが一時停止されました
- サブスクリプションがキャンセルされました

> [!WARNING]
> Cashier に含まれる [webhook signature verification](/docs/13.x/cashier-paddle#verifying-webhook-signatures) ミドルウェアを使用して、受信リクエストを必ず保護してください。

<a name="webhooks-csrf-protection"></a>
<!-- #### Webhooks and CSRF Protection -->
#### Webhooks and CSRF Protection

<!-- Since Paddle webhooks need to bypass Laravel's [CSRF protection](/docs/13.x/csrf), you should ensure that Laravel does not attempt to verify the CSRF token for incoming Paddle webhooks. To accomplish this, you should exclude `paddle/*` from CSRF protection in your application's `bootstrap/app.php` file: -->
Paddle Webhook は Laravel の [CSRF protection](/docs/13.x/csrf) をバイパスする必要があるため、Laravel が受信 Paddle Webhook の CSRF トークンを検証しようとしないようにする必要があります。これを実現するには、アプリケーションの `bootstrap/app.php` ファイルで CSRF 保護から `paddle/*` を除外する必要があります。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
<!-- #### Webhooks and Local Development -->
#### Webhooks and Local Development

<!-- For Paddle to be able to send your application webhooks during local development, you will need to expose your application via a site sharing service such as [Ngrok](https://ngrok.com/) or [Expose](https://expose.dev/docs/introduction). If you are developing your application locally using [Laravel Sail](/docs/13.x/sail), you may use Sail's [site sharing command](/docs/13.x/sail#sharing-your-site). -->
Paddle がローカル開発中にアプリケーション Webhook を送信できるようにするには、[Ngrok](https://ngrok.com/) や [Expose](https://expose.dev/docs/introduction) などのサイト共有サービスを介してアプリケーションを公開する必要があります。 [Laravel Sail](/docs/13.x/sail) を使用してアプリケーションをローカルで開発している場合は、Sail の [site sharing command](/docs/13.x/sail#sharing-your-site) を使用できます。

<a name="defining-webhook-event-handlers"></a>
<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancelation on failed charges and other common Paddle webhooks. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier は、失敗した請求やその他の一般的な Paddle Webhook によるサブスクリプションのキャンセルを自動的に処理します。ただし、追加の Webhook イベントを処理したい場合は、Cashier によって送出される次のイベントをリッスンすることで処理できます。

<!--
- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`
-->
- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

<!-- Both events contain the full payload of the Paddle webhook. For example, if you wish to handle the `transaction.billed` webhook, you may register a [listener](/docs/13.x/events#defining-listeners) that will handle the event: -->
どちらのイベントにも、Paddle Webhook の完全なペイロードが含まれています。たとえば、`transaction.billed` Webhook を処理したい場合は、イベントを処理する [listener](/docs/13.x/events#defining-listeners) を登録できます。

```php
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Handle received Paddle webhooks.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['event_type'] === 'transaction.billed') {
            // Handle the incoming event...
        }
    }
}
```

<!-- Cashier also emit events dedicated to the type of the received webhook. In addition to the full payload from Paddle, they also contain the relevant models that were used to process the webhook such as the billable model, the subscription, or the receipt: -->
Cashier は、受信した Webhook のタイプ専用のイベントも発行します。 Paddle からの完全なペイロードに加えて、請求可能なモデル、サブスクリプション、レシートなど、Webhook の処理に使用された関連モデルも含まれています。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`
-->
- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

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

<!-- To secure your webhooks, you may use [Paddle's webhook signatures](https://developer.paddle.com/webhooks/signature-verification). For convenience, Cashier automatically includes a middleware which validates that the incoming Paddle webhook request is valid. -->
Webhook を保護するには、[Paddle's webhook signatures](https://developer.paddle.com/webhooks/signature-verification) を使用できます。便宜上、Cashier には、受信した Paddle Webhook リクエストが有効であることを検証するミドルウェアが自動的に組み込まれています。

<!-- To enable webhook verification, ensure that the `PADDLE_WEBHOOK_SECRET` environment variable is defined in your application's `.env` file. The webhook secret may be retrieved from your Paddle account dashboard. -->
Webhook 検証を有効にするには、`PADDLE_WEBHOOK_SECRET` 環境変数がアプリケーションの `.env` ファイルで定義されていることを確認してください。 Webhook シークレットは、Paddle アカウントのダッシュボードから取得できます。

<a name="single-charges"></a>
<!-- ## Single Charges -->
## Single Charges

<a name="charging-for-products"></a>
<!-- ### Charging for Products -->
### Charging for Products

<!-- If you would like to initiate a product purchase for a customer, you may use the `checkout` method on a billable model instance to generate a checkout session for the purchase. The `checkout` method accepts one or multiple price ID's. If necessary, an associative array may be used to provide the quantity of the product that is being purchased: -->
顧客のために製品の購入を開始したい場合は、請求可能モデル インスタンスで `checkout` メソッドを使用して、購入のためのチェックアウト セッションを生成できます。 `checkout` メソッドは、1 つまたは複数の価格 ID を受け入れます。必要に応じて、連想配列を使用して、購入される製品の数量を提供することもできます。

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

<!-- After generating the checkout session, you may use Cashier's provided `paddle-button` [Blade component](#overlay-checkout) to allow the user to view the Paddle checkout widget and complete the purchase: -->
チェックアウト セッションを生成した後、Cashierが提供する `paddle-button` [Blade component](#overlay-checkout) を使用して、ユーザーがPaddle チェックアウト ウィジェットを表示して購入を完了できるようにすることができます。

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

<!-- A checkout session has a `customData` method, allowing you to pass any custom data you wish to the underlying transaction creation. Please consult [the Paddle documentation](https://developer.paddle.com/build/transactions/custom-data) to learn more about the options available to you when passing custom data: -->
チェックアウト セッションには `customData` メソッドがあり、必要なカスタム データを基になるトランザクション作成に渡すことができます。カスタム データを渡すときに利用できるオプションの詳細については、[the Paddle documentation](https://developer.paddle.com/build/transactions/custom-data) を参照してください。

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
<!-- ### Refunding Transactions -->
### Refunding Transactions

<!-- Refunding transactions will return the refunded amount to your customer's payment method that was used at the time of purchase. If you need to refund a Paddle purchase, you may use the `refund` method on a `Cashier\Paddle\Transaction` model. This method accepts a reason as the first argument, one or more price ID's to refund with optional amounts as an associative array. You may retrieve the transactions for a given billable model using the `transactions` method. -->
返金取引では、購入時に使用された顧客の支払い方法に返金金額が返されます。 Paddle の購入を返金する必要がある場合は、`Cashier\Paddle\Transaction` モデルで `refund` メソッドを使用できます。このメソッドは、最初の引数として理由を受け入れ、オプションの金額を連想配列として返金する 1 つ以上の価格 ID を受け取ります。 `transactions` メソッドを使用して、特定の請求可能モデルのトランザクションを取得できます。

<!-- For example, imagine we want to refund a specific transaction for prices `pri_123` and `pri_456`. We want to fully refund `pri_123`, but only refund two dollars for `pri_456`: -->
たとえば、価格 `pri_123` および `pri_456` の特定のトランザクションを返金したいとします。 `pri_123` は全額返金したいのですが、`pri_456` については 2 ドルのみ返金したいと考えています。

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // Fully refund this price...
    'pri_456' => 200, // Only partially refund this price...
]);
```

<!-- The example above refunds specific line items in a transaction. If you want to refund the entire transaction, simply provide a reason: -->
上の例では、トランザクション内の特定の項目を返金します。取引全体を返金したい場合は、理由を入力してください。

```php
$response = $transaction->refund('Accidental charge');
```

<!-- For more information on refunds, please consult [Paddle's refund documentation](https://developer.paddle.com/build/transactions/create-transaction-adjustments). -->
払い戻しの詳細については、[Paddle's refund documentation](https://developer.paddle.com/build/transactions/create-transaction-adjustments) にお問い合わせください。

> [!WARNING]
> 返金は完全に処理される前に必ず Paddle の承認を受ける必要があります。

<a name="crediting-transactions"></a>
<!-- ### Crediting Transactions -->
### Crediting Transactions

<!-- Just like refunding, you can also credit transactions. Crediting transactions will add the funds to the customer's balance so it may be used for future purchases. Crediting transactions can only be done for manually-collected transactions and not for automatically-collected transactions (like subscriptions) since Paddle handles subscription credits automatically: -->
払い戻しと同様に、トランザクションをクレジット処理することもできます。トランザクションをクレジットすると、資金が顧客の残高に追加され、将来の購入に使用できるようになります。 Paddle はサブスクリプション クレジットを自動的に処理するため、トランザクションのクレジット付与は手動で収集されたトランザクションに対してのみ実行でき、自動収集されたトランザクション (サブスクリプションなど) に対しては実行できません。

```php
$transaction = $user->transactions()->first();

// Credit a specific line item fully...
$response = $transaction->credit('Compensation', 'pri_123');
```

<!-- For more info, [see Paddle's documentation on crediting](https://developer.paddle.com/build/transactions/create-transaction-adjustments). -->
詳細については、[see Paddle's documentation on crediting](https://developer.paddle.com/build/transactions/create-transaction-adjustments) をご覧ください。

> [!WARNING]
> クレジットは手動で収集されたトランザクションにのみ適用できます。自動的に収集されたトランザクションは、Paddle 自体によって入金されます。

<a name="transactions"></a>
<!-- ## Transactions -->
## Transactions

<!-- You may easily retrieve an array of a billable model's transactions via the `transactions` property: -->
`transactions` プロパティを使用して、請求可能なモデルのトランザクションの配列を簡単に取得できます。

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

<!-- Transactions represent payments for your products and purchases and are accompanied by invoices. Only completed transactions are stored in your application's database. -->
トランザクションは製品と購入の支払いを表し、請求書が添付されます。完了したトランザクションのみがアプリケーションのデータベースに保存されます。

<!-- When listing the transactions for a customer, you may use the transaction instance's methods to display the relevant payment information. For example, you may wish to list every transaction in a table, allowing the user to easily download any of the invoices: -->
顧客のトランザクションをリストする場合、トランザクション インスタンスのメソッドを使用して、関連する支払い情報を表示できます。たとえば、すべての取引を表にリストして、ユーザーが任意の請求書を簡単にダウンロードできるようにしたい場合があります。

```html
<table>
    @foreach ($transactions as $transaction)
        <tr>
            <td>{{ $transaction->billed_at->toFormattedDateString() }}</td>
            <td>{{ $transaction->total() }}</td>
            <td>{{ $transaction->tax() }}</td>
            <td><a href="{{ route('download-invoice', $transaction->id) }}" target="_blank">Download</a></td>
        </tr>
    @endforeach
</table>
```

<!-- The `download-invoice` route may look like the following: -->
`download-invoice` ルートは次のようになります。

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
<!-- ### Past and Upcoming Payments -->
### Past and Upcoming Payments

<!-- You may use the `lastPayment` and `nextPayment` methods to retrieve and display a customer's past or upcoming payments for recurring subscriptions: -->
`lastPayment` メソッドと `nextPayment` メソッドを使用して、定期購読に対する顧客の過去または今後の支払いを取得して表示できます。

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

<!-- Both of these methods will return an instance of `Laravel\Paddle\Payment`; however, `lastPayment` will return `null` when transactions have not been synced by webhooks yet, while `nextPayment` will return `null` when the billing cycle has ended (such as when a subscription has been canceled): -->
これらのメソッドは両方とも、`Laravel\Paddle\Payment` のインスタンスを返します。ただし、トランザクションが Webhook によってまだ同期されていない場合、`lastPayment` は `null` を返しますが、請求サイクルが終了した場合 (サブスクリプションがキャンセルされた場合など)、`nextPayment` は `null` を返します。

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- While testing, you should manually test your billing flow to make sure your integration works as expected. -->
テスト中に、請求フローを手動でテストして、統合が期待どおりに機能することを確認する必要があります。

<!-- For automated tests, including those executed within a CI environment, you may use [Laravel's HTTP Client](/docs/13.x/http-client#testing) to fake HTTP calls made to Paddle. Although this does not test the actual responses from Paddle, it does provide a way to test your application without actually calling Paddle's API. -->
CI 環境内で実行されるテストを含む自動テストの場合、[Laravel's HTTP Client](/docs/13.x/http-client#testing) を使用して Paddle に対して行われた HTTP 呼び出しを偽装できます。これは Paddle からの実際の応答をテストしませんが、実際に Paddle の API を呼び出さずにアプリケーションをテストする方法を提供します。
