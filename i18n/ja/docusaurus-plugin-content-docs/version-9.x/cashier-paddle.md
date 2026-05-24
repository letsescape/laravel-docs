# Laravel Cashier (Paddle) (Laravel Cashier (Paddle))

- [Introduction](#introduction)
- [Cashierのアップグレード](#upgrading-cashier)
- [Installation](#installation)
    - [Paddle サンドボックス](#paddle-sandbox)
    - [データベースの移行](#database-migrations)
- [Configuration](#configuration)
    - [課金対象モデル](#billable-model)
    - [APIキー](#api-keys)
    - [Paddle.js](#paddle-js)
    - [通貨構成](#currency-configuration)
    - [デフォルトモデルの上書き](#overriding-default-models)
- [中心となる概念](#core-concepts)
    - [有料リンク](#pay-links)
    - [インラインチェックアウト](#inline-checkout)
    - [ユーザーの識別](#user-identification)
- [Prices](#prices)
- [Customers](#customers)
    - [顧客のデフォルト](#customer-defaults)
- [Subscriptions](#subscriptions)
    - [サブスクリプションの作成](#creating-subscriptions)
    - [購読ステータスの確認](#checking-subscription-status)
    - [サブスクリプションの単一料金](#subscription-single-charges)
    - [支払い情報の更新](#updating-payment-information)
    - [プランの変更](#changing-plans)
    - [購読数量](#subscription-quantity)
    - [サブスクリプション修飾子](#subscription-modifiers)
    - [複数のサブスクリプション](#multiple-subscriptions)
    - [サブスクリプションの一時停止](#pausing-subscriptions)
    - [定期購入のキャンセル](#cancelling-subscriptions)
- [サブスクリプショントライアル](#subscription-trials)
    - [支払い方法を前払いする場合](#with-payment-method-up-front)
    - [前払いの支払い方法なし](#without-payment-method-up-front)
- [Paddle Webhook の処理](#handling-paddle-webhooks)
    - [Webhook イベント ハンドラーの定義](#defining-webhook-event-handlers)
    - [Webhook 署名の検証](#verifying-webhook-signatures)
- [シングルチャージ](#single-charges)
    - [かんたんチャージ](#simple-charge)
    - [充電製品](#charging-products)
    - [注文の払い戻し](#refunding-orders)
- [Receipts](#receipts)
    - [過去および今後の支払い](#past-and-upcoming-payments)
- [失敗した支払いの処理](#handling-failed-payments)
- [Testing](#testing)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) は、[Paddle の](https://paddle.com) サブスクリプション請求サービスへの表現力豊かで流暢なインターフェイスを提供します。あなたが恐れている定型的なサブスクリプション請求コードのほぼすべてを処理します。基本的なサブスクリプション管理に加えて、Cashier はクーポン、サブスクリプションの交換、サブスクリプションの「数量」、キャンセル猶予期間などを処理できます。

Cashier を使用する際には、Paddle の [ユーザーガイド](https://developer.paddle.com/guides) および [APIドキュメント](https://developer.paddle.com/api-reference) も確認することをお勧めします。

<a name="upgrading-cashier"></a>
## Cashierのアップグレード (Upgrading Cashier)

Cashier の新しいバージョンにアップグレードする場合は、[アップグレードガイド](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを使用して Paddle の Cashier パッケージをインストールします。

```shell
composer require laravel/cashier-paddle
```

> **警告**
> Cashier がすべての Paddle イベントを適切に処理できるようにするには、[Cashier の Webhook 処理を設定する](#handling-paddle-webhooks) を忘れないでください。

<a name="paddle-sandbox"></a>
### Paddle サンドボックス

ローカルおよびステージング開発中は、[Paddle Sandbox アカウントを登録する](https://developer.paddle.com/getting-started/sandbox) を実行する必要があります。このアカウントでは、実際に支払いを行わずにアプリケーションのテストと開発を行うためのサンドボックス環境が提供されます。 Paddle の [テストカード番号](https://developer.paddle.com/getting-started/sandbox#test-cards) を使用して、さまざまな支払いシナリオをシミュレートできます。

Paddle Sandbox 環境を使用する場合は、アプリケーションの `.env` ファイル内で `PADDLE_SANDBOX` 環境変数を `true` に設定する必要があります。

```ini
PADDLE_SANDBOX=true
```

アプリケーションの開発が完了したら、[Paddle ベンダー アカウントを申請する](https://paddle.com) を実行できます。アプリケーションを運用環境に導入する前に、Paddle はアプリケーションのドメインを承認する必要があります。

<a name="database-migrations"></a>
### データベースの移行

Cashier サービスプロバイダは独自のデータベース移行ディレクトリを登録するため、パッケージのインストール後にデータベースを移行することを忘れないでください。 Cashier の移行により、新しい `customers` テーブルが作成されます。さらに、顧客のすべてのサブスクリプションを保存するために、新しい `subscriptions` テーブルが作成されます。最後に、アプリケーションのすべての受信情報を保存するための新しい `receipts` テーブルが作成されます。

```shell
php artisan migrate
```

Cashier に含まれる移行を上書きする必要がある場合は、`vendor:publish` Artisan コマンドを使用して公開できます。

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

Cashier の移行が完全に実行されないようにする場合は、Cashier が提供する `ignoreMigrations` を使用できます。通常、このメソッドは、`AppServiceProvider` の `register` メソッドで呼び出す必要があります。

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

<a name="configuration"></a>
## 構成 (Configuration)

<a name="billable-model"></a>
### 課金対象モデル

Cashier を使用する前に、`Billable` 特性をユーザー モデル定義に追加する必要があります。この特性は、サブスクリプションの作成、クーポンの適用、支払い方法情報の更新などの一般的な請求タスクを実行できるようにするさまざまなメソッドを提供します。

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
PADDLE_VENDOR_ID=your-paddle-vendor-id
PADDLE_VENDOR_AUTH_CODE=your-paddle-vendor-auth-code
PADDLE_PUBLIC_KEY="your-paddle-public-key"
PADDLE_SANDBOX=true
```

[Paddle のサンドボックス環境](#paddle-sandbox) を使用する場合は、`PADDLE_SANDBOX` 環境変数を `true` に設定する必要があります。アプリケーションを運用環境にデプロイし、Paddle のライブ ベンダー環境を使用している場合は、`PADDLE_SANDBOX` 変数を `false` に設定する必要があります。

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

デフォルトのCashier通貨は米ドル (USD) です。アプリケーションの `.env` ファイル内で `CASHIER_CURRENCY` 環境変数を定義することで、デフォルトの通貨を変更できます。

```ini
CASHIER_CURRENCY=EUR
```

レジの通貨を構成することに加えて、請求書に表示する金額の書式を設定するときに使用するロケールを指定することもできます。内部的には、Cashier は [PHPの`NumberFormatter`クラス](https://www.php.net/manual/en/class.numberformatter.php) を使用して通貨ロケールを設定します。

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> **警告**
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

<a name="core-concepts"></a>
## 中心となる概念 (Core Concepts)

<a name="pay-links"></a>
### 有料リンク

Paddle には、サブスクリプション状態の変更を実行するための広範な CRUD API がありません。したがって、Paddle とのほとんどの対話は、[チェックアウトウィジェット](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout) を通じて行われます。チェックアウト ウィジェットを表示する前に、Cashier を使用して「支払いリンク」を生成する必要があります。 「有料リンク」は、実行したい請求操作をチェックアウト ウィジェットに通知します。

    use App\Models\User;
    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $payLink = $request->user()->newSubscription('default', $premium = 34567)
            ->returnTo(route('home'))
            ->create();

        return view('billing', ['payLink' => $payLink]);
    });

Cashier には、`paddle-button` [Blade コンポーネント](/docs/{{version}}/blade#components) が含まれます。有料リンク URL を「小道具」としてこのコンポーネントに渡すことができます。このボタンをクリックすると、Paddle のチェックアウト ウィジェットが表示されます。

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

デフォルトでは、標準のPaddleスタイルのボタンが表示されます。 `data-theme="none"` 属性をコンポーネントに追加することで、すべてのPaddle スタイルを削除できます。

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="none">
    Subscribe
</x-paddle-button>
```

Paddle チェックアウト ウィジェットは非同期です。ユーザーがウィジェット内でサブスクリプションを作成または更新すると、Paddle はアプリケーション Webhook を送信し、ユーザーが独自のデータベース内のサブスクリプション状態を適切に更新できるようにします。したがって、Paddle からの状態変化に対応できるように [Webhook を設定する](#handling-paddle-webhooks) を適切に設定することが重要です。

有料リンクの詳細については、[有料リンクの生成に関する Paddle API ドキュメント](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) をご覧ください。

> **警告**
> サブスクリプションの状態が変更された後、対応する Webhook を受信するまでの遅延は通常最小限ですが、ユーザーのサブスクリプションがチェックアウト完了後にすぐに利用できない可能性があることを考慮して、アプリケーションでこれを考慮する必要があります。

<a name="manually-rendering-pay-links"></a>
#### 有料リンクの手動レンダリング

Laravel の組み込み Blade コンポーネントを使用せずに、有料リンクを手動でレンダリングすることもできます。まず、前の例で示したように有料リンク URL を生成します。

    $payLink = $request->user()->newSubscription('default', $premium = 34567)
        ->returnTo(route('home'))
        ->create();

次に、有料リンク URL を HTML の `a` 要素に添付するだけです。

    <a href="#!" class="ml-4 paddle_button" data-override="{{ $payLink }}">
        Paddle Checkout
    </a>

<a name="payments-requiring-additional-confirmation"></a>
#### 追加の確認が必要な支払い

支払いを確認して処理するために追加の検証が必要になる場合があります。これが発生すると、Paddle に支払い確認画面が表示されます。 Paddle または Cashier によって表示される支払い確認画面は、特定の銀行またはカード発行会社の支払いフローに合わせて調整することができ、追加のカード確認、一時的な少額請求、個別のデバイス認証、またはその他の形式の確認を含めることができます。

<a name="inline-checkout"></a>
### インラインチェックアウト

Paddle の「オーバーレイ」スタイルのチェックアウト ウィジェットを利用したくない場合、Paddle にはウィジェットをインラインで表示するオプションも用意されています。この方法では、チェックアウトの HTML フィールドを調整することはできませんが、アプリケーション内にウィジェットを埋め込むことができます。

インライン チェックアウトを簡単に開始できるように、Cashier には `paddle-checkout` Blade コンポーネントが含まれています。開始するには、[有料リンクを生成する](#pay-links) を実行し、有料リンクをコンポーネントの `override` 属性に渡す必要があります。

```blade
<x-paddle-checkout :override="$payLink" class="w-full" />
```

インライン チェックアウト コンポーネントの高さを調整するには、`height` 属性を Blade コンポーネントに渡すことができます。

```blade
<x-paddle-checkout :override="$payLink" class="w-full" height="500" />
```

<a name="inline-checkout-without-pay-links"></a>
#### 有料リンクなしのインライン チェックアウト

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

インライン チェックアウトで利用可能なオプションの詳細については、Paddle の [インラインチェックアウトに関するガイド](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout) および [パラメータリファレンス](https://developer.paddle.com/reference/paddle-js/parameters) を参照してください。

> **警告**
> カスタム オプションを指定するときに `passthrough` オプションも使用したい場合は、その値としてキー/値配列を指定する必要があります。 Cashier は配列の JSON 文字列への変換を自動的に処理します。さらに、`customer_id` パススルー オプションは、内部レジでの使用のために予約されています。

<a name="manually-rendering-an-inline-checkout"></a>
#### インライン チェックアウトを手動でレンダリングする

Laravel の組み込み Blade コンポーネントを使用せずに、インライン チェックアウトを手動でレンダリングすることもできます。まず、有料リンク URL [前の例で示したように](#pay-links) を生成します。

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
### ユーザーの識別

Stripe とは対照的に、Paddle ユーザーは Paddle アカウントごとに一意ではなく、Paddle 全体で一意です。このため、Paddle の API には現在、電子メール アドレスなどのユーザーの詳細を更新するメソッドが提供されていません。有料リンクを生成するとき、Paddle は `customer_email` パラメーターを使用してユーザーを識別します。サブスクリプションを作成するとき、Paddle はユーザーが提供した電子メールを既存の Paddle ユーザーと照合しようとします。

この動作を考慮して、Cashier と Paddle を使用するときに留意すべき重要な点がいくつかあります。まず、Cashier のサブスクリプションは同じアプリケーション ユーザーに関連付けられているとしても、**Paddle の内部システム内の異なるユーザーに関連付けられる可能性がある**ことに注意する必要があります。第 2 に、各サブスクリプションには独自の接続された支払い方法情報があり、Paddle の内部システム内で異なる電子メール アドレスを持つこともできます (サブスクリプションの作成時にどの電子メールがユーザーに割り当てられたかによって異なります)。

したがって、サブスクリプションを表示するときは、サブスクリプションごとにどの電子メール アドレスまたは支払い方法情報がサブスクリプションに関連付けられているかを常にユーザーに通知する必要があります。この情報の取得は、`Laravel\Paddle\Subscription` モデルによって提供される次のメソッドを使用して実行できます。

    $subscription = $user->subscription('default');

    $subscription->paddleEmail();
    $subscription->paymentMethod();
    $subscription->cardBrand();
    $subscription->cardLastFour();
    $subscription->cardExpirationDate();

現在、Paddle API を通じてユーザーの電子メール アドレスを変更する方法はありません。ユーザーが Paddle 内で自分の電子メール アドレスを更新したい場合、その唯一の方法は、Paddle カスタマー サポートに連絡することです。 Paddle と通信するときは、Paddle が正しいユーザーを更新できるように、サブスクリプションの `paddleEmail` 値を提供する必要があります。

<a name="prices"></a>
## 価格 (Prices)

Paddle を使用すると、通貨ごとに価格をカスタマイズできるため、基本的に国ごとに異なる価格を設定できます。 Cashier Paddle を使用すると、`productPrices` メソッドを使用して、特定の製品のすべての価格を取得できます。このメソッドは、価格を取得したい製品の製品 ID を受け入れます。

    use Laravel\Paddle\Cashier;

    $prices = Cashier::productPrices([123, 456]);

通貨はリクエストの IP アドレスに基づいて決定されます。ただし、オプションで特定の国を指定して次の価格を取得することもできます。

    use Laravel\Paddle\Cashier;

    $prices = Cashier::productPrices([123, 456], ['customer_country' => 'BE']);

価格を取得した後、必要に応じて価格を表示できます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

正味価格 (税抜) を表示し、税額を個別に表示することもできます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->net() }} (+ {{ $price->price()->tax() }} tax)</li>
    @endforeach
</ul>
```

サブスクリプション プランの価格を取得した場合は、初回価格と定期価格を個別に表示できます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - Initial: {{ $price->initialPrice()->gross() }} - Recurring: {{ $price->recurringPrice()->gross() }}</li>
    @endforeach
</ul>
```

詳細については、[価格についてはPaddleのAPIドキュメントを確認してください](https://developer.paddle.com/api-reference/checkout-api/prices/getprices) をご覧ください。

<a name="prices-customers"></a>
#### お客様

ユーザーがすでに顧客であり、その顧客に適用される価格を表示したい場合は、顧客インスタンスから直接価格を取得して表示できます。

    use App\Models\User;

    $prices = User::find(1)->productPrices([123, 456]);

内部的には、Cashier はユーザーの [`paddleCountry`メソッド](#customer-defaults) を使用して、ユーザーの通貨で価格を取得します。したがって、たとえば、米国に住んでいるユーザーには価格が米ドルで表示され、ベルギーのユーザーには価格がユーロで表示されます。一致する通貨が見つからない場合は、製品のデフォルトの通貨が使用されます。Paddle コントロール パネルで、製品またはサブスクリプション プランのすべての価格をカスタマイズできます。

<a name="prices-coupons"></a>
#### クーポン

クーポン割引後の価格を表示することもできます。 `productPrices` メソッドを呼び出すとき、クーポンはカンマ区切りの文字列として渡される場合があります。

    use Laravel\Paddle\Cashier;

    $prices = Cashier::productPrices([123, 456], [
        'coupons' => 'SUMMERSALE,20PERCENTOFF'
    ]);

次に、`price` メソッドを使用して計算された価格を表示します。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

`listPrice` メソッドを使用して、元の表示価格 (クーポン割引なし) を表示できます。

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->listPrice()->gross() }}</li>
    @endforeach
</ul>
```

> **警告**
> 価格 API を使用する場合、Paddle ではクーポンの適用を 1 回限りの購入製品にのみ許可し、サブスクリプション プランには適用できません。

<a name="customers"></a>
## お客様 (Customers)

<a name="customer-defaults"></a>
### 顧客のデフォルト

Cashier を使用すると、有料リンクを作成するときに顧客向けにいくつかの便利なデフォルトを定義できます。これらのデフォルトを設定すると、顧客の電子メール アドレス、国、郵便番号を事前に入力できるため、顧客はすぐにチェックアウト ウィジェットの支払い部分に進むことができます。これらのデフォルトは、請求可能なモデルで次のメソッドをオーバーライドすることで設定できます。

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

これらのデフォルトは、[有料リンク](#pay-links) を生成する Cashier のすべてのアクションに使用されます。

<a name="subscriptions"></a>
## 定期購入 (Subscriptions)

<a name="creating-subscriptions"></a>
### サブスクリプションの作成

サブスクリプションを作成するには、まず課金対象モデルのインスタンスをデータベースから取得します。これは通常、`App\Models\User` のインスタンスになります。モデル インスタンスを取得したら、`newSubscription` メソッドを使用してモデルのサブスクリプション有料リンクを作成できます。

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $payLink = $request->user()->newSubscription('default', $premium = 12345)
            ->returnTo(route('home'))
            ->create();

        return view('billing', ['payLink' => $payLink]);
    });

`newSubscription` メソッドに渡される最初の引数は、サブスクリプションの内部名である必要があります。アプリケーションが単一のサブスクリプションのみを提供する場合は、これを `default` または `primary` と呼びます。このサブスクリプション名はアプリケーション内部でのみ使用され、ユーザーに表示されることを意図したものではありません。また、スペースを含めることはできません。また、サブスクリプションの作成後に変更しないでください。 `newSubscription` メソッドに指定される 2 番目の引数は、ユーザーが購読している特定のプランです。この値は、Paddle のプランの識別子に対応する必要があります。 `returnTo` メソッドは、ユーザーがチェックアウトを正常に完了した後にリダイレクトされる URL を受け入れます。

`create` メソッドは、支払いボタンの生成に使用できる支払いリンクを作成します。支払いボタンは、Cashier Paddle に含まれる `paddle-button` [Blade コンポーネント](/docs/{{version}}/blade#components) を使用して生成できます。

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

ユーザーがチェックアウトを完了すると、`subscription_created` Webhook が Paddle からディスパッチされます。レジ担当者はこの Webhook を受信し、顧客のサブスクリプションをセットアップします。すべての Webhook が適切に受信され、アプリケーションによって処理されることを確認するには、[Webhook 処理のセットアップ](#handling-paddle-webhooks) が適切に設定されていることを確認してください。

<a name="additional-details"></a>
#### 追加の詳細

追加の顧客またはサブスクリプションの詳細を指定したい場合は、それらをキーと値のペアの配列として `create` メソッドに渡すことで指定できます。 Paddle でサポートされている追加フィールドの詳細については、[有料リンクの生成](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) にある Paddle のドキュメントを参照してください。

    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->create([
            'vat_number' => $vatNumber,
        ]);

<a name="subscriptions-coupons"></a>
#### クーポン

サブスクリプションの作成時にクーポンを適用したい場合は、`withCoupon` メソッドを使用できます。

    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->withCoupon('code')
        ->create();

<a name="metadata"></a>
#### メタデータ

`withMetadata` メソッドを使用してメタデータの配列を渡すこともできます。

    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->withMetadata(['key' => 'value'])
        ->create();

> **警告**
> メタデータを提供するときは、メタデータ キーとして `subscription_name` を使用しないでください。このキーは、Cashierによる内部使用のために予約されています。

<a name="checking-subscription-status"></a>
### 購読ステータスの確認

ユーザーがアプリケーションを購読すると、さまざまな便利な方法を使用してその購読ステータスを確認できます。まず、ユーザーがアクティブなサブスクリプションを持っている場合、サブスクリプションが現在試用期間内であっても、`subscribed` メソッドは `true` を返します。

    if ($user->subscribed('default')) {
        //
    }

`subscribed` メソッドも [ルートミドルウェア](/docs/{{version}}/middleware) の有力な候補となり、ユーザーのサブスクリプション ステータスに基づいてルートとコントローラへのアクセスをフィルタリングできます。

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

ユーザーがまだ試用期間内であるかどうかを確認したい場合は、`onTrial` メソッドを使用できます。このメソッドは、ユーザーがまだ試用期間中であることをユーザーに警告するかどうかを決定するのに役立ちます。

    if ($user->subscription('default')->onTrial()) {
        //
    }

`subscribedToPlan` メソッドは、特定のPaddle プラン ID に基づいて、ユーザーが特定のプランに加入しているかどうかを判断するために使用できます。この例では、ユーザーの `default` サブスクリプションが月次プランにアクティブにサブスクライブされているかどうかを判断します。

    if ($user->subscribedToPlan($monthly = 12345, 'default')) {
        //
    }

配列を `subscribedToPlan` メソッドに渡すことによって、ユーザーの `default` サブスクリプションが月次プランまたは年次プランにアクティブにサブスクライブされているかどうかを判断できます。

    if ($user->subscribedToPlan([$monthly = 12345, $yearly = 54321], 'default')) {
        //
    }

`recurring` メソッドは、ユーザーが現在購読中であり、試用期間中でないかどうかを判断するために使用できます。

    if ($user->subscription('default')->recurring()) {
        //
    }

<a name="cancelled-subscription-status"></a>
#### キャンセルされたサブスクリプションのステータス

ユーザーがかつてはアクティブなサブスクライバだったが、サブスクリプションをキャンセルしたかどうかを確認するには、`cancelled` メソッドを使用できます。

    if ($user->subscription('default')->cancelled()) {
        //
    }

また、ユーザーがサブスクリプションをキャンセルしたが、サブスクリプションが完全に期限切れになるまでまだ「猶予期間」中であるかどうかを判断することもできます。たとえば、ユーザーが元々 3 月 10 日に期限切れになる予定だったサブスクリプションを 3 月 5 日にキャンセルした場合、ユーザーは 3 月 10 日まで「猶予期間」に入ります。この間も、`subscribed` メソッドは `true` を返すことに注意してください。

    if ($user->subscription('default')->onGracePeriod()) {
        //
    }

ユーザーがサブスクリプションをキャンセルし、「猶予期間」に入っていないかどうかを確認するには、`ended` メソッドを使用できます。

    if ($user->subscription('default')->ended()) {
        //
    }

<a name="past-due-status"></a>
#### 期限超過ステータス

サブスクリプションの支払いが失敗した場合、`past_due` としてマークされます。サブスクリプションがこの状態にある場合、顧客が支払い情報を更新するまでアクティブになりません。サブスクリプション インスタンスの `pastDue` メソッドを使用して、サブスクリプションの期限が過ぎているかどうかを確認できます。

    if ($user->subscription('default')->pastDue()) {
        //
    }

サブスクリプションの期限を過ぎた場合は、ユーザーに [支払い情報を更新する](#updating-payment-information) を指示する必要があります。 [Paddle のサブスクリプション設定](https://vendors.paddle.com/subscription-settings) で期限を過ぎたサブスクリプションをどのように処理するかを構成できます。

サブスクリプションが `past_due` の場合でもアクティブであると見なされたい場合は、Cashier が提供する `keepPastDueSubscriptionsActive` メソッドを使用できます。通常、このメソッドは、`AppServiceProvider` の `register` メソッドで呼び出す必要があります。

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

> **警告**
> サブスクリプションが `past_due` 状態にある場合、支払い情報が更新されるまで変更することはできません。したがって、サブスクリプションが `past_due` 状態にある場合、`swap` メソッドと `updateQuantity` メソッドは例外をスローします。

<a name="subscription-scopes"></a>
#### サブスクリプションの範囲

ほとんどのサブスクリプション状態はクエリ スコープとしても使用できるため、特定の状態にあるサブスクリプションについてデータベースを簡単にクエリできます。

    // Get all active subscriptions...
    $subscriptions = Subscription::query()->active()->get();

    // Get all of the cancelled subscriptions for a user...
    $subscriptions = $user->subscriptions()->cancelled()->get();

利用可能なスコープの完全なリストは以下で入手できます。

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

<a name="subscription-single-charges"></a>
### サブスクリプションの単一料金

サブスクリプションの単一料金を使用すると、サブスクリプションに加えて 1 回限りの料金をサブスクライバに請求できます。

    $response = $user->subscription('default')->charge(12.99, 'Support Add-on');

[単一料金](#single-charges) とは対照的に、この方法では、顧客が保存した支払い方法にすぐにサブスクリプションの料金が請求されます。請求額は常にサブスクリプションの通貨で定義する必要があります。

<a name="updating-payment-information"></a>
### 支払い情報の更新

Paddle は常にサブスクリプションごとに支払い方法を保存します。サブスクリプションのデフォルトの支払い方法を更新する場合は、最初にサブスクリプション モデルで `updateUrl` メソッドを使用してサブスクリプションの「更新 URL」を生成する必要があります。

    use App\Models\User;

    $user = User::find(1);

    $updateUrl = $user->subscription('default')->updateUrl();

次に、生成された URL を Cashier が提供する `paddle-button` Blade コンポーネントと組み合わせて使用​​すると、ユーザーがPaddle ウィジェットを開始して支払い情報を更新できるようになります。

```html
<x-paddle-button :url="$updateUrl" class="px-8 py-4">
    Update Card
</x-paddle-button>
```

ユーザーが情報の更新を完了すると、`subscription_updated` Webhook が Paddle によって送出され、サブスクリプションの詳細がアプリケーションのデータベースで更新されます。

<a name="changing-plans"></a>
### プランの変更

ユーザーがアプリケーションを購読した後、新しい購読プランへの変更を希望する場合があります。ユーザーのサブスクリプション プランを更新するには、Paddle プランの識別子をサブスクリプションの `swap` メソッドに渡す必要があります。

    use App\Models\User;

    $user = User::find(1);

    $user->subscription('default')->swap($premium = 34567);

プランを交換して、次の請求サイクルを待たずにすぐにユーザーに請求を行いたい場合は、`swapAndInvoice` メソッドを使用できます。

    $user = User::find(1);

    $user->subscription('default')->swapAndInvoice($premium = 34567);

> **警告**
> 試用期間中はプランを切り替えることはできません。この制限に関する追加情報については、[Paddle のドキュメント](https://developer.paddle.com/api-reference/subscription-api/users/updateuser#usage-notes) を参照してください。

<a name="prorations"></a>
#### 按分

デフォルトでは、Paddle はプラン間を切り替えるときに料金を日割り計算します。 `noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションを更新できます。

    $user->subscription('default')->noProrate()->swap($premium = 34567);

<a name="subscription-quantity"></a>
### 購読数量

サブスクリプションは「数量」の影響を受ける場合があります。たとえば、プロジェクト管理アプリケーションでは、プロジェクトごとに月額 10 ドルを請求する場合があります。サブスクリプションの数量を簡単に増減するには、`incrementQuantity` メソッドと `decrementQuantity` メソッドを使用します。

    $user = User::find(1);

    $user->subscription('default')->incrementQuantity();

    // Add five to the subscription's current quantity...
    $user->subscription('default')->incrementQuantity(5);

    $user->subscription('default')->decrementQuantity();

    // Subtract five from the subscription's current quantity...
    $user->subscription('default')->decrementQuantity(5);

あるいは、`updateQuantity` メソッドを使用して特定の数量を設定することもできます。

    $user->subscription('default')->updateQuantity(10);

`noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションの数量を更新できます。

    $user->subscription('default')->noProrate()->updateQuantity(10);

<a name="subscription-modifiers"></a>
### サブスクリプション修飾子

サブスクリプション修飾子を使用すると、[従量制課金](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers) を実装したり、アドオンを使用してサブスクリプションを拡張したりできます。

たとえば、標準サブスクリプションで「プレミアム サポート」アドオンを提供したい場合があります。この修飾子は次のように作成できます。

    $modifier = $user->subscription('default')->newModifier(12.99)->create();

上の例では、12.99 ドルのアドオンをサブスクリプションに追加します。デフォルトでは、この料金はサブスクリプションに設定した間隔ごとに繰り返し発生します。必要に応じて、モディファイアの `description` メソッドを使用して、モディファイアに読みやすい説明を追加できます。

    $modifier = $user->subscription('default')->newModifier(12.99)
        ->description('Premium Support')
        ->create();

修飾子を使用して従量課金を実装する方法を説明するために、ユーザーが送信した SMS メッセージごとにアプリケーションが料金を請求することを想像してください。まず、Paddle ダッシュボードで $0 プランを作成する必要があります。ユーザーがこのプランにサブスクライブすると、個々の料金を表す修飾子をサブスクリプションに追加できます。

    $modifier = $user->subscription('default')->newModifier(0.99)
        ->description('New text message')
        ->oneTime()
        ->create();

ご覧のとおり、このモディファイアを作成するときに `oneTime` メソッドを呼び出しました。この方法により、モディファイアは 1 回だけ請求され、請求間隔ごとに繰り返されなくなります。

<a name="retrieving-modifiers"></a>
#### 修飾子の取得

`modifiers` メソッドを使用して、サブスクリプションのすべての修飾子のリストを取得できます。

    $modifiers = $user->subscription('default')->modifiers();

    foreach ($modifiers as $modifier) {
        $modifier->amount(); // $0.99
        $modifier->description; // New text message.
    }

<a name="deleting-modifiers"></a>
#### モディファイアの削除

修飾子は、`Laravel\Paddle\Modifier` インスタンスで `delete` メソッドを呼び出すことで削除できます。

    $modifier->delete();

<a name="multiple-subscriptions"></a>
### 複数のサブスクリプション

Paddle を使用すると、顧客は同時に複数のサブスクリプションを持つことができます。たとえば、水泳のサブスクリプションとウェイトリフティングのサブスクリプションを提供するジムを運営しており、各サブスクリプションの価格が異なる場合があります。もちろん、顧客はどちらかまたは両方のプランに加入できる必要があります。

アプリケーションがサブスクリプションを作成するとき、`newSubscription` メソッドにサブスクリプションの名前を指定できます。名前には、ユーザーが開始するサブスクリプションのタイプを表す任意の文字列を指定できます。

    use Illuminate\Http\Request;

    Route::post('/swimming/subscribe', function (Request $request) {
        $request->user()
            ->newSubscription('swimming', $swimmingMonthly = 12345)
            ->create($request->paymentMethodId);

        // ...
    });

この例では、顧客に対して毎月の水泳サブスクリプションを開始しました。ただし、後で年間サブスクリプションに切り替えたい場合もあります。顧客のサブスクリプションを調整するときは、`swimming` サブスクリプションの価格を単純に交換できます。

    $user->subscription('swimming')->swap($swimmingYearly = 34567);

もちろん、サブスクリプションを完全にキャンセルすることもできます。

    $user->subscription('swimming')->cancel();

<a name="pausing-subscriptions"></a>
### サブスクリプションの一時停止

サブスクリプションを一時停止するには、ユーザーのサブスクリプションで `pause` メソッドを呼び出します。

    $user->subscription('default')->pause();

サブスクリプションが一時停止されると、Cashier はデータベースに `paused_from` 列を自動的に設定します。この列は、`paused` メソッドが `true` を返し始める時期を知るために使用されます。たとえば、顧客が 3 月 1 日にサブスクリプションを一時停止したが、そのサブスクリプションが 3 月 5 日まで繰り返されるようにスケジュールされていなかった場合、`paused` メソッドは 3 月 5 日まで `false` を返し続けます。これは、ユーザーが通常、請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているために行われます。

ユーザーがサブスクリプションを一時停止しているが、まだ「猶予期間」中であるかどうかを、`onPausedGracePeriod` メソッドを使用して判断できます。

    if ($user->subscription('default')->onPausedGracePeriod()) {
        //
    }

一時停止したサブスクリプションを再開するには、ユーザーのサブスクリプションで `unpause` メソッドを呼び出すことができます。

    $user->subscription('default')->unpause();

> **警告**
> 一時停止中はサブスクリプションを変更できません。別のプランに切り替えたり、数量を更新したりする場合は、まずサブスクリプションを再開する必要があります。

<a name="cancelling-subscriptions"></a>
### 定期購入のキャンセル

サブスクリプションをキャンセルするには、ユーザーのサブスクリプションで `cancel` メソッドを呼び出します。

    $user->subscription('default')->cancel();

サブスクリプションがキャンセルされると、Cashier はデータベースに `ends_at` 列を自動的に設定します。この列は、`subscribed` メソッドが `false` を返し始める時期を知るために使用されます。たとえば、顧客が 3 月 1 日にサブスクリプションをキャンセルしたが、そのサブスクリプションが 3 月 5 日まで終了する予定ではなかった場合、`subscribed` メソッドは 3 月 5 日まで `true` を返し続けます。これは、ユーザーが通常、請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているために行われます。

`onGracePeriod` メソッドを使用して、ユーザーがサブスクリプションをキャンセルしたがまだ「猶予期間」中であるかどうかを確認できます。

    if ($user->subscription('default')->onGracePeriod()) {
        //
    }

サブスクリプションをすぐにキャンセルしたい場合は、ユーザーのサブスクリプションで `cancelNow` メソッドを呼び出すことができます。

    $user->subscription('default')->cancelNow();

> **警告**
> Paddle のサブスクリプションは、キャンセル後に再開することはできません。顧客がサブスクリプションの再開を希望する場合は、新しいサブスクリプションを購読する必要があります。

<a name="subscription-trials"></a>
## サブスクリプショントライアル (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 支払い方法を前払いする場合

> **警告**
> 事前に支払い方法の詳細を試用して収集している間、Paddle はプランの交換や数量の更新などのサブスクリプションの変更を防ぎます。試用期間中に顧客がプランを交換できるようにするには、サブスクリプションをキャンセルして再作成する必要があります。

支払い方法情報を事前に収集しながら顧客に試用期間を提供したい場合は、サブスクリプション有料リンクを作成するときに `trialDays` メソッドを使用する必要があります。

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $payLink = $request->user()->newSubscription('default', $monthly = 12345)
                    ->returnTo(route('home'))
                    ->trialDays(10)
                    ->create();

        return view('billing', ['payLink' => $payLink]);
    });

このメソッドは、アプリケーションのデータベース内のサブスクリプション レコードに試用期間の終了日を設定し、この日以降になるまで顧客への請求を開始しないように Paddle に指示します。

> **警告**
> 試用期間の終了日までに顧客のサブスクリプションがキャンセルされなかった場合、試用期間が終了するとすぐに料金が請求されるため、ユーザーに試用期間の終了日を必ず通知する必要があります。

ユーザー インスタンスの `onTrial` メソッドまたはサブスクリプション インスタンスの `onTrial` メソッドを使用して、ユーザーが試用期間内かどうかを判断できます。以下の 2 つの例は同等です。

    if ($user->onTrial('default')) {
        //
    }

    if ($user->subscription('default')->onTrial()) {
        //
    }

既存の試用版の有効期限が切れているかどうかを確認するには、`hasExpiredTrial` メソッドを使用できます。

    if ($user->hasExpiredTrial('default')) {
        //
    }

    if ($user->subscription('default')->hasExpiredTrial()) {
        //
    }

<a name="defining-trial-days-in-paddle-cashier"></a>
#### Paddle/Cashierでの試用日の定義

Paddle ダッシュボードでプランの試用日数を定義することも、Cashier を使用して常に明示的に試用日数を渡すこともできます。 Paddle でプランの試用日を定義することを選択した場合は、`trialDays(0)` メソッドを明示的に呼び出さない限り、過去にサブスクリプションを持っていた顧客の新しいサブスクリプションを含む、新しいサブスクリプションには常に試用期間が与えられることに注意する必要があります。

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

ユーザーの実際のサブスクリプションを作成する準備ができたら、通常どおり `newSubscription` メソッドを使用できます。

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $payLink = $user->newSubscription('default', $monthly = 12345)
            ->returnTo(route('home'))
            ->create();

        return view('billing', ['payLink' => $payLink]);
    });

ユーザーの試用終了日を取得するには、`trialEndsAt` メソッドを使用できます。このメソッドは、ユーザーが試用中の場合は Carbon date インスタンスを返し、試用中でない場合は `null` を返します。デフォルト以外の特定のサブスクリプションの試用終了日を取得したい場合は、オプションのサブスクリプション名パラメーターを渡すこともできます。

    if ($user->onTrial()) {
        $trialEndsAt = $user->trialEndsAt('main');
    }

ユーザーが「一般的な」試用期間内であり、実際のサブスクリプションをまだ作成していないことを具体的に知りたい場合は、`onGenericTrial` メソッドを使用できます。

    if ($user->onGenericTrial()) {
        // User is within their "generic" trial period...
    }

> **警告**
> Paddle サブスクリプションの作成後に試用期間を延長または変更する方法はありません。

<a name="handling-paddle-webhooks"></a>
## Paddle Webhook の処理 (Handling Paddle Webhooks)

Paddle は、Webhook 経由でさまざまなイベントをアプリケーションに通知できます。デフォルトでは、Cashier の Webhook コントローラを指すルートが Cashier サービスプロバイダによって登録されます。このコントローラは、受信したすべての Webhook リクエストを処理します。

デフォルトでは、このコントローラは、失敗した請求 ([Paddle督促設定で定義されている通り](https://vendors.paddle.com/recover-settings#dunning-form-id)) が多すぎるサブスクリプションのキャンセル、サブスクリプションの更新、および支払い方法の変更を自動的に処理します。ただし、すぐにわかりますが、このコントローラを拡張して、任意の Paddle Webhook イベントを処理できます。

アプリケーションが Paddle Webhook を処理できることを確認するには、必ず [Paddle コントロールパネルでWebhook URLを設定します。](https://vendors.paddle.com/alerts-webhooks) を実行してください。デフォルトでは、Cashier の Webhook コントローラは `/paddle/webhook` URL パスに応答します。Paddle コントロール パネルで有効にする必要があるすべての Webhook の完全なリストは次のとおりです。

- サブスクリプションが作成されました
- サブスクリプションが更新されました
- サブスクリプションがキャンセルされました
- 支払いが完了しました
- 定期購入の支払いが完了しました

> **警告**
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

どちらのイベントにも、Paddle Webhook の完全なペイロードが含まれています。たとえば、`invoice.payment_succeeded` Webhook を処理したい場合は、イベントを処理する [listener](/docs/{{version}}/events#defining-listeners) を登録できます。

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

- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`

</div>

アプリケーションの `.env` ファイルで `CASHIER_WEBHOOK` 環境変数を定義することで、デフォルトの組み込み Webhook ルートをオーバーライドすることもできます。この値は Webhook ルートの完全な URL である必要があり、Paddle コントロール パネルで設定された URL と一致する必要があります。

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### Webhook 署名の検証

Webhook を保護するには、[Paddle の Webhook 署名](https://developer.paddle.com/webhook-reference/verifying-webhooks) を使用できます。便宜上、Cashier には、受信した Paddle Webhook リクエストが有効であることを検証するミドルウェアが自動的に組み込まれています。

Webhook 検証を有効にするには、`PADDLE_PUBLIC_KEY` 環境変数がアプリケーションの `.env` ファイルで定義されていることを確認してください。公開キーは、Paddle アカウントのダッシュボードから取得できます。

<a name="single-charges"></a>
## シングルチャージ (Single Charges)

<a name="simple-charge"></a>
### かんたんチャージ

顧客に対して 1 回限りの請求を行う場合は、請求可能なモデル インスタンスで `charge` メソッドを使用して、請求用の有料リンクを生成できます。 `charge` メソッドは、最初の引数として請求金額 (浮動小数点数) を受け入れ、2 番目の引数として請求の説明を受け入れます。

    use Illuminate\Http\Request;

    Route::get('/store', function (Request $request) {
        return view('store', [
            'payLink' => $user->charge(12.99, 'Action Figure')
        ]);
    });

有料リンクを生成した後、Cashier が提供する `paddle-button` Blade コンポーネントを使用して、ユーザーがPaddle ウィジェットを開始してチャージを完了できるようにすることができます。

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`charge` メソッドは 3 番目の引数として配列を受け入れ、基になるPaddle有料リンクの作成に必要なオプションを渡すことができます。料金作成時に利用できるオプションの詳細については、[Paddle のドキュメント](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) を参照してください。

    $payLink = $user->charge(12.99, 'Action Figure', [
        'custom_option' => $value,
    ]);

料金は、`cashier.currency` 構成オプションで指定された通貨で発生します。デフォルトでは、これは USD に設定されています。アプリケーションの `.env` ファイルで `CASHIER_CURRENCY` 環境変数を定義することで、デフォルトの通貨をオーバーライドできます。

```ini
CASHIER_CURRENCY=EUR
```

Paddle の動的価格マッチング システムを使用して [通貨ごとの価格を上書きする](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink#price-overrides) することもできます。これを行うには、固定金額の代わりに価格の配列を渡します。

    $payLink = $user->charge([
        'USD:19.99',
        'EUR:15.99',
    ], 'Action Figure');

<a name="charging-products"></a>
### 充電製品

Paddle 内で構成された特定の製品に対して 1 回限りの請求を行いたい場合は、請求可能なモデル インスタンスで `chargeProduct` メソッドを使用して有料リンクを生成できます。

    use Illuminate\Http\Request;

    Route::get('/store', function (Request $request) {
        return view('store', [
            'payLink' => $request->user()->chargeProduct($productId = 123)
        ]);
    });

次に、`paddle-button` コンポーネントへの有料リンクを提供して、ユーザーがPaddle ウィジェットを初期化できるようにします。

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`chargeProduct` メソッドは 2 番目の引数として配列を受け入れ、基になるPaddle有料リンクの作成に必要なオプションを渡すことができます。料金作成時に利用できるオプションについては、[Paddle のドキュメント](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) を参照してください。

    $payLink = $user->chargeProduct($productId, [
        'custom_option' => $value,
    ]);

<a name="refunding-orders"></a>
### 注文の払い戻し

Paddle の注文を返金する必要がある場合は、`refund` メソッドを使用できます。このメソッドは、最初の引数としてPaddle注文 ID を受け入れます。 `receipts` メソッドを使用して、特定の請求可能モデルの領収書を取得できます。

    use App\Models\User;

    $user = User::find(1);

    $receipt = $user->receipts()->first();

    $refundRequestId = $user->refund($receipt->order_id);

オプションで、特定の返金金額と返金の理由を指定できます。

    $receipt = $user->receipts()->first();

    $refundRequestId = $user->refund(
        $receipt->order_id, 5.00, 'Unused product time'
    );

> **注記**
> Paddle サポートに連絡するときに、`$refundRequestId` を返金の参照として使用できます。

<a name="receipts"></a>
## 領収書 (Receipts)

`receipts` プロパティを使用して、請求可能なモデルの領収書の配列を簡単に取得できます。

    use App\Models\User;

    $user = User::find(1);

    $receipts = $user->receipts;

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
### 過去および今後の支払い

`lastPayment` メソッドと `nextPayment` メソッドを使用して、定期購読に対する顧客の過去または今後の支払いを取得して表示できます。

    use App\Models\User;

    $user = User::find(1);

    $subscription = $user->subscription('default');

    $lastPayment = $subscription->lastPayment();
    $nextPayment = $subscription->nextPayment();

これらのメソッドは両方とも、`Laravel\Paddle\Payment` のインスタンスを返します。ただし、請求サイクルが終了すると (サブスクリプションがキャンセルされた場合など)、`nextPayment` は `null` を返します。

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="handling-failed-payments"></a>
## 失敗した支払いの処理 (Handling Failed Payments)

カードの有効期限が切れたり、カードの残高が不足したりするなど、さまざまな理由でサブスクリプションの支払いが失敗します。このような場合は、Paddle に支払い失敗の処理を任せることをお勧めします。具体的には、Paddle ダッシュボードで [Paddle の自動請求メールをセットアップする](https://vendors.paddle.com/subscription-settings) を行うことができます。

あるいは、Cashier によってディスパッチされる `WebhookReceived` イベントを介して、`subscription_payment_failed` Paddle イベントの [listening](/docs/{{version}}/events) により、より正確なカスタマイズを実行することもできます。また、Paddle ダッシュボードの Webhook 設定で「サブスクリプションの支払いに失敗しました」オプションが有効になっていることを確認する必要があります。

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

リスナを定義したら、それをアプリケーションの `EventServiceProvider` 内に登録する必要があります。

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

<a name="testing"></a>
## テスト (Testing)

テスト中に、請求フローを手動でテストして、統合が期待どおりに機能することを確認する必要があります。

CI 環境内で実行されるテストを含む自動テストの場合、[LaravelのHTTPクライアント](/docs/{{version}}/http-client#testing) を使用して Paddle に対して行われた HTTP 呼び出しを偽装できます。これは Paddle からの実際の応答をテストしませんが、実際に Paddle の API を呼び出さずにアプリケーションをテストする方法を提供します。

