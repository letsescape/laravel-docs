# Laravel Cashier (Stripe) (Laravel Cashier (Stripe))

- [Introduction](#introduction)
- [Cashierのアップグレード](#upgrading-cashier)
- [Installation](#installation)
- [Configuration](#configuration)
    - [課金対象モデル](#billable-model)
    - [APIキー](#api-keys)
    - [通貨構成](#currency-configuration)
    - [税の構成](#tax-configuration)
    - [Logging](#logging)
    - [カスタムモデルの使用](#using-custom-models)
- [Quickstart](#quickstart)
    - [製品の販売](#quickstart-selling-products)
    - [サブスクリプションの販売](#quickstart-selling-subscriptions)
- [Customers](#customers)
    - [顧客の取得](#retrieving-customers)
    - [顧客の創造](#creating-customers)
    - [顧客の更新](#updating-customers)
    - [Balances](#balances)
    - [納税者番号](#tax-ids)
    - [Stripe と顧客データを同期する](#syncing-customer-data-with-stripe)
    - [請求ポータル](#billing-portal)
- [支払い方法](#payment-methods)
    - [支払い方法の保存](#storing-payment-methods)
    - [支払い方法の取得](#retrieving-payment-methods)
    - [支払い方法の有無](#payment-method-presence)
    - [デフォルトの支払い方法の更新](#updating-the-default-payment-method)
    - [支払い方法の追加](#adding-payment-methods)
    - [支払い方法の削除](#deleting-payment-methods)
- [Subscriptions](#subscriptions)
    - [サブスクリプションの作成](#creating-subscriptions)
    - [購読ステータスの確認](#checking-subscription-status)
    - [価格の変更](#changing-prices)
    - [購読数量](#subscription-quantity)
    - [複数の製品のサブスクリプション](#subscriptions-with-multiple-products)
    - [複数のサブスクリプション](#multiple-subscriptions)
    - [使用量ベースの請求](#usage-based-billing)
    - [購読税](#subscription-taxes)
    - [サブスクリプションアンカー日](#subscription-anchor-date)
    - [定期購入のキャンセル](#cancelling-subscriptions)
    - [サブスクリプションの再開](#resuming-subscriptions)
- [サブスクリプショントライアル](#subscription-trials)
    - [支払い方法を前払いする場合](#with-payment-method-up-front)
    - [前払いの支払い方法なし](#without-payment-method-up-front)
    - [トライアルの延長](#extending-trials)
- [Stripe Webhook の処理](#handling-stripe-webhooks)
    - [Webhook イベント ハンドラーの定義](#defining-webhook-event-handlers)
    - [Webhook 署名の検証](#verifying-webhook-signatures)
- [シングルチャージ](#single-charges)
    - [かんたんチャージ](#simple-charge)
    - [請求書による請求](#charge-with-invoice)
    - [支払い意図の作成](#creating-payment-intents)
    - [払戻手数料](#refunding-charges)
- [Invoices](#invoices)
    - [請求書の取得](#retrieving-invoices)
    - [今後の請求書](#upcoming-invoices)
    - [サブスクリプション請求書のプレビュー](#previewing-subscription-invoices)
    - [請求書 PDF の生成](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [製品チェックアウト](#product-checkouts)
    - [シングルチャージチェックアウト](#single-charge-checkouts)
    - [サブスクリプションのチェックアウト](#subscription-checkouts)
    - [納税者番号の収集](#collecting-tax-ids)
    - [ゲストのチェックアウト](#guest-checkouts)
- [失敗した支払いの処理](#handling-failed-payments)
    - [支払いの確認](#confirming-payments)
- [強力な顧客認証 (SCA)](#strong-customer-authentication)
    - [追加の確認が必要な支払い](#payments-requiring-additional-confirmation)
    - [セッション外の支払い通知](#off-session-payment-notifications)
- [StripeSDK](#stripe-sdk)
- [Testing](#testing)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe) は、[Stripe の](https://stripe.com) サブスクリプション請求サービスへの表現力豊かで流暢なインターフェイスを提供します。あなたが書くのを恐れている定型的なサブスクリプション請求コードのほぼすべてを処理します。基本的なサブスクリプション管理に加えて、Cashier はクーポン、サブスクリプションの交換、サブスクリプションの「数量」、キャンセル猶予期間を処理し、請求書の PDF を生成することもできます。

<a name="upgrading-cashier"></a>
## Cashierのアップグレード (Upgrading Cashier)

Cashier の新しいバージョンにアップグレードする場合は、[アップグレードガイド](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md) を注意深く確認することが重要です。

> [!WARNING]
> 重大な変更を防ぐために、Cashier は固定の Stripe API バージョンを使用します。 Cashier 16 は、Stripe API バージョン `2025-06-30.basil` を利用します。 Stripe API バージョンは、Stripe の新しい機能と改善を利用するためにマイナー リリースで更新されます。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを使用して Stripe の Cashier パッケージをインストールします。

```shell
composer require laravel/cashier
```

パッケージをインストールした後、`vendor:publish` Artisan コマンドを使用して Cashier の移行を公開します。

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

次に、データベースを移行します。

```shell
php artisan migrate
```

Cashier の移行により、`users` テーブルにいくつかの列が追加されます。また、顧客のすべてのサブスクリプションを保持する新しい `subscriptions` テーブルと、複数の価格のサブスクリプション用の `subscription_items` テーブルも作成されます。

必要に応じて、`vendor:publish` Artisan コマンドを使用して、Cashier の構成ファイルを公開することもできます。

```shell
php artisan vendor:publish --tag="cashier-config"
```

最後に、Cashier がすべての Stripe イベントを適切に処理できるようにするには、[Cashier の Webhook 処理を構成する](#handling-stripe-webhooks) を忘れないでください。

> [!WARNING]
> Stripe では、Stripe 識別子の格納に使用される列では大文字と小文字を区別することをお勧めします。したがって、MySQL を使用する場合は、`stripe_id` 列の列照合順序が `utf8_bin` に設定されていることを確認する必要があります。これに関する詳細については、[Stripe のドキュメント](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible) を参照してください。

<a name="configuration"></a>
## 構成 (Configuration)

<a name="billable-model"></a>
### 課金対象モデル

Cashier を使用する前に、`Billable` 特性を請求可能モデル定義に追加します。通常、これは `App\Models\User` モデルになります。この特性は、サブスクリプションの作成、クーポンの適用、支払い方法情報の更新などの一般的な請求タスクを実行できるようにするさまざまなメソッドを提供します。

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

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
> Laravel が提供する `App\Models\User` モデル以外のモデルを使用している場合は、提供される [Cashierの移行](#installation) を公開し、代替モデルのテーブル名と一致するように変更する必要があります。

<a name="api-keys"></a>
### APIキー

次に、アプリケーションの `.env` ファイルで Stripe API キーを構成する必要があります。 Stripe API キーは、Stripe コントロール パネルから取得できます。

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 環境変数がアプリケーションの `.env` ファイルで定義されていることを確認する必要があります。この変数は、受信 Webhook が実際に Stripe からのものであることを確認するために使用されます。

<a name="currency-configuration"></a>
### 通貨構成

デフォルトのCashier通貨は米ドル (USD) です。アプリケーションの `.env` ファイル内で `CASHIER_CURRENCY` 環境変数を設定することで、デフォルトの通貨を変更できます。

```ini
CASHIER_CURRENCY=eur
```

レジの通貨を構成することに加えて、請求書に表示する金額の書式を設定するときに使用するロケールを指定することもできます。内部的には、Cashier は [PHPの`NumberFormatter`クラス](https://www.php.net/manual/en/class.numberformatter.php) を使用して通貨ロケールを設定します。

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 以外のロケールを使用するには、`ext-intl` PHP 拡張機能がサーバーにインストールされ、構成されていることを確認してください。

<a name="tax-configuration"></a>
### 税の構成

[Stripe税](https://stripe.com/tax) のおかげで、Stripe によって生成されたすべての請求書の税金を自動的に計算することができます。自動税金計算を有効にするには、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドで `calculateTaxes` メソッドを呼び出します。

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

税計算が有効になると、新しいサブスクリプションと生成される 1 回限りの請求書で自動的に税計算が行われるようになります。

この機能が適切に動作するには、顧客の名前、住所、納税者番号などの請求詳細が Stripe に同期される必要があります。これを実現するには、Cashier が提供する [顧客データの同期](#syncing-customer-data-with-stripe) および [納税者番号](#tax-ids) メソッドを使用できます。

<a name="logging"></a>
### ロギング

Cashier を使用すると、致命的な Stripe エラーを記録するときに使用するログ チャネルを指定できます。アプリケーションの `.env` ファイル内で `CASHIER_LOGGER` 環境変数を定義することで、ログ チャネルを指定できます。

```ini
CASHIER_LOGGER=stack
```

Stripe への API 呼び出しによって生成された例外は、アプリケーションのデフォルトのログ チャネルを通じて記録されます。

<a name="using-custom-models"></a>
### カスタムモデルの使用

独自のモデルを定義し、対応する Cashier モデルを拡張することで、Cashier によって内部的に使用されるモデルを自由に拡張できます。

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

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
## クイックスタート (Quickstart)

<a name="quickstart-selling-products"></a>
### 製品の販売

> [!NOTE]
> Stripe Checkout を利用する前に、Stripe ダッシュボードで固定価格の製品を定義する必要があります。さらに、[Cashier の Webhook 処理を構成する](#handling-stripe-webhooks) を実行する必要があります。

アプリケーション経由で製品やサブスクリプションの請求を行うのは、威圧的な場合があります。ただし、Cashier と [Stripeチェックアウト](https://stripe.com/payments/checkout) のおかげで、最新の堅牢な支払い統合を簡単に構築できます。

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

上の例でわかるように、Cashierが提供する `checkout` メソッドを利用して、顧客を特定の「価格識別子」の Stripe Checkout にリダイレクトします。 Stripe を使用する場合、「価格」は [特定の製品に対して定義された価格](https://stripe.com/docs/products-prices/how-products-and-prices-work) を指します。

必要に応じて、`checkout` メソッドは Stripe に顧客を自動的に作成し、その Stripe 顧客レコードをアプリケーションのデータベース内の対応するユーザーに接続します。チェックアウト セッションが完了すると、顧客は専用の成功ページまたはキャンセル ページにリダイレクトされ、そこで顧客に情報メッセージを表示できます。

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout へのメタデータの提供

製品を販売する場合、独自のアプリケーションで定義された `Cart` および `Order` モデルを介して、完了した注文と購入した製品を追跡するのが一般的です。購入を完了するために顧客を Stripe Checkout にリダイレクトする場合、顧客がアプリケーションにリダイレクトされて戻ったときに、完了した購入を対応する注文に関連付けることができるように、既存の注文 ID を提供することが必要になる場合があります。

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

上の例でわかるように、ユーザーがチェックアウト プロセスを開始すると、カート/注文に関連付けられたすべての Stripe 価格識別子が `checkout` メソッドに提供されます。もちろん、アプリケーションは、顧客がこれらの商品を追加したときに、これらの商品を「ショッピング カート」または注文に関連付ける責任があります。また、`metadata` 配列を介して注文の ID を Stripe Checkout セッションに提供します。最後に、`CHECKOUT_SESSION_ID` テンプレート変数をチェックアウト成功ルートに追加しました。 Stripe が顧客をアプリケーションにリダイレクトすると、このテンプレート変数にはチェックアウト セッション ID が自動的に設定されます。

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

[チェックアウト セッション オブジェクトに含まれるデータ](https://stripe.com/docs/api/checkout/sessions/object) の詳細については、Stripe のドキュメントを参照してください。

<a name="quickstart-selling-subscriptions"></a>
### サブスクリプションの販売

> [!NOTE]
> Stripe Checkout を利用する前に、Stripe ダッシュボードで固定価格の製品を定義する必要があります。さらに、[Cashier の Webhook 処理を構成する](#handling-stripe-webhooks) を実行する必要があります。

アプリケーション経由で製品やサブスクリプションの請求を行うのは、威圧的な場合があります。ただし、Cashier と [Stripeチェックアウト](https://stripe.com/payments/checkout) のおかげで、最新の堅牢な支払い統合を簡単に構築できます。

Cashier と Stripe Checkout を使用してサブスクリプションを販売する方法を学ぶために、基本的な月次 (`price_basic_monthly`) および年次 (`price_basic_yearly`) プランを持つサブスクリプション サービスの簡単なシナリオを考えてみましょう。これら 2 つの価格は、Stripe ダッシュボードの「Basic」製品 (`pro_basic`) にグループ化できます。さらに、当社のサブスクリプション サービスでは、`pro_expert` としてエキスパート プランを提供する場合があります。

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

上の例でわかるように、顧客を Stripe Checkout セッションにリダイレクトし、ベーシック プランに加入できるようにします。チェックアウトまたはキャンセルが成功すると、顧客は `checkout` メソッドに指定した URL にリダイレクトされます。サブスクリプションが実際にいつ開始されたかを知るには (支払い方法によっては処理に数秒かかるため)、[Cashier の Webhook 処理を構成する](#handling-stripe-webhooks) も必要になります。

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

ミドルウェアを定義したら、それをルートに割り当てることができます。

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 顧客が料金プランを管理できるようにする

もちろん、顧客はサブスクリプション プランを別の製品または「階層」に変更したい場合もあります。これを許可する最も簡単な方法は、顧客を Stripe の [顧客請求ポータル](https://stripe.com/docs/no-code/customer-portal) に誘導することです。これは、顧客が請求書のダウンロード、支払い方法の更新、サブスクリプション プランの変更を可能にするホスト型ユーザー インターフェイスを提供します。

まず、Billing Portal セッションを開始するために利用する Laravel ルートにユーザーを誘導するリンクまたはボタンをアプリケーション内に定義します。

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

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
## お客様 (Customers)

<a name="retrieving-customers"></a>
### 顧客の取得

`Cashier::findBillable` メソッドを使用して、Stripe ID によって顧客を取得できます。このメソッドは、課金対象モデルのインスタンスを返します。

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 顧客の創造

場合によっては、サブスクリプションを開始せずに Stripe 顧客を作成したい場合があります。これは、`createAsStripeCustomer` メソッドを使用して実行できます。

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

Stripe で顧客を作成したら、後日サブスクリプションを開始できます。オプションの `$options` 配列を指定して、追加の [Stripe API でサポートされる顧客作成パラメータ](https://stripe.com/docs/api/customers/create) を渡すことができます。

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

課金対象モデルの Stripe 顧客オブジェクトを返したい場合は、`asStripeCustomer` メソッドを使用できます。

```php
$stripeCustomer = $user->asStripeCustomer();
```

`createOrGetStripeCustomer` メソッドは、特定の請求可能モデルの Stripe 顧客オブジェクトを取得したいが、請求可能モデルがすでに Stripe 内の顧客であるかどうかが不明な場合に使用できます。このメソッドは、Stripe に新しい顧客がまだ存在しない場合に作成します。

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 顧客の更新

場合によっては、Stripe 顧客に追加情報を直接更新したい場合があります。これは、`updateStripeCustomer` メソッドを使用して実行できます。このメソッドは、[Stripe API でサポートされる顧客更新オプション](https://stripe.com/docs/api/customers/update) の配列を受け入れます。

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 残高

Stripe では、顧客の「残高」を入金または借方記入することができます。後で、この残高は新しい請求書に記入または借方記入されます。顧客の合計残高を確認するには、請求対象モデルで利用できる `balance` メソッドを使用できます。 `balance` メソッドは、顧客の通貨で残高を表すフォーマットされた文字列を返します。

```php
$balance = $user->balance();
```

顧客の残高を入金するには、`creditBalance` メソッドに値を指定できます。必要に応じて、説明も入力できます。

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

`debitBalance` メソッドに値を指定すると、顧客の残高が引き落とされます。

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

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
### 納税者番号

Cashier は、顧客の納税者番号を管理する簡単な方法を提供します。たとえば、`taxIds` メソッドを使用して、顧客に割り当てられたすべての [納税者番号](https://stripe.com/docs/api/customer_tax_ids/object) をコレクションとして取得できます。

```php
$taxIds = $user->taxIds();
```

顧客の特​​定の納税者 ID を識別子によって取得することもできます。

```php
$taxId = $user->findTaxId('txi_belgium');
```

有効な [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) と値を `createTaxId` メソッドに指定することで、新しい税 ID を作成できます。

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId` メソッドは、顧客のアカウントに VAT ID をすぐに追加します。 [VAT ID の検証も Stripe によって行われます](https://stripe.com/docs/invoicing/customer/tax-ids#validation);ただし、これは非同期プロセスです。 `customer.tax_id.updated` Webhook イベントをサブスクライブし、[VAT ID `verification` パラメータ](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification) を検査することで、検証の更新の通知を受け取ることができます。 Webhook の処理の詳細については、[Webhook ハンドラーの定義に関するドキュメント](#handling-stripe-webhooks) を参照してください。

`deleteTaxId` メソッドを使用して納税者 ID を削除できます。

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### Stripe と顧客データを同期する

通常、アプリケーションのユーザーが自分の名前、電子メール アドレス、または Stripe によって保存されているその他の情報を更新する場合は、Stripe に更新を通知する必要があります。そうすることで、Stripe の情報のコピーがアプリケーションの情報と同期されます。

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

これで、顧客モデルが更新されるたびに、その情報が Stripe と同期されるようになります。便宜上、Cashier は顧客の最初の作成時に顧客情報を Stripe と自動的に同期します。

Cashier が提供するさまざまなメソッドをオーバーライドすることで、顧客情報を Stripe に同期するために使用される列をカスタマイズできます。たとえば、`stripeName` メソッドをオーバーライドして、レジ担当者が顧客情報を Stripe に同期するときに顧客の「名前」とみなされる属性をカスタマイズできます。

```php
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

同様に、`stripeEmail`、`stripePhone` (最大 20 文字)、`stripeAddress`、および `stripePreferredLocales` メソッドをオーバーライドできます。これらのメソッドは、[Stripe 顧客オブジェクトの更新](https://stripe.com/docs/api/customers/update) のときに、対応する顧客パラメータに情報を同期します。顧客情報の同期プロセスを完全に制御したい場合は、`syncStripeCustomerDetails` メソッドをオーバーライドできます。

<a name="billing-portal"></a>
### 請求ポータル

Stripe は、顧客がサブスクリプション、支払い方法を管理し、請求履歴を表示できるように [請求ポータルをセットアップする簡単な方法](https://stripe.com/docs/billing/subscriptions/customer-portal) を提供します。コントローラまたはルートから課金対象モデルの `redirectToBillingPortal` メソッドを呼び出すことで、ユーザーを課金ポータルにリダイレクトできます。

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

デフォルトでは、ユーザーはサブスクリプションの管理を終了すると、Stripe 請求ポータル内のリンクを介してアプリケーションの `home` ルートに戻ることができます。 URL を引数として `redirectToBillingPortal` メソッドに渡すことで、ユーザーが戻るカスタム URL を指定できます。

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

HTTP リダイレクト応答を生成せずに課金ポータルへの URL を生成したい場合は、`billingPortalUrl` メソッドを呼び出します。

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 支払い方法 (Payment Methods)

<a name="storing-payment-methods"></a>
### 支払い方法の保存

Stripe でサブスクリプションを作成したり、「1 回限り」の請求を実行するには、支払い方法を保存し、Stripe からその識別子を取得する必要があります。これを達成するために使用されるアプローチは、サブスクリプションまたは単一料金のどちらの支払い方法を使用する予定であるかによって異なります。そのため、以下では両方について検討します。

<a name="payment-methods-for-subscriptions"></a>
#### 定期購読の支払い方法

サブスクリプションで将来使用するために顧客のクレジット カード情報を保存する場合は、Stripe の「Setup Intents」API を使用して顧客の支払い方法の詳細を安全に収集する必要があります。 「セットアップ インテント」は、顧客の支払い方法に請求する意図を Stripe に示します。 Cashier の `Billable` トレイトには、新しいセットアップ インテントを簡単に作成するための `createSetupIntent` メソッドが含まれています。このメソッドは、顧客の支払い方法の詳細を収集するフォームをレンダリングするルートまたはコントローラから呼び出す必要があります。

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

Setup Intent を作成してビューに渡した後、支払い方法を収集する要素にそのシークレットを添付する必要があります。たとえば、次の「支払い方法の更新」フォームについて考えてみましょう。

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

次に、Stripe.js ライブラリを使用して、[Stripe要素](https://stripe.com/docs/stripe-js) をフォームに添付し、顧客の支払い詳細を安全に収集します。

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

次に、カードを検証し、[Stripe の `confirmCardSetup` メソッド](https://stripe.com/docs/js/setup_intents/confirm_card_setup) を使用して Stripe から安全な「支払い方法識別子」を取得できます。

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

Stripe によってカードが検証された後、結果の `setupIntent.payment_method` 識別子を Laravel アプリケーションに渡し、そこで顧客に添付できます。支払い方法は、[新しい支払い方法として追加されました](#adding-payment-methods) または [デフォルトの支払い方法を更新するために使用されます](#updating-the-default-payment-method) のいずれかです。支払い方法識別子をすぐに [新しいサブスクリプションを作成する](#creating-subscriptions) に使用することもできます。

> [!NOTE]
> セットアップ インテントおよび顧客の支払い詳細の収集に関する詳細情報が必要な場合は、[Stripe が提供するこの概要を確認してください](https://stripe.com/docs/payments/save-and-reuse#php) までお問い合わせください。

<a name="payment-methods-for-single-charges"></a>
#### 一括料金の支払い方法

もちろん、顧客の支払い方法に対して 1 回の請求を行う場合、支払い方法識別子を使用する必要があるのは 1 回だけです。 Stripe の制限により、顧客の保存されているデフォルトの支払い方法を 1 回の請求に使用することはできません。 Stripe.js ライブラリを使用して顧客が支払い方法の詳細を入力できるようにする必要があります。たとえば、次の形式を考えてみましょう。

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

このようなフォームを定義した後、Stripe.js ライブラリを使用して [Stripe要素](https://stripe.com/docs/stripe-js) をフォームに添付し、顧客の支払い詳細を安全に収集できます。

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

次に、カードを検証し、[Stripe の `createPaymentMethod` メソッド](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method) を使用して Stripe から安全な「支払い方法識別子」を取得できます。

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

カードが正常に検証された場合は、`paymentMethod.id` を Laravel アプリケーションに渡し、[一回の充電](#simple-charge) を処理できます。

<a name="retrieving-payment-methods"></a>
### 支払い方法の取得

課金対象モデル インスタンスの `paymentMethods` メソッドは、`Laravel\Cashier\PaymentMethod` インスタンスのコレクションを返します。

```php
$paymentMethods = $user->paymentMethods();
```

デフォルトでは、このメソッドはあらゆる種類の支払い方法を返します。特定のタイプの支払い方法を取得するには、メソッドの引数として `type` を渡すことができます。

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

顧客のデフォルトの支払い方法を取得するには、`defaultPaymentMethod` メソッドを使用できます。

```php
$paymentMethod = $user->defaultPaymentMethod();
```

`findPaymentMethod` メソッドを使用して、請求可能なモデルに関連付けられている特定の支払い方法を取得できます。

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
### 支払い方法の有無

請求可能なモデルのアカウントにデフォルトの支払い方法が関連付けられているかどうかを確認するには、`hasDefaultPaymentMethod` メソッドを呼び出します。

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

`hasPaymentMethod` メソッドを使用して、請求可能なモデルのアカウントに少なくとも 1 つの支払い方法が関連付けられているかどうかを確認できます。

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```

このメソッドは、請求可能なモデルに支払い方法があるかどうかを判断します。モデルに特定のタイプの支払い方法が存在するかどうかを確認するには、メソッドの引数として `type` を渡すことができます。

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
### デフォルトの支払い方法の更新

`updateDefaultPaymentMethod` メソッドは、顧客のデフォルトの支払い方法情報を更新するために使用できます。このメソッドは、Stripe 支払い方法識別子を受け入れ、新しい支払い方法をデフォルトの請求支払い方法として割り当てます。

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

デフォルトの支払い方法情報を Stripe の顧客のデフォルトの支払い方法情報と同期するには、`updateDefaultPaymentMethodFromStripe` メソッドを使用できます。

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 顧客のデフォルトの支払い方法は、請求書発行と新しいサブスクリプションの作成にのみ使用できます。 Stripe によって課された制限により、単一のチャージには使用できない場合があります。

<a name="adding-payment-methods"></a>
### 支払い方法の追加

新しい支払い方法を追加するには、支払い方法識別子を渡して、請求可能モデルで `addPaymentMethod` メソッドを呼び出します。

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 支払い方法識別子の取得方法については、[支払い方法の保管に関するドキュメント](#storing-payment-methods) をご覧ください。

<a name="deleting-payment-methods"></a>
### 支払い方法の削除

支払い方法を削除するには、削除する `Laravel\Cashier\PaymentMethod` インスタンスで `delete` メソッドを呼び出します。

```php
$paymentMethod->delete();
```

`deletePaymentMethod` メソッドは、請求可能なモデルから特定の支払い方法を削除します。

```php
$user->deletePaymentMethod('pm_visa');
```

`deletePaymentMethods` メソッドは、請求可能なモデルのすべての支払い方法情報を削除します。

```php
$user->deletePaymentMethods();
```

デフォルトでは、このメソッドはあらゆる種類の支払い方法を削除します。特定のタイプの支払い方法を削除するには、メソッドの引数として `type` を渡すことができます。

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> ユーザーがアクティブなサブスクリプションを持っている場合、アプリケーションではユーザーがデフォルトの支払い方法を削除できないようにする必要があります。

<a name="subscriptions"></a>
## 定期購入 (Subscriptions)

サブスクリプションは、顧客に定期的な支払いを設定する方法を提供します。 Cashier によって管理される Stripe サブスクリプションは、複数のサブスクリプション価格、サブスクリプション数量、トライアルなどのサポートを提供します。

<a name="creating-subscriptions"></a>
### サブスクリプションの作成

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

`newSubscription` メソッドに渡される最初の引数は、サブスクリプションの内部タイプである必要があります。アプリケーションが単一のサブスクリプションのみを提供する場合は、これを `default` または `primary` と呼びます。このサブスクリプション タイプはアプリケーション内部でのみ使用され、ユーザーに表示されることを目的としていません。また、スペースを含めることはできません。また、サブスクリプションの作成後に変更しないでください。 2 番目の引数は、ユーザーが購読している特定の価格です。この値は、Stripe の価格の識別子に対応する必要があります。

[Stripe 支払い方法識別子](#storing-payment-methods) または Stripe `PaymentMethod` オブジェクトを受け入れる `create` メソッドは、サブスクリプションを開始するだけでなく、課金対象モデルの Stripe 顧客 ID およびその他の関連課金情報でデータベースを更新します。

> [!WARNING]
> 支払い方法識別子を `create` サブスクリプション メソッドに直接渡すと、その識別子がユーザーの保存された支払い方法に自動的に追加されます。

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 請求書メールによる定期的な支払いの回収

顧客の定期支払いを自動的に収集する代わりに、定期支払いの期限が来るたびに顧客に請求書を電子メールで送信するように Stripe に指示できます。その後、顧客は請求書を受け取ったら手動で支払うことができます。請求書を通じて定期的な支払いを回収する場合、顧客は前もって支払い方法を指定する必要はありません。

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

サブスクリプションがキャンセルされるまでに顧客が請求書を支払わなければならない期間は、`days_until_due` オプションによって決まります。デフォルトでは、これは 30 日です。ただし、必要に応じて、このオプションに特定の値を指定できます。

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### 数量

サブスクリプションの作成時に価格に特定の [quantity](https://stripe.com/docs/billing/subscriptions/quantities) を設定したい場合は、サブスクリプションを作成する前にサブスクリプション ビルダで `quantity` メソッドを呼び出す必要があります。

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 追加の詳細

Stripe でサポートされている追加の [customer](https://stripe.com/docs/api/customers/create) または [subscription](https://stripe.com/docs/api/subscriptions/create) オプションを指定したい場合は、それらを `create` メソッドの 2 番目と 3 番目の引数として渡すことで指定できます。

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => 'Some extra information.'],
]);
```

<a name="coupons"></a>
#### クーポン

サブスクリプションの作成時にクーポンを適用したい場合は、`withCoupon` メソッドを使用できます。

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

または、[Stripe プロモーション コード](https://stripe.com/docs/billing/subscriptions/discounts/codes) を適用したい場合は、`withPromotionCode` メソッドを使用できます。

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

指定されたプロモーション コード ID は、顧客向けのプロモーション コードではなく、プロモーション コードに割り当てられた Stripe API ID である必要があります。特定の顧客向けプロモーション コードに基づいてプロモーション コード ID を検索する必要がある場合は、`findPromotionCode` メソッドを使用できます。

```php
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

上の例では、返される `$promotionCode` オブジェクトは `Laravel\Cashier\PromotionCode` のインスタンスです。このクラスは、基礎となる `Stripe\PromotionCode` オブジェクトを装飾します。 `coupon` メソッドを呼び出して、プロモーション コードに関連するクーポンを取得できます。

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

クーポン インスタンスを使用すると、割引額と、クーポンが固定割引を表すかパーセントベースの割引を表すかを決定できます。

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

顧客またはサブスクリプションに現在適用されている割引を取得することもできます。

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

返された `Laravel\Cashier\Discount` インスタンスは、基になる `Stripe\Discount` オブジェクト インスタンスを装飾します。 `coupon` メソッドを呼び出して、この割引に関連するクーポンを取得できます。

```php
$coupon = $subscription->discount()->coupon();
```

新しいクーポンまたはプロモーション コードを顧客またはサブスクリプションに適用したい場合は、`applyCoupon` または `applyPromotionCode` メソッドを使用して適用できます。

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

顧客向けのプロモーション コードではなく、プロモーション コードに割り当てられた Stripe API ID を使用する必要があることに注意してください。特定の時点で顧客またはサブスクリプションに適用できるクーポンまたはプロモーション コードは 1 つだけです。

この件に関する詳細については、[coupons](https://stripe.com/docs/billing/subscriptions/coupons) および [プロモーションコード](https://stripe.com/docs/billing/subscriptions/coupons/codes) に関する Stripe ドキュメントを参照してください。

<a name="adding-subscriptions"></a>
#### サブスクリプションの追加

すでにデフォルトの支払い方法を持っている顧客にサブスクリプションを追加したい場合は、サブスクリプション ビルダで `add` メソッドを呼び出すことができます。

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe ダッシュボードからのサブスクリプションの作成

Stripe ダッシュボード自体からサブスクリプションを作成することもできます。これを行うと、Cashier は新しく追加されたサブスクリプションを同期し、それらに `default` のタイプを割り当てます。ダッシュボードで作成されたサブスクリプションに割り当てられるサブスクリプション タイプをカスタマイズするには、[Webhook イベント ハンドラーを定義する](#defining-webhook-event-handlers)。

さらに、Stripe ダッシュボードから作成できるサブスクリプションは 1 種類のみです。アプリケーションが異なるタイプを使用する複数のサブスクリプションを提供している場合、Stripe ダッシュボードから追加できるサブスクリプションのタイプは 1 つだけです。

最後に、アプリケーションによって提供されるサブスクリプションの種類ごとに、アクティブなサブスクリプションを 1 つだけ追加するように常に注意する必要があります。顧客が 2 つの `default` サブスクリプションを持っている場合、両方がアプリケーションのデータベースと同期されるとしても、最後に追加されたサブスクリプションのみが Cashier によって使用されます。

<a name="checking-subscription-status"></a>
### 購読ステータスの確認

顧客がアプリケーションを購読すると、さまざまな便利な方法を使用して顧客の購読ステータスを簡単に確認できます。まず、顧客がアクティブなサブスクリプションを持っている場合、サブスクリプションが現在試用期間内であっても、`subscribed` メソッドは `true` を返します。 `subscribed` メソッドは、最初の引数としてサブスクリプションのタイプを受け入れます。

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` メソッドも [ルートミドルウェア](/docs/{{version}}/middleware) の有力な候補となり、ユーザーのサブスクリプション ステータスに基づいてルートとコントローラへのアクセスをフィルタリングできます。

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

ユーザーがまだ試用期間内であるかどうかを確認したい場合は、`onTrial` メソッドを使用できます。このメソッドは、ユーザーがまだ試用期間中であることをユーザーに警告するかどうかを決定するのに役立ちます。

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

`subscribedToProduct` メソッドは、特定の Stripe 製品の識別子に基づいて、ユーザーが特定の製品を購読しているかどうかを判断するために使用できます。 Stripe では、製品は価格の集合です。この例では、ユーザーの `default` サブスクリプションがアプリケーションの「プレミアム」製品にアクティブにサブスクライブされているかどうかを判断します。指定された Stripe 製品 ID は、Stripe ダッシュボード内の製品 ID の 1 つに対応する必要があります。

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

配列を `subscribedToProduct` メソッドに渡すことによって、ユーザーの `default` サブスクリプションがアプリケーションの「ベーシック」製品または「プレミアム」製品にアクティブにサブスクライブされているかどうかを判断できます。

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

`subscribedToPrice` メソッドは、顧客のサブスクリプションが特定の価格 ID に対応するかどうかを判断するために使用できます。

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

`recurring` メソッドは、ユーザーが現在購読中であり、試用期間中でないかどうかを判断するために使用できます。

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> ユーザーが同じタイプの 2 つのサブスクリプションを持っている場合、`subscription` メソッドによって常に最新のサブスクリプションが返されます。たとえば、ユーザーは `default` タイプのサブスクリプション レコードを 2 つ持っているとします。ただし、サブスクリプションの 1 つは期限切れの古いサブスクリプションであり、もう 1 つは現在のアクティブなサブスクリプションである可能性があります。最新のサブスクリプションは常に返されますが、古いサブスクリプションは履歴レビューのためにデータベースに保存されます。

<a name="cancelled-subscription-status"></a>
#### キャンセルされたサブスクリプションのステータス

ユーザーがかつてはアクティブなサブスクライバだったが、サブスクリプションをキャンセルしたかどうかを確認するには、`canceled` メソッドを使用できます。

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

また、ユーザーがサブスクリプションをキャンセルしたが、サブスクリプションが完全に期限切れになるまでまだ「猶予期間」中であるかどうかを判断することもできます。たとえば、ユーザーが元々 3 月 10 日に期限切れになる予定だったサブスクリプションを 3 月 5 日にキャンセルした場合、ユーザーは 3 月 10 日まで「猶予期間」に入ります。この間も、`subscribed` メソッドは `true` を返すことに注意してください。

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

ユーザーがサブスクリプションをキャンセルし、「猶予期間」に入っていないかどうかを確認するには、`ended` メソッドを使用できます。

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
#### 未完了および期限超過のステータス

サブスクリプションの作成後に 2 番目の支払いアクションが必要な場合、サブスクリプションは `incomplete` としてマークされます。サブスクリプションのステータスは、Cashier の `subscriptions` データベース テーブルの `stripe_status` 列に保存されます。

同様に、価格を交換するときに 2 番目の支払いアクションが必要な場合、サブスクリプションは `past_due` としてマークされます。サブスクリプションがこれらの状態のいずれかにある場合、顧客が支払いを確認するまでアクティブになりません。サブスクリプションに支払いが完了していないかどうかを判断するには、請求可能モデルまたはサブスクリプション インスタンスで `hasIncompletePayment` メソッドを使用します。

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

サブスクリプションの支払いが完了していない場合は、`latestPayment` 識別子を渡して、ユーザーをCashierの支払い確認ページに誘導する必要があります。サブスクリプション インスタンスで利用可能な `latestPayment` メソッドを使用して、この識別子を取得できます。

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

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
#### サブスクリプションの範囲

ほとんどのサブスクリプション状態はクエリ スコープとしても使用できるため、特定の状態にあるサブスクリプションについてデータベースを簡単にクエリできます。

```php
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

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
### 価格の変更

顧客がアプリケーションをサブスクライブした後、新しいサブスクリプション価格への変更を希望する場合があります。顧客を新しい価格に切り替えるには、Stripe 価格の識別子を `swap` メソッドに渡します。価格を交換するときは、ユーザーが以前にサブスクリプションをキャンセルした場合にそのサブスクリプションを再アクティブ化したいと考えていると想定されます。指定された価格識別子は、Stripe ダッシュボードで使用可能な Stripe 価格識別子に対応する必要があります。

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

お客様が試用中の場合、試用期間は維持されます。さらに、サブスクリプションに「数量」が存在する場合、その数量も維持されます。

価格を交換し、顧客が現在参加している試用期間をキャンセルしたい場合は、`skipTrial` メソッドを呼び出すことができます。

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

価格を交換して、次の請求サイクルを待たずにすぐに顧客に請求したい場合は、`swapAndInvoice` メソッドを使用できます。

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 按分

デフォルトでは、Stripe は価格を切り替えるときに料金を日割り計算します。 `noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションの価格を更新できます。

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

サブスクリプションの日割り計算の詳細については、[Stripe のドキュメント](https://stripe.com/docs/billing/subscriptions/prorations) を参照してください。

> [!WARNING]
> `swapAndInvoice` メソッドの前に `noProrate` メソッドを実行しても、比例配分には影響しません。請求書は必ず発行されます。

<a name="subscription-quantity"></a>
### 購読数量

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

あるいは、`updateQuantity` メソッドを使用して特定の数量を設定することもできます。

```php
$user->subscription('default')->updateQuantity(10);
```

`noProrate` メソッドを使用すると、料金を日割り計算せずにサブスクリプションの数量を更新できます。

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

サブスクリプション数量の詳細については、[Stripe のドキュメント](https://stripe.com/docs/subscriptions/quantities) を参照してください。

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 複数の製品のサブスクリプションの数量

サブスクリプションが [複数の製品のサブスクリプション](#subscriptions-with-multiple-products) の場合は、増分または減分する数量の価格の ID を 2 番目の引数として増分 / 減分メソッドに渡す必要があります。

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 複数の製品のサブスクリプション

[複数の製品のサブスクリプション](https://stripe.com/docs/billing/subscriptions/multiple-products) を使用すると、複数の課金製品を 1 つのサブスクリプションに割り当てることができます。たとえば、基本サブスクリプション価格が月額 10 ドルであるが、月額 15 ドルの追加料金でライブ チャット アドオン製品を提供するカスタマー サービスの「ヘルプデスク」アプリケーションを構築していると想像してください。複数の製品のサブスクリプションの情報は、Cashier の `subscription_items` データベース テーブルに保存されます。

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

上の例では、顧客は `default` サブスクリプションに 2 つの価格を設定します。どちらの価格も、それぞれの請求間隔で請求されます。必要に応じて、`quantity` メソッドを使用して、各価格の特定の数量を指定できます。

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

既存のサブスクリプションに別の価格を追加したい場合は、サブスクリプションの `addPrice` メソッドを呼び出します。

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

上記の例では、新しい価格が追加され、顧客は次の請求サイクルでその料金を請求されます。顧客にすぐに請求したい場合は、`addPriceAndInvoice` メソッドを使用できます。

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

特定の数量を含む価格を追加したい場合は、`addPrice` メソッドまたは `addPriceAndInvoice` メソッドの 2 番目の引数として数量を渡すことができます。

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

`removePrice` メソッドを使用して、サブスクリプションから価格を削除できます。

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> サブスクリプションの最後の価格を削除することはできません。代わりに、サブスクリプションをキャンセルするだけです。

<a name="swapping-prices"></a>
#### スワッピング価格

複数の製品のサブスクリプションに関連付けられている価格を変更することもできます。たとえば、顧客が `price_chat` アドオン製品を含む `price_basic` サブスクリプションを持っており、顧客を `price_basic` から `price_pro` 価格にアップグレードしたいとします。

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

上記の例を実行すると、`price_basic` を持つ基になるサブスクリプション アイテムが削除され、`price_chat` を持つサブスクリプション アイテムは保持されます。さらに、`price_pro` の新しいサブスクリプション アイテムが作成されます。

キーと値のペアの配列を `swap` メソッドに渡すことで、サブスクリプション項目オプションを指定することもできます。たとえば、サブスクリプション価格の数量を指定する必要がある場合があります。

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

サブスクリプションの単一の価格を交換したい場合は、サブスクリプション項目自体で `swap` メソッドを使用して行うことができます。このアプローチは、サブスクリプションの他の価格に関する既存のメタデータをすべて保持したい場合に特に便利です。

```php
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>
#### 日割り

デフォルトでは、Stripe は複数の製品のサブスクリプションに価格を追加または削除するときに料金を日割り計算します。日割りなしで価格調整を行いたい場合は、価格操作に `noProrate` メソッドをチェーンする必要があります。

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 数量

個々のサブスクリプション価格の数量を更新したい場合は、[既存の数量メソッド](#subscription-quantity) を使用して価格の ID を追加の引数としてメソッドに渡します。

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> サブスクリプションに複数の価格がある場合、`Subscription` モデルの `stripe_price` 属性と `quantity` 属性は `null` になります。個々の価格属性にアクセスするには、`Subscription` モデルで使用可能な `items` 関係を使用する必要があります。

<a name="subscription-items"></a>
#### 定期購入アイテム

サブスクリプションに複数の価格がある場合、データベースの `subscription_items` テーブルに複数のサブスクリプション「アイテム」が保存されます。これらには、サブスクリプションの `items` 関係を介してアクセスできます。

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

`findItemOrFail` メソッドを使用して特定の価格を取得することもできます。

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### 複数のサブスクリプション

Stripe を使用すると、顧客は複数のサブスクリプションを同時に持つことができます。たとえば、水泳のサブスクリプションとウェイトリフティングのサブスクリプションを提供するジムを運営しており、各サブスクリプションの価格が異なる場合があります。もちろん、顧客はどちらかまたは両方のプランに加入できる必要があります。

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

この例では、顧客に対して毎月の水泳サブスクリプションを開始しました。ただし、後で年間サブスクリプションに切り替えたい場合もあります。顧客のサブスクリプションを調整するときは、`swimming` サブスクリプションの価格を単純に交換できます。

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

もちろん、サブスクリプションを完全にキャンセルすることもできます。

```php
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
### 使用量ベースの請求

[使用量ベースの請求](https://stripe.com/docs/billing/subscriptions/metered-billing) を使用すると、請求サイクル中の製品の使用量に基づいて顧客に請求できます。たとえば、顧客が毎月送信するテキスト メッセージや電子メールの数に基づいて顧客に請求できます。

従量課金の使用を開始するには、まず、[使用量ベースの課金モデル](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) と [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter) を使用して、Stripe ダッシュボードに新しい製品を作成する必要があります。メーターを作成した後、関連するイベント名とメーター ID を保存します。これらは、使用状況をレポートおよび取得するために必要になります。次に、`meteredPrice` メソッドを使用して、従量制価格 ID を顧客のサブスクリプションに追加します。

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

[Stripeチェックアウト](#checkout) 経由で従量制サブスクリプションを開始することもできます。

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
#### 使用状況のレポート

顧客がアプリケーションを使用すると、正確に請求できるように、その使用状況を Stripe に報告します。計測イベントの使用状況をレポートするには、`Billable` モデルで `reportMeterEvent` メソッドを使用できます。

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

デフォルトでは、「使用数量」1 が請求期間に追加されます。あるいは、特定の「使用量」を渡して、請求期間中の顧客の使用量に追加することもできます。

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

メーターの顧客のイベント概要を取得するには、`Billable` インスタンスの `meterEventSummaries` メソッドを使用できます。

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

メーターイベントの概要の詳細については、Stripe の [メーターイベント概要オブジェクトのドキュメント](https://docs.stripe.com/api/billing/meter-event_summary/object) を参照してください。

[すべてのメーターをリストする](https://docs.stripe.com/api/billing/meter/list) には、`Billable` インスタンスの `meters` メソッドを使用できます。

```php
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>
### 購読税

> [!WARNING]
> 税率を手動で計算する代わりに、[Stripe Tax を使用して税金を自動計算する](#tax-configuration) を実行できます。

ユーザーがサブスクリプションに対して支払う税率を指定するには、請求可能モデルに `taxRates` メソッドを実装し、Stripe 税率 ID を含む配列を返す必要があります。これらの税率は [Stripe ダッシュボード](https://dashboard.stripe.com/test/tax-rates) で定義できます。

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

`taxRates` メソッドを使用すると、顧客ごとに税率を適用できます。これは、複数の国や税率にまたがるユーザー ベースに役立つ場合があります。

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
#### 税率の同期

`taxRates` メソッドによって返されるハードコードされた税率 ID を変更する場合、ユーザーの既存のサブスクリプションの税金設定は同じままになります。既存のサブスクリプションの税額を新しい `taxRates` 値で更新する場合は、ユーザーのサブスクリプション インスタンスで `syncTaxRates` メソッドを呼び出す必要があります。

```php
$user->subscription('default')->syncTaxRates();
```

これにより、複数の商品のサブスクリプションの商品税率も同期されます。アプリケーションが複数の製品のサブスクリプションを提供している場合は、課金対象モデルが `priceTaxRates` メソッド [上で議論した](#subscription-taxes) を実装していることを確認する必要があります。

<a name="tax-exemption"></a>
#### 免税

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
### サブスクリプションアンカー日

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

サブスクリプションの請求サイクルの管理の詳細については、[Stripe の請求サイクルに関するドキュメント](https://stripe.com/docs/billing/subscriptions/billing-cycle) を参照してください。

<a name="cancelling-subscriptions"></a>
### 定期購入のキャンセル

サブスクリプションをキャンセルするには、ユーザーのサブスクリプションで `cancel` メソッドを呼び出します。

```php
$user->subscription('default')->cancel();
```

サブスクリプションがキャンセルされると、Cashier は `subscriptions` データベース テーブルに `ends_at` 列を自動的に設定します。この列は、`subscribed` メソッドが `false` を返し始める時期を知るために使用されます。

たとえば、顧客が 3 月 1 日にサブスクリプションをキャンセルしたが、そのサブスクリプションが 3 月 5 日まで終了する予定ではなかった場合、`subscribed` メソッドは 3 月 5 日まで `true` を返し続けます。これは、ユーザーが通常、請求サイクルが終了するまでアプリケーションを使用し続けることが許可されているために行われます。

`onGracePeriod` メソッドを使用して、ユーザーがサブスクリプションをキャンセルしたがまだ「猶予期間」中であるかどうかを確認できます。

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

サブスクリプションをすぐにキャンセルしたい場合は、ユーザーのサブスクリプションで `cancelNow` メソッドを呼び出します。

```php
$user->subscription('default')->cancelNow();
```

サブスクリプションをすぐにキャンセルし、残りの未請求の従量制使用量または新規/保留中の日割り請求書アイテムを請求したい場合は、ユーザーのサブスクリプションで `cancelNowAndInvoice` メソッドを呼び出します。

```php
$user->subscription('default')->cancelNowAndInvoice();
```

特定の時点でサブスクリプションをキャンセルすることもできます。

```php
$user->subscription('default')->cancelAt(
    now()->plus(days: 10)
);
```

最後に、関連するユーザー モデルを削除する前に、常にユーザー サブスクリプションをキャンセルする必要があります。

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
### サブスクリプションの再開

顧客がサブスクリプションをキャンセルし、それを再開したい場合は、サブスクリプションで `resume` メソッドを呼び出すことができます。顧客がサブスクリプションを再開するには、「猶予期間」内である必要があります。

```php
$user->subscription('default')->resume();
```

顧客がサブスクリプションをキャンセルし、サブスクリプションの有効期限が完全に切れる前にそのサブスクリプションを再開した場合、顧客にはすぐには請求されません。代わりに、サブスクリプションが再度アクティブ化され、元の請求サイクルで請求されます。

<a name="subscription-trials"></a>
## サブスクリプショントライアル (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 支払い方法を前払いする場合

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

このメソッドは、データベース内のサブスクリプション レコードに試用期間の終了日を設定し、この日以降になるまで顧客への請求を開始しないように Stripe に指示します。 `trialDays` メソッドを使用すると、Cashier は Stripe の価格に設定されたデフォルトの試用期間を上書きします。

> [!WARNING]
> 試用期間の終了日までに顧客のサブスクリプションがキャンセルされなかった場合、試用期間が終了するとすぐに料金が請求されるため、ユーザーに試用期間の終了日を必ず通知する必要があります。

`trialUntil` メソッドを使用すると、試用期間の終了時期を指定する `DateTime` インスタンスを提供できます。

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->plus(days: 10))
    ->create($paymentMethod);
```

ユーザー インスタンスの `onTrial` メソッドまたはサブスクリプション インスタンスの `onTrial` メソッドを使用して、ユーザーが試用期間内かどうかを判断できます。以下の 2 つの例は同等です。

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

`endTrial` メソッドを使用して、サブスクリプションのトライアルをすぐに終了できます。

```php
$user->subscription('default')->endTrial();
```

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
#### Stripe / Cashier での試用日の定義

Stripe ダッシュボードで価格を受け取るトライアル日数を定義するか、Cashier を使用して常に明示的に渡すかを選択できます。 Stripe で価格の試用期間を定義することを選択した場合は、明示的に `skipTrial()` メソッドを呼び出さない限り、過去にサブスクリプションを持っていた顧客の新規サブスクリプションを含む、新しいサブスクリプションには常に試用期間が設定されることに注意する必要があります。

<a name="without-payment-method-up-front"></a>
### 前払いの支払い方法なし

ユーザーの支払い方法情報を事前に収集せずに試用期間を提供したい場合は、ユーザー レコードの `trial_ends_at` 列を希望する試用終了日に設定できます。これは通常、ユーザー登録時に行われます。

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->plus(days: 10),
]);
```

> [!WARNING]
> 課金対象モデルのクラス定義内の `trial_ends_at` 属性に [日付キャスト](/docs/{{version}}/eloquent-mutators#date-casting) を必ず追加してください。

既存のサブスクリプションに関連付けられていないため、Cashier はこのタイプのトライアルを「一般トライアル」と呼びます。現在の日付が `trial_ends_at` の値を超えていない場合、請求可能モデル インスタンスの `onTrial` メソッドは `true` を返します。

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

ユーザーの実際のサブスクリプションを作成する準備ができたら、通常どおり `newSubscription` メソッドを使用できます。

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

ユーザーの試用終了日を取得するには、`trialEndsAt` メソッドを使用できます。このメソッドは、ユーザーが試用中の場合は Carbon date インスタンスを返し、試用中でない場合は `null` を返します。デフォルト以外の特定のサブスクリプションの試用終了日を取得したい場合は、オプションのサブスクリプション タイプ パラメーターを渡すこともできます。

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

ユーザーが「一般的な」試用期間内であり、実際のサブスクリプションをまだ作成していないことを具体的に知りたい場合は、`onGenericTrial` メソッドを使用することもできます。

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>
### トライアルの延長

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
## Stripe Webhook の処理 (Handling Stripe Webhooks)

> [!NOTE]
> [Stripe CLI](https://stripe.com/docs/stripe-cli) を使用すると、ローカル開発中に Webhook をテストできます。

Stripe は、Webhook 経由でさまざまなイベントをアプリケーションに通知できます。デフォルトでは、Cashier の Webhook コントローラを指すルートは、Cashier サービスプロバイダによって自動的に登録されます。このコントローラは、受信したすべての Webhook リクエストを処理します。

デフォルトでは、Cashier Webhook コントローラは、失敗した請求 (Stripe 設定で定義されている) が多すぎるサブスクリプションのキャンセル、顧客の更新、顧客の削除、サブスクリプションの更新、支払い方法の変更を自動的に処理します。ただし、すぐにわかりますが、このコントローラを拡張して、任意の Stripe Webhook イベントを処理できます。

アプリケーションが Stripe Webhook を処理できるようにするには、Stripe コントロール パネルで Webhook URL を構成してください。デフォルトでは、Cashier の Webhook コントローラは `/stripe/webhook` URL パスに応答します。 Stripe コントロール パネルで有効にする必要があるすべての Webhook の完全なリストは次のとおりです。

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

便宜上、Cashier には `cashier:webhook` Artisan コマンドが含まれています。このコマンドは、Cashier が必要とするすべてのイベントをリッスンする Webhook を Stripe に作成します。

```shell
php artisan cashier:webhook
```

デフォルトでは、作成された Webhook は、`APP_URL` 環境変数によって定義された URL と、Cashier に含まれる `cashier.webhook` ルートを指します。別の URL を使用したい場合は、コマンドを呼び出すときに `--url` オプションを指定できます。

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

作成される Webhook は、Cashier のバージョンと互換性のある Stripe API バージョンを使用します。別の Stripe バージョンを使用したい場合は、`--api-version` オプションを指定できます。

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

作成後、Webhook はすぐにアクティブになります。 Webhook を作成したいが、準備が完了するまで無効にしておく場合は、コマンドを呼び出すときに `--disabled` オプションを指定できます。

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Cashier に含まれる [Webhook 署名の検証](#verifying-webhook-signatures) ミドルウェアを使用して、受信した Stripe Webhook リクエストを必ず保護してください。

<a name="webhooks-csrf-protection"></a>
#### Webhook と CSRF 保護

Stripe Webhook は Laravel の [CSRF保護](/docs/{{version}}/csrf) をバイパスする必要があるため、Laravel が受信 Stripe Webhook の CSRF トークンを検証しないようにする必要があります。これを実現するには、アプリケーションの `bootstrap/app.php` ファイルで CSRF 保護から `stripe/*` を除外する必要があります。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
### Webhook イベント ハンドラーの定義

Cashier は、失敗した請求やその他の一般的な Stripe Webhook イベントによるサブスクリプションのキャンセルを自動的に処理します。ただし、追加の Webhook イベントを処理したい場合は、Cashier によって送出される次のイベントをリッスンすることで処理できます。

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

どちらのイベントにも、Stripe Webhook の完全なペイロードが含まれています。たとえば、`invoice.payment_succeeded` Webhook を処理したい場合は、イベントを処理する [listener](/docs/{{version}}/events#defining-listeners) を登録できます。

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
### Webhook 署名の検証

Webhook を保護するには、[Stripe の Webhook 署名](https://stripe.com/docs/webhooks/signatures) を使用できます。便宜上、Cashier には、受信した Stripe Webhook リクエストが有効であることを検証するミドルウェアが自動的に組み込まれています。

Webhook 検証を有効にするには、アプリケーションの `.env` ファイルに `STRIPE_WEBHOOK_SECRET` 環境変数が設定されていることを確認してください。 Webhook `secret` は、Stripe アカウントのダッシュボードから取得できます。

<a name="single-charges"></a>
## シングルチャージ (Single Charges)

<a name="simple-charge"></a>
### かんたんチャージ

顧客に対して 1 回限りの請求を行う場合は、請求可能モデル インスタンスで `charge` メソッドを使用できます。 `charge` メソッドの 2 番目の引数として [支払い方法識別子を提供する](#payment-methods-for-single-charges) を指定する必要があります。

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

`charge` メソッドは 3 番目の引数として配列を受け入れ、基になる Stripe チャージ作成に必要なオプションを渡すことができます。料金作成時に利用できるオプションの詳細については、[Stripe のドキュメント](https://stripe.com/docs/api/charges/create) を参照してください。

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

基になる顧客またはユーザーなしで `charge` メソッドを使用することもできます。これを実現するには、アプリケーションの課金対象モデルの新しいインスタンスで `charge` メソッドを呼び出します。

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

充電が失敗すると、`charge` メソッドは例外をスローします。チャージが成功すると、`Laravel\Cashier\Payment` のインスタンスがメソッドから返されます。

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
### 請求書による請求

場合によっては、1 回限りの請求を行って、PDF の請求書を顧客に提供する必要がある場合があります。 `invoicePrice` メソッドを使用すると、まさにそれが可能になります。たとえば、顧客に新しいシャツ 5 枚の請求書を発行してみましょう。

```php
$user->invoicePrice('price_tshirt', 5);
```

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

`invoicePrice` と同様に、`tabPrice` メソッドを使用して、顧客の「タブ」にアイテムを追加して顧客に請求することにより、複数のアイテム (請求書ごとに最大 250 アイテム) に対する 1 回限りの請求を作成できます。たとえば、顧客にシャツ 5 枚とマグカップ 2 個の請求を行うとします。

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

あるいは、`invoiceFor` メソッドを使用して、顧客のデフォルトの支払い方法に対して「1 回限り」の請求を行うこともできます。

```php
$user->invoiceFor('One Time Fee', 500);
```

`invoiceFor` メソッドを使用することもできますが、事前定義された価格で `invoicePrice` および `tabPrice` メソッドを使用することをお勧めします。そうすることで、Stripe ダッシュボード内で製品ごとの売上に関するより優れた分析とデータにアクセスできるようになります。

> [!WARNING]
> `invoice`、`invoicePrice`、および `invoiceFor` メソッドは、失敗した請求を再試行する Stripe 請求書を作成します。失敗した請求書を再試行したくない場合は、最初の請求失敗後に Stripe API を使用して請求書を閉じる必要があります。

<a name="creating-payment-intents"></a>
### 支払い意図の作成

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

支払いインテントを作成した後、ユーザーがブラウザーで支払いを完了できるように、クライアント シークレットをアプリケーションのフロントエンドに返すことができます。 Stripe 支払いインテントを使用した支払いフロー全体の構築の詳細については、[Stripe のドキュメント](https://stripe.com/docs/payments/accept-a-payment?platform=web) を参照してください。

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
### 払戻手数料

Stripe 料金を返金する必要がある場合は、`refund` メソッドを使用できます。このメソッドは、最初の引数として Stripe [支払い意図 ID](#payment-methods-for-single-charges) を受け入れます。

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 請求書 (Invoices)

<a name="retrieving-invoices"></a>
### 請求書の取得

`invoices` メソッドを使用すると、請求可能なモデルの請求書の配列を簡単に取得できます。 `invoices` メソッドは、`Laravel\Cashier\Invoice` インスタンスのコレクションを返します。

```php
$invoices = $user->invoices();
```

結果に保留中の請求書を含めたい場合は、`invoicesIncludingPending` メソッドを使用できます。

```php
$invoices = $user->invoicesIncludingPending();
```

`findInvoice` メソッドを使用して、ID で特定の請求書を取得できます。

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### 請求書情報の表示

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
### 今後の請求書

顧客の今後の請求書を取得するには、`upcomingInvoice` メソッドを使用できます。

```php
$invoice = $user->upcomingInvoice();
```

同様に、顧客が複数のサブスクリプションを持っている場合は、特定のサブスクリプションの今後の請求書を取得することもできます。

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### サブスクリプション請求書のプレビュー

`previewInvoice` メソッドを使用すると、価格を変更する前に請求書をプレビューできます。これにより、特定の価格変更が行われたときに顧客の請求書がどのようになるかを判断できます。

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

複数の新しい価格で請求書をプレビューするために、価格の配列を `previewInvoice` メソッドに渡すことができます。

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### 請求書 PDF の生成

請求書 PDF を生成する前に、Composer を使用して、Cashier のデフォルトの請求書レンダラーである Dompdf ライブラリをインストールする必要があります。

```shell
composer require dompdf/dompdf
```

ルートまたはコントローラ内から、`downloadInvoice` メソッドを使用して、特定の請求書の PDF ダウンロードを生成できます。このメソッドは、請求書のダウンロードに必要な適切な HTTP 応答を自動的に生成します。

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

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

`downloadInvoice` メソッドでは、3 番目の引数を使用してカスタム ファイル名を指定することもできます。このファイル名には、自動的に `.pdf` という接尾辞が付けられます。

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### カスタム請求書レンダラー

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

請求書レンダラー コントラクトを実装したら、アプリケーションの `config/cashier.php` 構成ファイル内の `cashier.invoices.renderer` 構成値を更新する必要があります。この構成値は、カスタム レンダラー実装のクラス名に設定する必要があります。

<a name="checkout"></a>
## チェックアウト (Checkout)

Cashier Stripe は、[Stripeチェックアウト](https://stripe.com/payments/checkout) のサポートも提供します。 Stripe Checkout は、事前に構築されたホストされた支払いページを提供することで、支払いを受け入れるためのカスタム ページを実装する手間を省きます。

次のドキュメントには、Cashier で Stripe Checkout の使用を開始する方法に関する情報が含まれています。 Stripe Checkout について詳しく知りたい場合は、[Checkout に関する Stripe 独自のドキュメント](https://stripe.com/docs/payments/checkout) を確認することも検討してください。

<a name="product-checkouts"></a>
### 製品チェックアウト

課金対象モデルで `checkout` メソッドを使用して、Stripe ダッシュボード内で作成された既存の製品のチェックアウトを実行できます。 `checkout` メソッドは、新しい Stripe Checkout セッションを開始します。デフォルトでは、Stripe Price ID を渡す必要があります。

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

必要に応じて、製品の数量を指定することもできます。

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

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
#### プロモーションコード

デフォルトでは、Stripe Checkout は [ユーザーが引き換え可能なプロモーション コード](https://stripe.com/docs/billing/subscriptions/discounts/codes) を許可しません。幸いなことに、チェックアウト ページでこれらを有効にする簡単な方法があります。これを行うには、`allowPromotionCodes` メソッドを呼び出します。

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### シングルチャージチェックアウト

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
### サブスクリプションのチェックアウト

> [!WARNING]
> サブスクリプションに Stripe Checkout を使用するには、Stripe ダッシュボードで `customer.subscription.created` Webhook を有効にする必要があります。この Webhook は、データベースにサブスクリプション レコードを作成し、関連するすべてのサブスクリプション アイテムを保存します。

Stripe Checkout を使用してサブスクリプションを開始することもできます。 Cashier のサブスクリプション ビルダ メソッドを使用してサブスクリプションを定義した後、`checkout ` メソッドを呼び出すことができます。顧客がこのルートにアクセスすると、Stripe のチェックアウト ページにリダイレクトされます。

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

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
> 残念ながら、Stripe Checkout は、サブスクリプションの開始時にすべてのサブスクリプション請求オプションをサポートしているわけではありません。サブスクリプションビルダでの `anchorBillingCycleOn` メソッドの使用、比例配分動作の設定、または支払い動作の設定は、Stripe Checkout セッション中には影響しません。使用可能なパラメータを確認するには、[Stripe チェックアウト セッション API ドキュメント](https://stripe.com/docs/api/checkout/sessions/create) を参照してください。

<a name="stripe-checkout-trial-periods"></a>
#### Stripe チェックアウトと試用期間

もちろん、Stripe Checkout を使用して完了するサブスクリプションを構築するときに、試用期間を定義できます。

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

ただし、試用期間は少なくとも 48 時間である必要があります。これは、Stripe Checkout でサポートされる最小試用時間です。

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### サブスクリプションとWebhook

Stripe と Cashier は Webhook 経由でサブスクリプションのステータスを更新するため、顧客が支払い情報を入力した後にアプリケーションに戻った時点では、サブスクリプションがまだ有効になっていない可能性があることに注意してください。このシナリオに対処するには、支払いまたはサブスクリプションが保留中であることをユーザーに通知するメッセージを表示することができます。

<a name="collecting-tax-ids"></a>
### 納税者番号の収集

Checkout では、顧客の納税者 ID の収集もサポートされています。チェックアウト セッションでこれを有効にするには、セッションの作成時に `collectTaxIds` メソッドを呼び出します。

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

このメソッドを呼び出すと、顧客は会社として購入するかどうかを示す新しいチェックボックスが利用できるようになります。その場合、納税者 ID 番号を提供する機会が得られます。

> [!WARNING]
> アプリケーションのサービスプロバイダで [自動税徴収](#tax-configuration) をすでに構成している場合、この機能は自動的に有効になり、`collectTaxIds` メソッドを呼び出す必要はありません。

<a name="guest-checkouts"></a>
### ゲストのチェックアウト

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

ゲストのチェックアウトが完了すると、Stripe は `checkout.session.completed` Webhook イベントを送信できるため、必ず [Stripe Webhook を設定する](https://dashboard.stripe.com/webhooks) を実行してこのイベントを実際にアプリケーションに送信してください。 Stripe ダッシュボード内で Webhook が有効になったら、[Cashier で Webhook を処理する](#handling-stripe-webhooks) を行うことができます。 Webhook ペイロードに含まれるオブジェクトは [チェックアウトオブジェクト](https://stripe.com/docs/api/checkout/sessions/object) となり、顧客の注文を満たすために検査できます。

<a name="handling-failed-payments"></a>
## 失敗した支払いの処理 (Handling Failed Payments)

場合によっては、サブスクリプションまたは単一料金の支払いが失敗することがあります。これが発生すると、Cashier はこれが発生したことを通知する `Laravel\Cashier\Exceptions\IncompletePayment` 例外をスローします。この例外をキャッチした後、続行する方法には 2 つのオプションがあります。

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

支払い確認ページで、顧客はクレジット カード情報を再度入力し、「3D セキュア」確認など、Stripe で必要な追加のアクションを実行するよう求められます。支払いを確認した後、ユーザーは上で指定した `redirect` パラメータで指定された URL にリダイレクトされます。リダイレクト時に、`message` (文字列) および `success` (整数) クエリ文字列変数が URL に追加されます。支払いページでは現在、次のタイプの支払い方法がサポートされています。

<div class="content-list" markdown="1">

- クレジットカード
- アリペイ
- バンコンタクト
- BECS 口座振替
- EPS
- ギロペイ
- 理想的
- SEPA 口座振替

</div>

あるいは、Stripe が支払い確認を処理できるようにすることもできます。この場合、支払い確認ページにリダイレクトする代わりに、Stripe ダッシュボードで [Stripe の自動請求メールを設定する](https://dashboard.stripe.com/account/billing/automatic) を実行できます。ただし、`IncompletePayment` 例外がキャッチされた場合でも、支払い確認の手順が記載された電子メールを受け取ることをユーザーに通知する必要があります。

支払い例外は、`Billable` トレイトを使用するモデルの `charge`、`invoiceFor`、および `invoice` のメソッドに対してスローされる可能性があります。サブスクリプションを操作するとき、`SubscriptionBuilder` の `create` メソッド、および `Subscription` および `SubscriptionItem` モデルの `incrementAndInvoice` および `swapAndInvoice` メソッドは、不完全な支払い例外をスローする場合があります。

既存のサブスクリプションに支払いが完了していないかどうかを判断するには、請求可能モデルまたはサブスクリプション インスタンスで `hasIncompletePayment` メソッドを使用します。

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

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
### 支払いの確認

一部の支払い方法では、支払いを確認するために追加のデータが必要です。たとえば、SEPA 支払い方法では、支払いプロセス中に追加の「委任」データが必要になります。 `withPaymentConfirmationOptions` メソッドを使用して、このデータをCashierに提供できます。

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

[Stripe API ドキュメント](https://stripe.com/docs/api/payment_intents/confirm) を参照して、支払いを確認するときに受け入れられるすべてのオプションを確認することができます。

<a name="strong-customer-authentication"></a>
## 強力な顧客認証 (Strong Customer Authentication)

あなたのビジネスまたは顧客のいずれかがヨーロッパに拠点を置いている場合は、EU の強力な顧客認証 (SCA) 規制に従う必要があります。これらの規制は、支払い詐欺を防止するために 2019 年 9 月に欧州連合によって課されました。幸いなことに、Stripe と Cashier は SCA 準拠のアプリケーションを構築する準備ができています。

> [!WARNING]
> 始める前に、[PSD2 と SCA に関する Stripe のガイド](https://stripe.com/guides/strong-customer-authentication) と [新しい SCA API に関するドキュメント](https://stripe.com/docs/strong-customer-authentication) を確認してください。

<a name="payments-requiring-additional-confirmation"></a>
### 追加の確認が必要な支払い

SCA 規制では、支払いを確認して処理するために追加の検証が必要になることがよくあります。これが発生すると、Cashier は追加の検証が必要であることを通知する `Laravel\Cashier\Exceptions\IncompletePayment` 例外をスローします。これらの例外を処理する方法の詳細については、[失敗した支払いの処理](#handling-failed-payments) のドキュメントを参照してください。

Stripe または Cashier によって表示される支払い確認画面は、特定の銀行またはカード発行会社の支払いフローに合わせて調整することができ、追加のカード確認、一時的な少額請求、個別のデバイス認証、またはその他の形式の確認を含めることができます。

<a name="incomplete-and-past-due-state"></a>
#### 未完了および期限超過の状態

支払いに追加の確認が必要な場合、サブスクリプションは、`stripe_status` データベース列で示されるように、`incomplete` または `past_due` 状態のままになります。支払い確認が完了し、Stripe から Webhook 経由でアプリケーションに完了が通知されると、Cashier は顧客のサブスクリプションを自動的にアクティブ化します。

`incomplete` および `past_due` 状態の詳細については、[これらの状態に関する追加のドキュメント](#incomplete-and-past-due-status) を参照してください。

<a name="off-session-payment-notifications"></a>
### オフセッション支払い通知

SCA 規制により、顧客はサブスクリプションがアクティブな間でも支払いの詳細を時折確認する必要があるため、セッション外の支払い確認が必要な場合、Cashierは顧客に通知を送信できます。たとえば、これはサブスクリプションの更新時に発生する可能性があります。Cashierの支払い通知は、`CASHIER_PAYMENT_NOTIFICATION` 環境変数を通知クラスに設定することで有効にできます。デフォルトでは、この通知は無効になっています。もちろん、Cashier にはこの目的に使用できる通知クラスが含まれていますが、必要に応じて独自の通知クラスを自由に提供できます。

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

セッション外の支払い確認通知が確実に配信されるようにするには、アプリケーションの [Stripe Webhook が設定されている](#handling-stripe-webhooks) と `invoice.payment_action_required` Webhook が Stripe ダッシュボードで有効になっていることを確認してください。さらに、`Billable` モデルは Laravel の `Illuminate\Notifications\Notifiable` トレイトも使用する必要があります。

> [!WARNING]
> 顧客が追加の確認が必要な支払いを手動で行っている場合でも、通知は送信されます。残念ながら、Stripe には支払いが手動で行われたのか、または「オフセッション」で行われたのかを知る方法がありません。ただし、顧客が支払いを確認した後に支払いページにアクセスすると、単に「支払いが成功しました」というメッセージが表示されます。顧客が誤って同じ支払いを 2 回確認して、誤って 2 回目の請求が発生することは許されません。

<a name="stripe-sdk"></a>
## StripeSDK (Stripe SDK)

Cashier のオブジェクトの多くは、Stripe SDK オブジェクトのラッパーです。 Stripe オブジェクトを直接操作したい場合は、`asStripe` メソッドを使用してオブジェクトを簡単に取得できます。

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

`updateStripeSubscription` メソッドを使用して、Stripe サブスクリプションを直接更新することもできます。

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

`Stripe\StripeClient` クライアントを直接使用したい場合は、`Cashier` クラスの `stripe` メソッドを呼び出すことができます。たとえば、このメソッドを使用して `StripeClient` インスタンスにアクセスし、Stripe アカウントから価格のリストを取得できます。

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## テスト (Testing)

Cashier を使用するアプリケーションをテストする場合、Stripe API への実際の HTTP リクエストをモックすることができます。ただし、これには、Cashier 自体の動作を部分的に再実装する必要があります。したがって、テストが実際の Stripe API にアクセスできるようにすることをお勧めします。これは遅くなりますが、アプリケーションが期待どおりに動作しているという信頼性が高まり、遅いテストは独自の Pest / PHPUnit テスト グループ内に配置される可能性があります。

テストするときは、Cashier 自体に優れたテスト スイートがすでに用意されているため、基礎となる Cashier の動作をすべてテストするのではなく、独自のアプリケーションのサブスクリプションと支払いフローのテストにのみ重点を置く必要があることに注意してください。

まず、**テスト** バージョンの Stripe シークレットを `phpunit.xml` ファイルに追加します。

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

これで、テスト中に Cashier と対話するたびに、実際の API リクエストが Stripe テスト環境に送信されます。便宜上、Stripe テスト アカウントにテスト中に使用するサブスクリプション/価格を事前に入力しておく必要があります。

> [!NOTE]
> クレジット カードの拒否や失敗など、さまざまな請求シナリオをテストするために、Stripe が提供する幅広い [カード番号とトークンのテスト](https://stripe.com/docs/testing) を使用できます。

