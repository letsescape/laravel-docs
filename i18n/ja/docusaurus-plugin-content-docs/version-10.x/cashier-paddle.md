# Laravel Cashier (Paddle) (Laravel Cashier (Paddle))

- [Introduction](#introduction)
- [Cashierのアップグレード](#upgrading-cashier)
- [Installation](#installation)
    - [Paddle サンドボックス](#paddle-sandbox)
- [Configuration](#configuration)
    - [課金対象モデル](#billable-model)
    - [APIキー](#api-keys)
    - [Paddle.js](#paddle-js)
    - [通貨構成](#currency-configuration)
    - [デフォルトモデルの上書き](#overriding-default-models)
- [Quickstart](#quickstart)
    - [製品の販売](#quickstart-selling-products)
    - [サブスクリプションの販売](#quickstart-selling-subscriptions)
- [チェックアウトセッション](#checkout-sessions)
    - [オーバーレイチェックアウト](#overlay-checkout)
    - [インラインチェックアウト](#inline-checkout)
    - [ゲストのチェックアウト](#guest-checkouts)
- [価格プレビュー](#price-previews)
    - [顧客価格プレビュー](#customer-price-previews)
    - [Discounts](#price-discounts)
- [Customers](#customers)
    - [顧客のデフォルト](#customer-defaults)
    - [顧客の取得](#retrieving-customers)
    - [顧客の創造](#creating-customers)
- [Subscriptions](#subscriptions)
    - [サブスクリプションの作成](#creating-subscriptions)
    - [購読ステータスの確認](#checking-subscription-status)
    - [サブスクリプションの単一料金](#subscription-single-charges)
    - [支払い情報の更新](#updating-payment-information)
    - [プランの変更](#changing-plans)
    - [購読数量](#subscription-quantity)
    - [複数の製品のサブスクリプション](#subscriptions-with-multiple-products)
    - [複数のサブスクリプション](#multiple-subscriptions)
    - [サブスクリプションの一時停止](#pausing-subscriptions)
    - [定期購入のキャンセル](#canceling-subscriptions)
- [サブスクリプショントライアル](#subscription-trials)
    - [支払い方法を前払いする場合](#with-payment-method-up-front)
    - [前払いの支払い方法なし](#without-payment-method-up-front)
    - [トライアルを延長またはアクティブ化する](#extend-or-activate-a-trial)
- [Paddle Webhook の処理](#handling-paddle-webhooks)
    - [Webhook イベント ハンドラーの定義](#defining-webhook-event-handlers)
    - [Webhook 署名の検証](#verifying-webhook-signatures)
- [シングルチャージ](#single-charges)
    - [製品の課金](#charging-for-products)
    - [返金取引](#refunding-transactions)
    - [クレジット取引](#crediting-transactions)
- [Transactions](#transactions)
    - [過去および今後の支払い](#past-and-upcoming-payments)
- [Testing](#testing)

<a name="introduction"></a>
## 導入 (Introduction)

> [!WARNING]  
> このドキュメントは、Cashier Paddle 2.x と Paddle Billing の統合に関するものです。まだ Paddle Classic を使用している場合は、[Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x) を使用する必要があります。

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) は、[Paddle の](https://paddle.com) サブスクリプション請求サービスへの表現力豊かで流暢なインターフェイスを提供します。あなたが恐れている定型的なサブスクリプション請求コードのほぼすべてを処理します。基本的なサブスクリプション管理に加えて、Cashier はサブスクリプションの交換、サブスクリプションの「数量」、サブスクリプションの一時停止、キャンセルの猶予期間などを処理できます。

Cashier Paddle について詳しく説明する前に、Paddle の [コンセプトガイド](https://developer.paddle.com/concepts/overview) と [APIドキュメント](https://developer.paddle.com/api-reference/overview) も確認することをお勧めします。

<a name="upgrading-cashier"></a>
## Cashierのアップグレード (Upgrading Cashier)

Cashier の新しいバージョンにアップグレードする場合は、[アップグレードガイド](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを使用して Paddle の Cashier パッケージをインストールします。

```shell
composer require laravel/cashier-paddle
```

次に、`vendor:publish` Artisan コマンドを使用して、Cashier 移行ファイルを公開する必要があります。

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

次に、アプリケーションのデータベース移行を実行する必要があります。 Cashier の移行により、新しい `customers` テーブルが作成されます。さらに、顧客のすべてのサブスクリプションを保存するために、新しい `subscriptions` テーブルと `subscription_items` テーブルが作成されます。最後に、顧客に関連付けられたすべての Paddle トランザクションを保存するための新しい `transactions` テーブルが作成されます。

```shell
php artisan migrate
```

> [!WARNING]  
> Cashier がすべての Paddle イベントを適切に処理できるようにするには、[Cashier の Webhook 処理を設定する](#handling-paddle-webhooks) を忘れないでください。

<a name="paddle-sandbox"></a>
### Paddle サンドボックス

ローカルおよびステージング開発中は、[Paddle Sandbox アカウントを登録する](https://sandbox-login.paddle.com/signup) を実行する必要があります。このアカウントでは、実際に支払いを行わずにアプリケーションのテストと開発を行うためのサンドボックス環境が提供されます。 Paddle の [テストカード番号](https://developer.paddle.com/concepts/payment-methods/credit-debit-card) を使用して、さまざまな支払いシナリオをシミュレートできます。

Paddle Sandbox 環境を使用する場合は、アプリケーションの `.env` ファイル内で `PADDLE_SANDBOX` 環境変数を `true` に設定する必要があります。

```ini
PADDLE_SANDBOX=true
```

アプリケーションの開発が完了したら、[Paddle ベンダー アカウントを申請する](https://paddle.com) を実行できます。アプリケーションを運用環境に導入する前に、Paddle はアプリケーションのドメインを承認する必要があります。

<a name="configuration"></a>
## 構成 (Configuration)

<a name="billable-model"></a>
### 課金対象モデル

Cashier を使用する前に、`Billable` 特性をユーザー モデル定義に追加する必要があります。この特性は、サブスクリプションの作成や支払い方法情報の更新など、一般的な請求タスクを実行できるようにするさまざまなメソッドを提供します。

    use Laravel\Paddle\Billable;

    class User extends Authenticatable
    {
        use Billable;
    }

ユーザーではない請求可能なエンティティがある場合は、それらのクラスに特性を追加することもできます。

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Paddle\Billable;

    class Team extends Model
    {
        use Billable;
    }

<a name="api-keys"></a>
### APIキー

次に、アプリケーションの `.env` ファイルでPaddle キーを構成する必要があります。 Paddle コントロール パネルから Paddle API キーを取得できます。

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

[Paddle のサンドボックス環境](#paddle-sandbox) を使用する場合は、`PADDLE_SANDBOX` 環境変数を `true` に設定する必要があります。アプリケーションを運用環境にデプロイし、Paddle のライブ ベンダー環境を使用している場合は、`PADDLE_SANDBOX` 変数を `false` に設定する必要があります。

`PADDLE_RETAIN_KEY` はオプションであり、[Retain](https://developer.paddle.com/paddlejs/retain) で Paddle を使用している場合にのみ設定する必要があります。

<a name="paddle-js"></a>
### Paddle.js

Paddle は、独自の JavaScript ライブラリを利用して Paddle チェックアウト ウィジェットを開始します。アプリケーション レイアウトの `</head>` 終了タグの直前に `@paddleJS` Blade ディレクティブを配置することで、JavaScript ライブラリをロードできます。

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 通貨構成

請求書に表示する金額の書式を設定するときに使用するロケールを指定できます。内部的には、Cashier は [PHPの`NumberFormatter`クラス](https://www.php.net/manual/en/class.numberformatter.php) クラスを使用して通貨ロケールを設定します。

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]  
> `en` 以外のロケールを使用するには、`ext-intl` PHP 拡張機能がサーバーにインストールされ、構成されていることを確認してください。

<a name="overriding-default-models"></a>
### デフォルトモデルの上書き

独自のモデルを定義し、対応する Cashier モデルを拡張することで、Cashier によって内部的に使用されるモデルを自由に拡張できます。

    use Laravel\Paddle\Subscription as CashierSubscription;

    class Subscription extends CashierSubscription
    {
        // ...
    }

モデルを定義した後、`Laravel\Paddle\Cashier` クラスを介してカスタム モデルを使用するように Cashier に指示できます。通常、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドでカスタム モデルについて Cashier に通知する必要があります。

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

<a name="quickstart"></a>
## クイックスタート (Quickstart)

<a name="quickstart-selling-products"></a>
### 製品の販売

> [!NOTE]
> Paddle Checkout を利用する前に、Paddle ダッシュボードで固定価格の製品を定義する必要があります。さらに、[Paddle の Webhook 処理を構成する](#handling-paddle-webhooks) を実行する必要があります。

アプリケーション経由で製品やサブスクリプションの請求を行うのは、威圧的な場合があります。ただし、Cashier と [Paddle のチェックアウト オーバーレイ](https://www.paddle.com/billing/checkout) のおかげで、最新の堅牢な支払い統合を簡単に構築できます。

非定期的な 1 回限りの製品に対して顧客に請求するには、Cashier を利用して顧客に Paddle の Checkout Overlay を請求します。顧客はそこで支払いの詳細を提供し、購入を確認します。チェックアウト オーバーレイ経由で支払いが完了すると、顧客はアプリケーション内で選択した成功 URL にリダイレクトされます。

    use Illuminate\Http\Request;

    Route::get('/buy', function (Request $request) {
        $checkout = $request->user()->checkout('pri_deluxe_album')
            ->returnTo(route('dashboard'));

        return view('buy', ['checkout' => $checkout]);
    })->name('checkout');

上の例でわかるように、Cashierが提供する `checkout` メソッドを利用して、特定の「価格識別子」のPaddle チェックアウト オーバーレイを顧客に提示するチェックアウト オブジェクトを作成します。 Paddle を使用する場合、「価格」は [特定の製品に対して定義された価格](https://developer.paddle.com/build/products/create-products-prices) を指します。

必要に応じて、`checkout` メソッドは Paddle に顧客を自動的に作成し、その Paddle 顧客レコードをアプリケーションのデータベース内の対応するユーザーに接続します。チェックアウト セッションが完了すると、顧客は専用の成功ページにリダイレクトされ、そこで顧客に情報メッセージを表示できます。

`buy` ビューには、チェックアウト オーバーレイを表示するボタンが含まれます。 `paddle-button` Blade コンポーネントは Cashier Paddle に含まれています。ただし、[オーバーレイ チェックアウトを手動でレンダリングする](#manually-rendering-an-overlay-checkout) を実行することもできます。

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle チェックアウトへのメタデータの提供

製品を販売する場合、独自のアプリケーションで定義された `Cart` および `Order` モデルを介して、完了した注文と購入した製品を追跡するのが一般的です。購入を完了するために顧客を Paddle の Checkout Overlay にリダイレクトする場合、顧客がアプリケーションにリダイレクトされたときに完了した購入を対応する注文に関連付けることができるように、既存の注文 ID を提供する必要がある場合があります。

これを実現するには、カスタム データの配列を `checkout` メソッドに提供します。ユーザーがチェックアウトプロセスを開始したときに、アプリケーション内で保留中の `Order` が作成されると想像してみましょう。この例の `Cart` モデルと `Order` モデルは説明用であり、Cashier によって提供されるものではないことに注意してください。独自のアプリケーションのニーズに基づいて、これらの概念を自由に実装できます。
    
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

上の例でわかるように、ユーザーがチェックアウト プロセスを開始すると、カート/注文に関連付けられたすべてのPaddle 価格識別子が `checkout` メソッドに提供されます。もちろん、アプリケーションは、顧客がこれらの商品を追加したときに、これらの商品を「ショッピング カート」または注文に関連付ける責任があります。また、`customData` メソッドを介して注文の ID をPaddle チェックアウト オーバーレイに提供します。

もちろん、顧客がチェックアウトプロセスを完了したら、注文を「完了」としてマークすることもできます。これを実現するには、Paddle によってディスパッチされ、Cashier によってイベント経由で発生した Webhook をリッスンして、注文情報をデータベースに保存します。

まず、Cashier によって送出される `TransactionCompleted` イベントをリッスンします。通常、アプリケーションのサービスプロバイダの 1 つの `boot` メソッドにイベント リスナを登録する必要があります。

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

この例では、`CompleteOrder` リスナは次のようになります。

    namespace App\Listeners;

    use App\Models\Order;
    use Laravel\Cashier\Cashier;
    use Laravel\Cashier\Events\TransactionCompleted;

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

[`transaction.completed` イベントに含まれるデータ](https://developer.paddle.com/webhooks/transactions/transaction-completed) の詳細については、Paddle のドキュメントを参照してください。

<a name="quickstart-selling-subscriptions"></a>
### サブスクリプションの販売

> [!NOTE]  
> Paddle Checkout を利用する前に、Paddle ダッシュボードで固定価格の製品を定義する必要があります。さらに、[Paddle の Webhook 処理を構成する](#handling-paddle-webhooks) を実行する必要があります。

アプリケーション経由で製品やサブスクリプションの請求を行うのは、威圧的な場合があります。ただし、Cashier と [Paddle のチェックアウト オーバーレイ](https://www.paddle.com/billing/checkout) のおかげで、最新の堅牢な支払い統合を簡単に構築できます。

Cashier と Paddle の Checkout Overlay を使用してサブスクリプションを販売する方法を学ぶために、基本的な月次 (`price_basic_monthly`) および年次 (`price_basic_yearly`) プランを持つサブスクリプション サービスの簡単なシナリオを考えてみましょう。これら 2 つの価格は、Paddle ダッシュボードの「Basic」製品 (`pro_basic`) にグループ化できます。さらに、当社のサブスクリプション サービスでは、`pro_expert` としてエキスパート プランを提供する場合があります。

まず、顧客がサービスに登録する方法を見てみましょう。もちろん、顧客がアプリケーションの価格設定ページでベーシック プランの「購読」ボタンをクリックする可能性があることは想像できます。このボタンは、選択したプランのPaddle チェックアウト オーバーレイを呼び出します。まず、`checkout` メソッドを使用してチェックアウト セッションを開始しましょう。

    use Illuminate\Http\Request;

    Route::get('/subscribe', function (Request $request) {
        $checkout = $request->user()->checkout('price_basic_monthly')
            ->returnTo(route('dashboard'));

        return view('subscribe', ['checkout' => $checkout]);
    })->name('subscribe');

`subscribe` ビューには、チェックアウト オーバーレイを表示するボタンが含まれます。 `paddle-button` Blade コンポーネントは Cashier Paddle に含まれています。ただし、[オーバーレイ チェックアウトを手動でレンダリングする](#manually-rendering-an-overlay-checkout) を実行することもできます。

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

「購読」ボタンをクリックすると、顧客は支払いの詳細を入力して購読を開始できるようになります。サブスクリプションが実際にいつ開始されたかを知るには (支払い方法によっては処理に数秒かかるため)、[Cashier の Webhook 処理を構成する](#handling-paddle-webhooks) も必要です。

顧客がサブスクリプションを開始できるようになったので、アプリケーションの特定の部分を制限して、サブスクライブしたユーザーのみがアクセスできるようにする必要があります。もちろん、Cashier の `Billable` トレイトによって提供される `subscribed` メソッドを介して、ユーザーの現在のサブスクリプション ステータスをいつでも確認できます。

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

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
#### サブスクライブされたミドルウェアの構築

便宜上、受信リクエストが購読ユーザーからのものであるかどうかを判断する [middleware](/docs/{{version}}/middleware) を作成するとよいでしょう。このミドルウェアを定義したら、それをルートに簡単に割り当てて、サブスクライブされていないユーザーがルートにアクセスできないようにすることができます。

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

ミドルウェアを定義したら、それをルートに割り当てることができます。

    use App\Http\Middleware\Subscribed;

    Route::get('/dashboard', function () {
        // ...
    })->middleware([Subscribed::class]);

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 顧客が料金プランを管理できるようにする

もちろん、顧客はサブスクリプション プランを別の製品または「階層」に変更したい場合もあります。上記の例では、顧客が月次サブスクリプションから年次サブスクリプションにプランを変更できるようにしたいと考えています。このためには、以下のルートにつながるボタンのようなものを実装する必要があります。

    use Illuminate\Http\Request;

    Route::put('/subscription/{price}/swap', function (Request $request, $price) {
        $user->subscription()->swap($price); // With "$price" being "price_basic_yearly" for this example.

        return redirect()->route('dashboard');
    })->name('subscription.swap');

プランを交換するだけでなく、顧客がサブスクリプションをキャンセルできるようにする必要もあります。プランの切り替えと同様に、次のルートにつながるボタンを提供します。

    use Illuminate\Http\Request;

    Route::put('/subscription/cancel', function (Request $request, $price) {
        $user->subscription()->cancel();

        return redirect()->route('dashboard');
    })->name('subscription.cancel');

そして、請求期間の終了時にサブスクリプションはキャンセルされます。

> [!NOTE]  
> Cashier の Webhook 処理を構成している限り、Cashier は Paddle から受信した Webhook を検査することで、アプリケーションの Cashier 関連のデータベース テーブルの同期を自動的に維持します。したがって、たとえば、Paddle のダッシュボード経由で顧客のサブスクリプションをキャンセルすると、Cashier は対応する Webhook を受け取り、アプリケーションのデータベース内でサブスクリプションを「キャンセル済み」としてマークします。

<a name="checkout-sessions"></a>
## チェックアウトセッション (Checkout Sessions)

顧客に請求するほとんどの操作は、Paddle の [チェックアウトオーバーレイウィジェット](https://developer.paddle.com/build/checkout/build-overlay-checkout) を介した「チェックアウト」を使用するか、[インラインチェックアウト](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) を利用して実行されます。

Paddle を使用してチェックアウト支払いを処理する前に、Paddle チェックアウト設定ダッシュボードでアプリケーションの [デフォルトの支払いリンク](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link) を定義する必要があります。

<a name="overlay-checkout"></a>
### オーバーレイチェックアウト

チェックアウト オーバーレイ ウィジェットを表示する前に、Cashier を使用してチェックアウト セッションを生成する必要があります。チェックアウト セッションは、実行する必要がある請求操作をチェックアウト ウィジェットに通知します。

    use Illuminate\Http\Request;

    Route::get('/buy', function (Request $request) {
        $checkout = $user->checkout('pri_34567')
            ->returnTo(route('dashboard'));

        return view('billing', ['checkout' => $checkout]);
    });

Cashier には、`paddle-button` [Blade コンポーネント](/docs/{{version}}/blade#components) が含まれます。チェックアウト セッションを「prop」としてこのコンポーネントに渡すことができます。次に、このボタンをクリックすると、Paddle のチェックアウト ウィジェットが表示されます。

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

デフォルトでは、Paddle のデフォルトのスタイルを使用してウィジェットが表示されます。 `data-theme='light'` 属性のような [Paddle でサポートされる属性](https://developer.paddle.com/paddlejs/html-data-attributes) をコンポーネントに追加することで、ウィジェットをカスタマイズできます。

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle チェックアウト ウィジェットは非同期です。ユーザーがウィジェット内でサブスクリプションを作成すると、アプリケーションのデータベース内のサブスクリプション状態を適切に更新できるように、Paddle がアプリケーションに Webhook を送信します。したがって、Paddle からの状態変化に対応できるように [Webhook を設定する](#handling-paddle-webhooks) を適切に設定することが重要です。

> [!WARNING]  
> サブスクリプションの状態が変更された後、対応する Webhook を受信するまでの遅延は通常最小限ですが、ユーザーのサブスクリプションがチェックアウト完了後にすぐに利用できない可能性があることを考慮して、アプリケーションでこれを考慮する必要があります。

<a name="manually-rendering-an-overlay-checkout"></a>
#### オーバーレイ チェックアウトを手動でレンダリングする

Laravel の組み込み Blade コンポーネントを使用せずに、オーバーレイ チェックアウトを手動でレンダリングすることもできます。まず、チェックアウト セッション [前の例で示したように](#overlay-checkout) を生成します。

    use Illuminate\Http\Request;

    Route::get('/buy', function (Request $request) {
        $checkout = $user->checkout('pri_34567')
            ->returnTo(route('dashboard'));

        return view('billing', ['checkout' => $checkout]);
    });

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
### インラインチェックアウト

Paddle の「オーバーレイ」スタイルのチェックアウト ウィジェットを利用したくない場合、Paddle にはウィジェットをインラインで表示するオプションも用意されています。この方法では、チェックアウトの HTML フィールドを調整することはできませんが、アプリケーション内にウィジェットを埋め込むことができます。

インライン チェックアウトを簡単に開始できるように、Cashier には `paddle-checkout` Blade コンポーネントが含まれています。開始するには、[チェックアウトセッションを生成する](#overlay-checkout) を実行する必要があります。

    use Illuminate\Http\Request;

    Route::get('/buy', function (Request $request) {
        $checkout = $user->checkout('pri_34567')
            ->returnTo(route('dashboard'));

        return view('billing', ['checkout' => $checkout]);
    });

次に、チェックアウト セッションをコンポーネントの `checkout` 属性に渡すことができます。

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

インライン チェックアウト コンポーネントの高さを調整するには、`height` 属性を Blade コンポーネントに渡すことができます。

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

インライン チェックアウトのカスタマイズ オプションの詳細については、Paddle の [インラインチェックアウトに関するガイド](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) および [利用可能なチェックアウト設定](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings) を参照してください。

<a name="manually-rendering-an-inline-checkout"></a>
#### インライン チェックアウトを手動でレンダリングする

Laravel の組み込み Blade コンポーネントを使用せずに、インライン チェックアウトを手動でレンダリングすることもできます。まず、チェックアウト セッション [前の例で示したように](#inline-checkout) を生成します。

    use Illuminate\Http\Request;

    Route::get('/buy', function (Request $request) {
        $checkout = $user->checkout('pri_34567')
            ->returnTo(route('dashboard'));

        return view('billing', ['checkout' => $checkout]);
    });

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
### ゲストのチェックアウト

場合によっては、アプリケーションのアカウントを必要としないユーザーのためにチェックアウト セッションを作成することが必要になる場合があります。これを行うには、`guest` メソッドを使用できます。

    use Illuminate\Http\Request;
    use Laravel\Paddle\Checkout;

    Route::get('/buy', function (Request $request) {
        $checkout = Checkout::guest('pri_34567')
            ->returnTo(route('home'));

        return view('billing', ['checkout' => $checkout]);
    });

次に、[Paddle ボタン](#overlay-checkout) または [インラインチェックアウト](#inline-checkout) Blade コンポーネントにチェックアウト セッションを提供できます。

<a name="price-previews"></a>
## 価格プレビュー (Price Previews)

Paddle を使用すると、通貨ごとに価格をカスタマイズできるため、基本的に国ごとに異なる価格を設定できます。 Cashier Paddle を使用すると、`previewPrices` メソッドを使用してこれらの価格をすべて取得できます。このメソッドは、価格を取得する価格 ID を受け入れます。

    use Laravel\Paddle\Cashier;

    $prices = Cashier::previewPrices(['pri_123', 'pri_456']);

通貨はリクエストの IP アドレスに基づいて決定されます。ただし、オプションで特定の国を指定して次の価格を取得することもできます。

    use Laravel\Paddle\Cashier;

    $prices = Cashier::productPrices(['pri_123', 'pri_456'], ['address' => [
        'country_code' => 'BE',
        'postal_code' => '1234',
    ]]);

価格を取得した後、必要に応じて価格を表示できます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

小計価格と税額を個別に表示することもできます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

詳細については、[価格プレビューに関する Paddle の API ドキュメントをチェックアウトする](https://developer.paddle.com/api-reference/pricing-preview/preview-prices) をご覧ください。

<a name="customer-price-previews"></a>
### 顧客価格プレビュー

ユーザーがすでに顧客であり、その顧客に適用される価格を表示したい場合は、顧客インスタンスから直接価格を取得して表示できます。

    use App\Models\User;

    $prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);

内部的には、Cashier はユーザーの顧客 ID を使用して、その通貨での価格を取得します。したがって、たとえば、米国に住んでいるユーザーには価格が米ドルで表示され、ベルギーのユーザーには価格がユーロで表示されます。一致する通貨が見つからない場合は、製品のデフォルトの通貨が使用されます。Paddle コントロール パネルで、製品またはサブスクリプション プランのすべての価格をカスタマイズできます。

<a name="price-discounts"></a>
### 割引

割引後の価格を表示することもできます。 `previewPrices` メソッドを呼び出すときは、`discount_id` オプションを使用して割引 ID を指定します。

    use Laravel\Paddle\Cashier;

    $prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
        'discount_id' => 'dsc_123'
    ]);

次に、計算された価格を表示します。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

<a name="customers"></a>
## お客様 (Customers)

<a name="customer-defaults"></a>
### 顧客のデフォルト

Cashier を使用すると、チェックアウト セッションを作成するときに、顧客にとって役立つデフォルトをいくつか定義できます。これらのデフォルトを設定すると、顧客の電子メール アドレスと名前を事前に入力できるため、顧客はすぐにチェックアウト ウィジェットの支払い部分に進むことができます。これらのデフォルトは、請求可能なモデルで次のメソッドをオーバーライドすることで設定できます。

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

これらのデフォルトは、[チェックアウトセッション](#checkout-sessions) を生成する Cashier のすべてのアクションに使用されます。

<a name="retrieving-customers"></a>
### 顧客の取得

`Cashier::findBillable` メソッドを使用して、Paddle 顧客 ID によって顧客を取得できます。このメソッドは、課金対象モデルのインスタンスを返します。

    use Laravel\Cashier\Cashier;

    $user = Cashier::findBillable($customerId);

<a name="creating-customers"></a>
### 顧客の創造

場合によっては、サブスクリプションを開始せずに Paddle 顧客を作成したい場合があります。これは、`createAsCustomer` メソッドを使用して実行できます。

    $customer = $user->createAsCustomer();

`Laravel\Paddle\Customer` のインスタンスが返されます。 Paddle で顧客を作成したら、後日サブスクリプションを開始できます。オプションの `$options` 配列を指定して、追加の [Paddle API でサポートされる顧客作成パラメータ](https://developer.paddle.com/api-reference/customers/create-customer) を渡すことができます。

    $customer = $user->createAsCustomer($options);

<a name="subscriptions"></a>
## 定期購入 (Subscriptions)

<a name="creating-subscriptions"></a>
### サブスクリプションの作成

サブスクリプションを作成するには、まず課金対象モデルのインスタンスをデータベースから取得します。これは通常、`App\Models\User` のインスタンスになります。モデル インスタンスを取得したら、`subscribe` メソッドを使用してモデルのチェックアウト セッションを作成できます。

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $checkout = $request->user()->subscribe($premium = 12345, 'default')
            ->returnTo(route('home'));

        return view('billing', ['checkout' => $checkout]);
    });

`subscribe` メソッドに指定される最初の引数は、ユーザーが購読している特定の価格です。この値は、Paddle の価格の識別子に対応する必要があります。 `returnTo` メソッドは、ユーザーがチェックアウトを正常に完了した後にリダイレクトされる URL を受け入れます。 `subscribe` メソッドに渡される 2 番目の引数は、サブスクリプションの内部「タイプ」である必要があります。アプリケーションが単一のサブスクリプションのみを提供する場合は、これを `default` または `primary` と呼びます。このサブスクリプション タイプはアプリケーション内部でのみ使用され、ユーザーに表示されることを意図したものではありません。また、スペースを含めることはできません。また、サブスクリプションの作成後に変更しないでください。

`customData` メソッドを使用して、サブスクリプションに関するカスタム メタ データの配列を提供することもできます。

    $checkout = $request->user()->subscribe($premium = 12345, 'default')
        ->customData(['key' => 'value'])
        ->returnTo(route('home'));

サブスクリプションのチェックアウト セッションが作成されると、そのチェックアウト セッションは、Cashier Paddle に含まれる `paddle-button` [Blade コンポーネント](#overlay-checkout) に提供されます。

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

ユーザーがチェックアウトを完了すると、`subscription_created` Webhook が Paddle からディスパッチされます。レジ担当者はこの Webhook を受信し、顧客のサブスクリプションをセットアップします。すべての Webhook が適切に受信され、アプリケーションによって処理されることを確認するには、[Webhook 処理のセットアップ](#handling-paddle-webhooks) が適切に設定されていることを確認してください。

<a name="checking-subscription-status"></a>
### 購読ステータスの確認

ユーザーがアプリケーションを購読すると、さまざまな便利な方法を使用してその購読ステータスを確認できます。まず、ユーザーが有効なサブスクリプションを持っている場合、サブスクリプションが現在試用期間内であっても、`subscribed` メソッドは `true` を返します。

    if ($user->subscribed()) {
        // ...
    }

アプリケーションが複数のサブスクリプションを提供する場合、`subscribed` メソッドを呼び出すときにサブスクリプションを指定できます。

    if ($user->subscribed('default')) {
        // ...
    }

`subscribed` メソッドも [ルートミドルウェア](/docs/{{version}}/middleware) の有力な候補となり、ユーザーのサブスクリプション ステータスに基づいてルートとコントローラへのアクセスをフィルタリングできます。

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
                return redirect('billing');
            }

            return $next($request);
        }
    }

ユーザーがまだ試用期間内であるかどうかを確認したい場合は、`onTrial` メソッドを使用できます。このメソッドは、ユーザーがまだ試用期間中であることをユーザーに警告するかどうかを決定するのに役立ちます。

    if ($user->subscription()->onTrial()) {
        // ...
    }

`subscribedToPrice` メソッドは、特定の Paddle 価格 ID に基づいて、ユーザーが特定のプランに加入しているかどうかを判断するために使用できます。この例では、ユーザーの `default` サブスクリプションが月額料金にアクティブにサブスクライブされているかどうかを判断します。

    if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
        // ...
    }

`recurring` メソッドを使用して、ユーザーが現在アクティブなサブスクリプションに参加していて、試用期間中であるか猶予期間中であるかを判断できます。

    if ($user->subscription()->recurring()) {
        // ...
    }

<a name="canceled-subscription-status"></a>
#### キャンセルされたサブスクリプションのステータス

ユーザーがかつてはアクティブなサブスクライバだったが、サブスクリプションをキャンセルしたかどうかを確認するには、`canceled` メソッドを使用できます。

    if ($user->subscription()->canceled()) {
        // ...
    }

また、ユーザーがサブスクリプションをキャンセルしたが、サブスクリプションが完全に期限切れになるまでまだ「猶予期間」中であるかどうかを判断することもできます。たとえば、ユーザーが元々 3 月 10 日に期限切れになる予定だったサブスクリプションを 3 月 5 日にキャンセルした場合、ユーザーは 3 月 10 日まで「猶予期間」に入ります。さらに、`subscribed` メソッドは、この間も `true` を返します。

    if ($user->subscription()->onGracePeriod()) {
        // ...
    }

<a name="past-due-status"></a>
#### 期限超過ステータス

サブスクリプションの支払いが失敗した場合、`past_due` としてマークされます。サブスクリプションがこの状態にある場合、顧客が支払い情報を更新するまでアクティブになりません。サブスクリプション インスタンスの `pastDue` メソッドを使用して、サブスクリプションの期限が過ぎているかどうかを確認できます。

    if ($user->subscription()->pastDue()) {
        // ...
    }

サブスクリプションの期限を過ぎた場合は、ユーザーに [支払い情報を更新する](#updating-payment-information) を指示する必要があります。

サブスクリプションが `past_due` の場合でも有効であると見なしたい場合は、Cashier が提供する `keepPastDueSubscriptionsActive` メソッドを使用できます。通常、このメソッドは、`AppServiceProvider` の `register` メソッドで呼び出す必要があります。

    use Laravel\Paddle\Cashier;

    /**
     * Register any application services.
     */
    public function register(): void
    {
        Cashier::keepPastDueSubscriptionsActive();
    }

> [!WARNING]  
> サブスクリプションが `past_due` 状態にある場合、支払い情報が更新されるまで変更することはできません。したがって、サブスクリプションが `past_due` 状態にある場合、`swap` メソッドと `updateQuantity` メソッドは例外をスローします。

<a name="subscription-scopes"></a>
#### サブスクリプションの範囲

ほとんどのサブスクリプション状態はクエリ スコープとしても使用できるため、特定の状態にあるサブスクリプションについてデータベースを簡単にクエリできます。

    // Get all valid subscriptions...
    $subscriptions = Subscription::query()->valid()->get();

    // Get all of the canceled subscriptions for a user...
    $subscriptions = $user->subscriptions()->canceled()->get();

利用可能なスコープの完全なリストは以下で入手できます。

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

<a name="subscription-single-charges"></a>
### サブスクリプションの単一料金

サブスクリプションの単一料金を使用すると、サブスクリプションに加えて 1 回限りの料金をサブスクライバに請求できます。 `charge` メソッドを呼び出すときは、1 つまたは複数の価格 ID を指定する必要があります。

    // Charge a single price...
    $response = $user->subscription()->charge('pri_123');

    // Charge multiple prices at once...
    $response = $user->subscription()->charge(['pri_123', 'pri_456']);

`charge` メソッドでは、サブスクリプションの次の請求間隔まで実際には顧客に請求されません。顧客にすぐに請求したい場合は、代わりに `chargeAndInvoice` メソッドを使用できます。

    $response = $user->subscription()->chargeAndInvoice('pri_123');

<a name="updating-payment-information"></a>
### 支払い情報の更新

Paddle は常にサブスクリプションごとに支払い方法を保存します。サブスクリプションのデフォルトの支払い方法を更新する場合は、サブスクリプション モデルの `redirectToUpdatePaymentMethod` メソッドを使用して、顧客を Paddle のホスト型支払い方法更新ページにリダイレクトする必要があります。

    use Illuminate\Http\Request;

    Route::get('/update-payment-method', function (Request $request) {
        $user = $request->user();

        return $user->subscription()->redirectToUpdatePaymentMethod();
    });

ユーザーが情報の更新を完了すると、`subscription_updated` Webhook が Paddle によって送出され、サブスクリプションの詳細がアプリケーションのデータベースで更新されます。

<a name="changing-plans"></a>
### プランの変更

ユーザーがアプリケーションを購読した後、新しい購読プランへの変更を希望する場合があります。ユーザーのサブスクリプション プランを更新するには、Paddle 価格の識別子をサブスクリプションの `swap` メソッドに渡す必要があります。

    use App\Models\User;

    $user = User::find(1);

    $user->subscription()->swap($premium = 'pri_456');

プランを交換して、次の請求サイクルを待たずにすぐにユーザーに請求を行いたい場合は、`swapAndInvoice` メソッドを使用できます。

    $user = User::find(1);

    $user->subscription()->swapAndInvoice($premium = 'pri_456');

<a name="prorations"></a>
#### 按分

デフォルトでは、Paddle はプラン間を切り替えるときに料金を日割り計算します。 `noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションを更新できます。

    $user->subscription('default')->noProrate()->swap($premium = 'pri_456');

日割り計算と請求書の顧客をすぐに無効にしたい場合は、`swapAndInvoice` メソッドを `noProrate` と組み合わせて使用​​できます。

    $user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');

または、サブスクリプションの変更に対して顧客に請求しないようにするには、`doNotBill` メソッドを利用することもできます。

    $user->subscription('default')->doNotBill()->swap($premium = 'pri_456');

Paddle の比例配分ポリシーの詳細については、Paddle の [比例配分に関する文書](https://developer.paddle.com/concepts/subscriptions/proration) を参照してください。

<a name="subscription-quantity"></a>
### 購読数量

サブスクリプションは「数量」の影響を受ける場合があります。たとえば、プロジェクト管理アプリケーションでは、プロジェクトごとに月額 10 ドルを請求する場合があります。サブスクリプションの数量を簡単に増減するには、`incrementQuantity` メソッドと `decrementQuantity` メソッドを使用します。

    $user = User::find(1);

    $user->subscription()->incrementQuantity();

    // Add five to the subscription's current quantity...
    $user->subscription()->incrementQuantity(5);

    $user->subscription()->decrementQuantity();

    // Subtract five from the subscription's current quantity...
    $user->subscription()->decrementQuantity(5);

あるいは、`updateQuantity` メソッドを使用して特定の数量を設定することもできます。

    $user->subscription()->updateQuantity(10);

`noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションの数量を更新できます。

    $user->subscription()->noProrate()->updateQuantity(10);

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 複数の製品のサブスクリプションの数量

サブスクリプションが [複数の製品のサブスクリプション](#subscriptions-with-multiple-products) の場合は、増分または減分する数量の価格の ID を 2 番目の引数として増分 / 減分メソッドに渡す必要があります。

    $user->subscription()->incrementQuantity(1, 'price_chat');

<a name="subscriptions-with-multiple-products"></a>
### 複数の製品のサブスクリプション

[複数の製品のサブスクリプション](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons) を使用すると、複数の課金製品を 1 つのサブスクリプションに割り当てることができます。たとえば、基本サブスクリプション価格が月額 10 ドルであるが、月額 15 ドルの追加料金でライブ チャット アドオン製品を提供するカスタマー サービスの「ヘルプデスク」アプリケーションを構築していると想像してください。

サブスクリプション チェックアウト セッションを作成するとき、価格の配列を最初の引数として `subscribe` メソッドに渡すことで、特定のサブスクリプションに複数の製品を指定できます。

    use Illuminate\Http\Request;

    Route::post('/user/subscribe', function (Request $request) {
        $checkout = $request->user()->subscribe([
            'price_monthly',
            'price_chat',
        ]);

        return view('billing', ['checkout' => $checkout]);
    });

上の例では、顧客は `default` サブスクリプションに 2 つの価格を設定します。どちらの価格も、それぞれの請求間隔で請求されます。必要に応じて、キーと値のペアの連想配列を渡して、各価格の特定の数量を示すことができます。

    $user = User::find(1);

    $checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);

既存のサブスクリプションに別の価格を追加する場合は、サブスクリプションの `swap` メソッドを使用する必要があります。 `swap` メソッドを呼び出すときは、サブスクリプションの現在の価格と数量も含める必要があります。

    $user = User::find(1);

    $user->subscription()->swap(['price_chat', 'price_original' => 2]);

上の例では新しい価格が追加されますが、顧客には次の請求サイクルまで請求されません。顧客にすぐに請求したい場合は、`swapAndInvoice` メソッドを使用できます。

    $user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);

`swap` メソッドを使用し、削除する価格を省略して、サブスクリプションから価格を削除できます。

    $user->subscription()->swap(['price_original' => 2]);

> [!WARNING]  
> サブスクリプションの最後の価格を削除することはできません。代わりに、サブスクリプションをキャンセルするだけです。

<a name="multiple-subscriptions"></a>
### 複数のサブスクリプション

Paddle を使用すると、顧客は同時に複数のサブスクリプションを持つことができます。たとえば、水泳のサブスクリプションとウェイトリフティングのサブスクリプションを提供するジムを運営しており、各サブスクリプションの価格が異なる場合があります。もちろん、顧客はどちらかまたは両方のプランに加入できる必要があります。

アプリケーションがサブスクリプションを作成するとき、2 番目の引数として `subscribe` メソッドにサブスクリプションのタイプを指定できます。タイプには、ユーザーが開始しているサブスクリプションのタイプを表す任意の文字列を指定できます。

    use Illuminate\Http\Request;

    Route::post('/swimming/subscribe', function (Request $request) {
        $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

        return view('billing', ['checkout' => $checkout]);
    });

この例では、顧客に対して毎月の水泳サブスクリプションを開始しました。ただし、後で年間サブスクリプションに切り替えたい場合もあります。顧客のサブスクリプションを調整するときは、`swimming` サブスクリプションの価格を単純に交換できます。

    $user->subscription('swimming')->swap($swimmingYearly = 'pri_456');

もちろん、サブスクリプションを完全にキャンセルすることもできます。

    $user->subscription('swimming')->cancel();

<a name="pausing-subscriptions"></a>
### サブスクリプションの一時停止

サブスクリプションを一時停止するには、ユーザーのサブスクリプションで `pause` メソッドを呼び出します。

    $user->subscription()->pause();

サブスクリプションが一時停止されると、Cashier はデータベースに `paused_at` 列を自動的に設定します。この列は、`paused` メソッドが `true` を返し始める時期を決定するために使用されます。たとえば、顧客が 3 月 1 日にサブスクリプションを一時停止したが、そのサブスクリプションが 3 月 5 日まで繰り返されるようにスケジュールされていなかった場合、`paused` メソッドは 3 月 5 日まで `false` を返し続けます。これは、通常、ユーザーは請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているためです。

デフォルトでは、次の請求間隔で一時停止が行われるため、顧客は支払った期間の残りを使用できます。サブスクリプションをすぐに一時停止したい場合は、`pauseNow` メソッドを使用できます。

    $user->subscription()->pauseNow();

`pauseUntil` メソッドを使用すると、特定の時点までサブスクリプションを一時停止できます。

    $user->subscription()->pauseUntil(now()->addMonth());

または、`pauseNowUntil` メソッドを使用して、特定の時点までサブスクリプションをすぐに一時停止することもできます。

    $user->subscription()->pauseNowUntil(now()->addMonth());

ユーザーがサブスクリプションを一時停止しているが、まだ「猶予期間」中であるかどうかを、`onPausedGracePeriod` メソッドを使用して判断できます。

    if ($user->subscription()->onPausedGracePeriod()) {
        // ...
    }

一時停止したサブスクリプションを再開するには、サブスクリプションで `resume` メソッドを呼び出すことができます。

    $user->subscription()->resume();

> [!WARNING]  
> 一時停止中はサブスクリプションを変更できません。別のプランに切り替えたり、数量を更新したりする場合は、まずサブスクリプションを再開する必要があります。

<a name="canceling-subscriptions"></a>
### 定期購入のキャンセル

サブスクリプションをキャンセルするには、ユーザーのサブスクリプションで `cancel` メソッドを呼び出します。

    $user->subscription()->cancel();

サブスクリプションがキャンセルされると、Cashier はデータベースに `ends_at` 列を自動的に設定します。この列は、`subscribed` メソッドが `false` を返し始める時期を決定するために使用されます。たとえば、顧客が 3 月 1 日にサブスクリプションをキャンセルしたが、そのサブスクリプションが 3 月 5 日まで終了する予定ではなかった場合、`subscribed` メソッドは 3 月 5 日まで `true` を返し続けます。これは、ユーザーが通常、請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているために行われます。

`onGracePeriod` メソッドを使用して、ユーザーがサブスクリプションをキャンセルしたがまだ「猶予期間」中であるかどうかを確認できます。

    if ($user->subscription()->onGracePeriod()) {
        // ...
    }

サブスクリプションをすぐにキャンセルしたい場合は、サブスクリプションで `cancelNow` メソッドを呼び出すことができます。

    $user->subscription()->cancelNow();

猶予期間中のサブスクリプションのキャンセルを停止するには、`stopCancelation` メソッドを呼び出します。

    $user->subscription()->stopCancelation();

> [!WARNING]  
> Paddle のサブスクリプションは、キャンセル後に再開することはできません。顧客がサブスクリプションの再開を希望する場合は、新しいサブスクリプションを作成する必要があります。

<a name="subscription-trials"></a>
## サブスクリプショントライアル (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 支払い方法を前払いする場合

支払い方法情報を事前に収集しながら顧客に試用期間を提供したい場合は、顧客が購読している価格に応じて Paddle ダッシュボードで試用期間を設定する必要があります。次に、通常どおりチェックアウト セッションを開始します。

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $checkout = $request->user()->subscribe('pri_monthly')
                    ->returnTo(route('home'));

        return view('billing', ['checkout' => $checkout]);
    });

アプリケーションが `subscription_created` イベントを受信すると、Cashier はアプリケーションのデータベース内のサブスクリプション レコードに試用期間の終了日を設定し、この日付以降になるまで顧客への請求を開始しないように Paddle に指示します。

> [!WARNING]  
> 試用期間の終了日までに顧客のサブスクリプションがキャンセルされなかった場合、試用期間が終了するとすぐに料金が請求されるため、ユーザーに試用期間の終了日を必ず通知する必要があります。

ユーザー インスタンスの `onTrial` メソッドまたはサブスクリプション インスタンスの `onTrial` メソッドを使用して、ユーザーが試用期間内かどうかを判断できます。以下の 2 つの例は同等です。

    if ($user->onTrial()) {
        // ...
    }

    if ($user->subscription()->onTrial()) {
        // ...
    }
既存の試用版の有効期限が切れているかどうかを確認するには、`hasExpiredTrial` メソッドを使用できます。

    if ($user->hasExpiredTrial()) {
        // ...
    }

    if ($user->subscription()->hasExpiredTrial()) {
        // ...
    }

ユーザーが特定のサブスクリプション タイプの試用中かどうかを判断するには、そのタイプを `onTrial` メソッドまたは `hasExpiredTrial` メソッドに指定できます。

    if ($user->onTrial('default')) {
        // ...
    }

    if ($user->hasExpiredTrial('default')) {
        // ...
    }

<a name="without-payment-method-up-front"></a>
### 前払いの支払い方法なし

ユーザーの支払い方法情報を事前に収集せずに試用期間を提供したい場合は、ユーザーに添付されている顧客レコードの `trial_ends_at` 列を希望する試用終了日に設定できます。これは通常、ユーザー登録時に行われます。

    use App\Models\User;

    $user = User::create([
        // ...
    ]);

    $user->createAsCustomer([
        'trial_ends_at' => now()->addDays(10)
    ]);

既存のサブスクリプションに関連付けられていないため、Cashier はこのタイプのトライアルを「一般トライアル」と呼びます。現在の日付が `trial_ends_at` の値を超えていない場合、`User` インスタンスの `onTrial` メソッドは `true` を返します。

    if ($user->onTrial()) {
        // User is within their trial period...
    }

ユーザーの実際のサブスクリプションを作成する準備ができたら、通常どおり `subscribe` メソッドを使用できます。

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $checkout = $user->subscribe('pri_monthly')
            ->returnTo(route('home'));

        return view('billing', ['checkout' => $checkout]);
    });

ユーザーの試用終了日を取得するには、`trialEndsAt` メソッドを使用できます。このメソッドは、ユーザーが試用中の場合は Carbon date インスタンスを返し、試用中でない場合は `null` を返します。デフォルト以外の特定のサブスクリプションの試用終了日を取得したい場合は、オプションのサブスクリプション タイプ パラメーターを渡すこともできます。

    if ($user->onTrial('default')) {
        $trialEndsAt = $user->trialEndsAt();
    }

ユーザーが「一般的な」試用期間内であり、実際のサブスクリプションをまだ作成していないことを具体的に知りたい場合は、`onGenericTrial` メソッドを使用できます。

    if ($user->onGenericTrial()) {
        // User is within their "generic" trial period...
    }

<a name="extend-or-activate-a-trial"></a>
### トライアルを延長またはアクティブ化する

`extendTrial` メソッドを呼び出し、トライアルを終了する時点を指定することで、サブスクリプションの既存のトライアル期間を延長できます。

    $user->subsription()->extendTrial(now()->addDays(5));

または、サブスクリプションで `activate` メソッドを呼び出してトライアルを終了し、サブスクリプションをすぐにアクティブ化することもできます。

    $user->subscription()->activate();

<a name="handling-paddle-webhooks"></a>
## Paddle Webhook の処理 (Handling Paddle Webhooks)

Paddle は、Webhook 経由でさまざまなイベントをアプリケーションに通知できます。デフォルトでは、Cashier の Webhook コントローラを指すルートが Cashier サービスプロバイダによって登録されます。このコントローラは、受信したすべての Webhook リクエストを処理します。

デフォルトでは、このコントローラは、請求失敗が多すぎるサブスクリプションのキャンセル、サブスクリプションの更新、支払い方法の変更を自動的に処理します。ただし、すぐにわかりますが、このコントローラを拡張して、任意の Paddle Webhook イベントを処理できます。

アプリケーションが Paddle Webhook を処理できることを確認するには、必ず [Paddle コントロールパネルでWebhook URLを設定します。](https://vendors.paddle.com/alerts-webhooks) を実行してください。デフォルトでは、Cashier の Webhook コントローラは `/paddle/webhook` URL パスに応答します。Paddle コントロール パネルで有効にする必要があるすべての Webhook の完全なリストは次のとおりです。

- 顧客が更新しました
- 取引完了
- トランザクションが更新されました
- サブスクリプションが作成されました
- サブスクリプションが更新されました
- サブスクリプションが一時停止されました
- サブスクリプションがキャンセルされました

> [!WARNING]  
> Cashier に含まれる [Webhook 署名の検証](/docs/{{version}}/cashier-paddle#verifying-webhook-signatures) ミドルウェアを使用して、受信リクエストを必ず保護してください。

<a name="webhooks-csrf-protection"></a>
#### Webhook と CSRF 保護

Paddle Webhook は Laravel の [CSRF保護](/docs/{{version}}/csrf) をバイパスする必要があるため、必ず `App\Http\Middleware\VerifyCsrfToken` ミドルウェアの例外として URI をリストするか、`web` ミドルウェア グループの外側のルートをリストしてください。

    protected $except = [
        'paddle/*',
    ];

<a name="webhooks-local-development"></a>
#### Webhook とローカル開発

Paddle がローカル開発中にアプリケーション Webhook を送信できるようにするには、[Ngrok](https://ngrok.com/) や [Expose](https://expose.dev/docs/introduction) などのサイト共有サービスを介してアプリケーションを公開する必要があります。 [Laravel Sail](/docs/{{version}}/sail) を使用してアプリケーションをローカルで開発している場合は、Sail の [サイト共有コマンド](/docs/{{version}}/sail#sharing-your-site) を使用できます。

<a name="defining-webhook-event-handlers"></a>
### Webhook イベント ハンドラーの定義

Cashier は、失敗した請求やその他の一般的な Paddle Webhook によるサブスクリプションのキャンセルを自動的に処理します。ただし、追加の Webhook イベントを処理したい場合は、Cashier によって送出される次のイベントをリッスンすることで処理できます。

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

どちらのイベントにも、Paddle Webhook の完全なペイロードが含まれています。たとえば、`transaction_billed` Webhook を処理したい場合は、イベントを処理する [listener](/docs/{{version}}/events#defining-listeners) を登録できます。

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
            if ($event->payload['alert_name'] === 'transaction_billed') {
                // Handle the incoming event...
            }
        }
    }

リスナを定義したら、アプリケーションの `EventServiceProvider` 内にリスナを登録できます。

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

Cashier は、受信した Webhook のタイプ専用のイベントも発行します。 Paddle からの完全なペイロードに加えて、請求可能なモデル、サブスクリプション、レシートなど、Webhook の処理に使用された関連モデルも含まれています。

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

アプリケーションの `.env` ファイルで `CASHIER_WEBHOOK` 環境変数を定義することで、デフォルトの組み込み Webhook ルートをオーバーライドすることもできます。この値は Webhook ルートの完全な URL である必要があり、Paddle コントロール パネルで設定された URL と一致する必要があります。

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### Webhook 署名の検証

Webhook を保護するには、[Paddle の Webhook 署名](https://developer.paddle.com/webhook-reference/verifying-webhooks) を使用できます。便宜上、Cashier には、受信した Paddle Webhook リクエストが有効であることを検証するミドルウェアが自動的に組み込まれています。

Webhook 検証を有効にするには、`PADDLE_WEBHOOK_SECRET` 環境変数がアプリケーションの `.env` ファイルで定義されていることを確認してください。 Webhook シークレットは、Paddle アカウントのダッシュボードから取得できます。

<a name="single-charges"></a>
## シングルチャージ (Single Charges)

<a name="charging-for-products"></a>
### 製品の課金

顧客のために製品の購入を開始したい場合は、請求可能モデル インスタンスで `checkout` メソッドを使用して、購入のためのチェックアウト セッションを生成できます。 `checkout` メソッドは、1 つまたは複数の価格 ID を受け入れます。必要に応じて、連想配列を使用して、購入される製品の数量を提供することもできます。

    use Illuminate\Http\Request;

    Route::get('/buy', function (Request $request) {
        $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

        return view('buy', ['checkout' => $checkout]);
    });

チェックアウト セッションを生成した後、Cashierが提供する `paddle-button` [Blade コンポーネント](#overlay-checkout) を使用して、ユーザーがPaddle チェックアウト ウィジェットを表示して購入を完了できるようにすることができます。

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

チェックアウト セッションには `customData` メソッドがあり、必要なカスタム データを基になるトランザクション作成に渡すことができます。カスタム データを渡すときに利用できるオプションの詳細については、[Paddle のドキュメント](https://developer.paddle.com/build/transactions/custom-data) を参照してください。

    $checkout = $user->checkout('pri_tshirt')
        ->customData([
            'custom_option' => $value,
        ]);

<a name="refunding-transactions"></a>
### 返金取引

返金取引では、購入時に使用された顧客の支払い方法に返金金額が返されます。 Paddle の購入を返金する必要がある場合は、`Cashier\Paddle\Transaction` モデルで `refund` メソッドを使用できます。このメソッドは、最初の引数として理由を受け入れ、オプションの金額を連想配列として返金する 1 つ以上の価格 ID を受け取ります。 `transactions` メソッドを使用して、特定の請求可能モデルのトランザクションを取得できます。

たとえば、価格 `pri_123` および `pri_456` の特定のトランザクションを返金したいとします。 `pri_123` は全額返金したいのですが、`pri_456` については 2 ドルのみ返金したいと考えています。

    use App\Models\User;

    $user = User::find(1);

    $transaction = $user->transactions()->first();

    $response = $transaction->refund('Accidental charge', [
        'pri_123', // Fully refund this price...
        'pri_456' => 200, // Only partially refund this price...
    ]);

上の例では、トランザクション内の特定の項目を返金します。取引全体を返金したい場合は、理由を入力してください。

    $response = $transaction->refund('Accidental charge');

払い戻しの詳細については、[Paddle の返金ドキュメント](https://developer.paddle.com/build/transactions/create-transaction-adjustments) にお問い合わせください。

> [!WARNING]  
> 返金は完全に処理される前に必ず Paddle の承認を受ける必要があります。

<a name="crediting-transactions"></a>
### クレジット取引

払い戻しと同様に、トランザクションをクレジット処理することもできます。トランザクションをクレジットすると、資金が顧客の残高に追加され、将来の購入に使用できるようになります。 Paddle はサブスクリプション クレジットを自動的に処理するため、トランザクションのクレジット付与は手動で収集されたトランザクションに対してのみ実行でき、自動収集されたトランザクション (サブスクリプションなど) に対しては実行できません。

    $transaction = $user->transactions()->first();

    // Credit a specific line item fully...
    $response = $transaction->credit('Compensation', 'pri_123');

詳細については、[クレジットに関するPaddleのドキュメントを参照してください。](https://developer.paddle.com/build/transactions/create-transaction-adjustments) をご覧ください。

> [!WARNING]  
> クレジットは手動で収集されたトランザクションにのみ適用できます。自動的に収集されたトランザクションは、Paddle 自体によって入金されます。

<a name="transactions"></a>
## 取引 (Transactions)

`transactions` プロパティを使用して、請求可能なモデルのトランザクションの配列を簡単に取得できます。

    use App\Models\User;

    $user = User::find(1);

    $transactions = $user->transactions;

トランザクションは製品と購入の支払いを表し、請求書が添付されます。完了したトランザクションのみがアプリケーションのデータベースに保存されます。

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

`download-invoice` ルートは次のようになります。

    use Illuminate\Http\Request;
    use Laravel\Cashier\Transaction;

    Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
        return $transaction->redirectToInvoicePdf();
    })->name('download-invoice');

<a name="past-and-upcoming-payments"></a>
### 過去および今後の支払い

`lastPayment` メソッドと `nextPayment` メソッドを使用して、定期購読に対する顧客の過去または今後の支払いを取得して表示できます。

    use App\Models\User;

    $user = User::find(1);

    $subscription = $user->subscription();

    $lastPayment = $subscription->lastPayment();
    $nextPayment = $subscription->nextPayment();

これらのメソッドは両方とも、`Laravel\Paddle\Payment` のインスタンスを返します。ただし、トランザクションが Webhook によってまだ同期されていない場合、`lastPayment` は `null` を返しますが、請求サイクルが終了した場合 (サブスクリプションがキャンセルされた場合など)、`nextPayment` は `null` を返します。

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## テスト (Testing)

テスト中に、請求フローを手動でテストして、統合が期待どおりに機能することを確認する必要があります。

CI 環境内で実行されるテストを含む自動テストの場合、[LaravelのHTTPクライアント](/docs/{{version}}/http-client#testing) を使用して Paddle に対して行われた HTTP 呼び出しを偽装できます。これは Paddle からの実際の応答をテストしませんが、実際に Paddle の API を呼び出さずにアプリケーションをテストする方法を提供します。

