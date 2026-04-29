# Laravel Cashier (Paddle) (Laravel Cashier (Paddle))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [설정](#configuration)
    - [청구 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [제품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [Checkout 세션](#checkout-sessions)
    - [오버레이 Checkout](#overlay-checkout)
    - [인라인 Checkout](#inline-checkout)
    - [게스트 Checkout](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객 가격 미리보기](#customer-price-previews)
    - [할인](#price-discounts)
- [고객](#customers)
    - [고객 기본값](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단건 청구](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [여러 제품을 포함하는 구독](#subscriptions-with-multiple-products)
    - [여러 구독](#multiple-subscriptions)
    - [구독 일시 중지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 수단을 미리 받는 경우](#with-payment-method-up-front)
    - [결제 수단을 미리 받지 않는 경우](#without-payment-method-up-front)
    - [체험 기간 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle Webhook 처리](#handling-paddle-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단건 청구](#single-charges)
    - [제품 청구](#charging-for-products)
    - [트랜잭션 환불](#refunding-transactions)
    - [트랜잭션 크레딧 처리](#crediting-transactions)
- [트랜잭션](#transactions)
    - [과거 및 예정 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 이 문서는 Cashier Paddle 2.x와 Paddle Billing의 통합에 관한 문서입니다. 아직 Paddle Classic을 사용하고 있다면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 사용해야 합니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 청구 서비스에 대해 표현력 있고 유창한 인터페이스를 제공합니다. 신경 쓰고 싶지 않은 거의 모든 반복적인 구독 청구 코드를 처리해 줍니다. 기본적인 구독 관리 외에도 Cashier는 구독 교체, 구독 "수량", 구독 일시 중지, 취소 유예 기간 등을 처리할 수 있습니다.

Cashier Paddle을 자세히 살펴보기 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 검토하는 것을 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용하여 Paddle용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier-paddle
```

다음으로 `vendor:publish` Artisan 명령어를 사용하여 Cashier 마이그레이션 파일을 게시해야 합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그런 다음 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. Cashier 마이그레이션은 새 `customers` 테이블을 생성합니다. 또한 고객의 모든 구독을 저장하기 위해 새 `subscriptions` 및 `subscription_items` 테이블이 생성됩니다. 마지막으로 고객과 연결된 모든 Paddle 트랜잭션을 저장하기 위해 새 `transactions` 테이블이 생성됩니다.

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 올바르게 처리하도록 하려면 [Cashier의 webhook 처리 설정](#handling-paddle-webhooks)을 잊지 마십시오.

<a name="paddle-sandbox"></a>
### Paddle Sandbox

로컬 및 스테이징 개발 중에는 [Paddle Sandbox 계정](https://sandbox-login.paddle.com/signup)을 등록해야 합니다. 이 계정은 실제 결제를 하지 않고 애플리케이션을 테스트하고 개발할 수 있는 sandbox 환경을 제공합니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 사용하여 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

Paddle Sandbox 환경을 사용할 때는 애플리케이션의 `.env` 파일에서 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다.

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발을 마친 후에는 [Paddle vendor 계정 신청](https://paddle.com)을 할 수 있습니다. 애플리케이션을 프로덕션에 배포하기 전에 Paddle이 애플리케이션의 도메인을 승인해야 합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 청구 가능 모델

Cashier를 사용하기 전에 사용자 모델 정의에 `Billable` trait를 추가해야 합니다. 이 trait는 구독 생성과 결제 수단 정보 업데이트 같은 일반적인 청구 작업을 수행할 수 있도록 다양한 메서드를 제공합니다.

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 청구 가능 엔티티가 있다면 해당 클래스에도 trait를 추가할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
### API 키

다음으로 애플리케이션의 `.env` 파일에서 Paddle 키를 설정해야 합니다. Paddle control panel에서 Paddle API 키를 확인할 수 있습니다.

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

[Paddle의 Sandbox 환경](#paddle-sandbox)을 사용할 때는 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다. 애플리케이션을 프로덕션에 배포하고 Paddle의 live vendor 환경을 사용하는 경우에는 `PADDLE_SANDBOX` 변수를 `false`로 설정해야 합니다.

`PADDLE_RETAIN_KEY`는 선택 사항이며 Paddle을 [Retain](https://developer.paddle.com/concepts/retain/overview)과 함께 사용하는 경우에만 설정해야 합니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 Paddle checkout widget을 시작하기 위해 자체 JavaScript 라이브러리에 의존합니다. 애플리케이션 레이아웃의 닫는 `</head>` 태그 바로 앞에 `@paddleJS` Blade directive를 배치하여 JavaScript 라이브러리를 로드할 수 있습니다.

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

인보이스에 표시할 금액 값을 형식화할 때 사용할 locale을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용하여 통화 locale을 설정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 locale을 사용하려면 서버에 `ext-intl` PHP 확장이 설치되고 설정되어 있는지 확인하십시오.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

자체 모델을 정의하고 해당 Cashier 모델을 확장하여 Cashier가 내부적으로 사용하는 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후에는 `Laravel\Paddle\Cashier` 클래스를 통해 Cashier가 사용자 정의 모델을 사용하도록 지시할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 Cashier에 사용자 정의 모델을 알려야 합니다.

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
## 빠른 시작 (Quickstart)

<a name="quickstart-selling-products"></a>
### 제품 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전에 Paddle dashboard에서 고정 가격이 있는 Products를 정의해야 합니다. 또한 [Paddle의 webhook 처리](#handling-paddle-webhooks)를 설정해야 합니다.

애플리케이션을 통해 제품 및 구독 청구를 제공하는 일은 부담스러울 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 덕분에 현대적이고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

반복 청구가 아닌 단건 청구 제품에 대해 고객에게 청구하려면 Cashier를 사용하여 Paddle의 Checkout Overlay로 고객에게 청구합니다. 이 과정에서 고객은 결제 정보를 입력하고 구매를 확인합니다. Checkout Overlay를 통해 결제가 완료되면 고객은 애플리케이션 내에서 사용자가 선택한 성공 URL로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예제에서 볼 수 있듯이, Cashier가 제공하는 `checkout` 메서드를 사용하여 checkout 객체를 생성하고, 지정된 "price identifier"에 대한 Paddle Checkout Overlay를 고객에게 표시합니다. Paddle을 사용할 때 "prices"는 [특정 제품에 대해 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요한 경우 `checkout` 메서드는 Paddle에 고객을 자동으로 생성하고, 해당 Paddle 고객 레코드를 애플리케이션 데이터베이스의 해당 사용자와 연결합니다. checkout 세션이 완료되면 고객은 전용 성공 페이지로 리디렉션되며, 이 페이지에서 고객에게 안내 메시지를 표시할 수 있습니다.

`buy` view에는 Checkout Overlay를 표시하기 위한 버튼을 포함합니다. `paddle-button` Blade component는 Cashier Paddle에 포함되어 있지만, [오버레이 checkout을 직접 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타데이터 제공

제품을 판매할 때는 애플리케이션에서 직접 정의한 `Cart` 및 `Order` 모델을 통해 완료된 주문과 구매한 제품을 추적하는 것이 일반적입니다. 구매를 완료하도록 고객을 Paddle의 Checkout Overlay로 리디렉션할 때, 고객이 애플리케이션으로 다시 리디렉션되었을 때 완료된 구매를 해당 주문과 연결할 수 있도록 기존 주문 식별자를 제공해야 할 수 있습니다.

이를 위해 `checkout` 메서드에 사용자 정의 데이터 배열을 제공할 수 있습니다. 사용자가 checkout 프로세스를 시작할 때 애플리케이션 내에서 대기 중인 `Order`가 생성된다고 가정해 보겠습니다. 이 예제의 `Cart` 및 `Order` 모델은 설명을 위한 것이며 Cashier가 제공하지 않는다는 점을 기억하십시오. 이러한 개념은 애플리케이션의 필요에 따라 자유롭게 구현할 수 있습니다.

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

위 예제에서 볼 수 있듯이, 사용자가 checkout 프로세스를 시작하면 cart / order와 연결된 모든 Paddle price identifier를 `checkout` 메서드에 제공합니다. 물론 고객이 항목을 추가할 때 이러한 항목을 "shopping cart" 또는 주문과 연결하는 책임은 애플리케이션에 있습니다. 또한 `customData` 메서드를 통해 주문의 ID를 Paddle Checkout Overlay에 제공합니다.

물론 고객이 checkout 프로세스를 완료하면 주문을 "complete"로 표시하고 싶을 것입니다. 이를 위해 Paddle이 발송하고 Cashier가 이벤트로 발생시키는 webhook을 수신하여 주문 정보를 데이터베이스에 저장할 수 있습니다.

시작하려면 Cashier가 발송하는 `TransactionCompleted` 이벤트를 수신하십시오. 일반적으로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트 리스너를 등록해야 합니다.

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

이 예제에서 `CompleteOrder` 리스너는 다음과 같을 수 있습니다.

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

[`transaction.completed` 이벤트에 포함된 데이터](https://developer.paddle.com/webhooks/transactions/transaction-completed)에 대한 자세한 내용은 Paddle 문서를 참조하십시오.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전에 Paddle dashboard에서 고정 가격이 있는 Products를 정의해야 합니다. 또한 [Paddle의 webhook 처리](#handling-paddle-webhooks)를 설정해야 합니다.

애플리케이션을 통해 제품 및 구독 청구를 제공하는 일은 부담스러울 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 덕분에 현대적이고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

Cashier와 Paddle의 Checkout Overlay를 사용하여 구독을 판매하는 방법을 알아보기 위해, 기본 월간(`price_basic_monthly`) 플랜과 연간(`price_basic_yearly`) 플랜이 있는 구독 서비스라는 간단한 시나리오를 생각해 보겠습니다. 이 두 가격은 Paddle dashboard에서 "Basic" 제품(`pro_basic`) 아래에 그룹화할 수 있습니다. 또한 구독 서비스는 `pro_expert`라는 "Expert" 플랜을 제공할 수도 있습니다.

먼저 고객이 서비스에 구독하는 방법을 알아보겠습니다. 물론 고객은 애플리케이션의 가격 페이지에서 Basic 플랜의 "subscribe" 버튼을 클릭할 수 있습니다. 이 버튼은 고객이 선택한 플랜에 대한 Paddle Checkout Overlay를 호출합니다. 시작하려면 `checkout` 메서드를 통해 checkout 세션을 시작해 보겠습니다.

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` view에는 Checkout Overlay를 표시하기 위한 버튼을 포함합니다. `paddle-button` Blade component는 Cashier Paddle에 포함되어 있지만, [오버레이 checkout을 직접 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 Subscribe 버튼을 클릭하면 고객은 결제 정보를 입력하고 구독을 시작할 수 있습니다. 일부 결제 수단은 처리에 몇 초가 걸리므로 실제로 구독이 시작된 시점을 알기 위해 [Cashier의 webhook 처리](#handling-paddle-webhooks)도 설정해야 합니다.

이제 고객이 구독을 시작할 수 있으므로, 애플리케이션의 특정 영역은 구독한 사용자만 접근할 수 있도록 제한해야 합니다. 물론 Cashier의 `Billable` trait가 제공하는 `subscribed` 메서드를 통해 언제든지 사용자의 현재 구독 상태를 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

사용자가 특정 제품 또는 가격에 구독 중인지도 쉽게 확인할 수 있습니다.

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 확인 Middleware 만들기

편의를 위해 들어오는 요청이 구독한 사용자로부터 온 것인지 확인하는 [middleware](/docs/master/middleware)를 만들 수 있습니다. 이 middleware를 정의한 후에는 라우트에 쉽게 할당하여 구독하지 않은 사용자가 해당 라우트에 접근하지 못하도록 막을 수 있습니다.

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

middleware가 정의되면 라우트에 할당할 수 있습니다.
```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 자신의 청구 요금제를 관리하도록 허용하기

물론 고객은 자신의 구독 요금제를 다른 상품이나 "티어"로 변경하고 싶을 수 있습니다. 위 예시에서는 고객이 월간 구독에서 연간 구독으로 요금제를 변경할 수 있도록 해야 합니다. 이를 위해 아래 라우트로 이어지는 버튼과 같은 기능을 구현해야 합니다.

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // With "$price" being "price_basic_yearly" for this example.

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

요금제 변경 외에도 고객이 구독을 취소할 수 있도록 해야 합니다. 요금제 변경과 마찬가지로, 다음 라우트로 이어지는 버튼을 제공하세요.

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이제 구독은 청구 기간이 끝날 때 취소됩니다.

> [!NOTE]
> Cashier의 Webhook 처리를 설정해 두었다면, Cashier는 Paddle에서 들어오는 Webhook을 확인하여 애플리케이션의 Cashier 관련 데이터베이스 테이블을 자동으로 동기화합니다. 예를 들어 Paddle 대시보드에서 고객의 구독을 취소하면, Cashier가 해당 Webhook을 수신하고 애플리케이션 데이터베이스에서 구독을 "canceled" 상태로 표시합니다.

<a name="checkout-sessions"></a>
## 체크아웃 세션 (Checkout Sessions)

고객에게 비용을 청구하는 대부분의 작업은 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)을 통한 "체크아웃" 또는 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 사용하여 수행됩니다.

Paddle로 체크아웃 결제를 처리하기 전에, Paddle 체크아웃 설정 대시보드에서 애플리케이션의 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 정의해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 체크아웃

Checkout Overlay 위젯을 표시하기 전에 Cashier를 사용하여 체크아웃 세션을 생성해야 합니다. 체크아웃 세션은 수행해야 할 청구 작업을 체크아웃 위젯에 알려줍니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier에는 `paddle-button` [Blade 컴포넌트](/docs/master/blade#components)가 포함되어 있습니다. 체크아웃 세션을 이 컴포넌트에 "prop"으로 전달할 수 있습니다. 그러면 이 버튼을 클릭했을 때 Paddle의 체크아웃 위젯이 표시됩니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 이 위젯은 Paddle의 기본 스타일을 사용하여 표시됩니다. 컴포넌트에 `data-theme='light'` 속성과 같은 [Paddle 지원 속성](https://developer.paddle.com/paddlejs/html-data-attributes)을 추가하여 위젯을 사용자 정의할 수 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기 방식으로 동작합니다. 사용자가 위젯 안에서 구독을 생성하면 Paddle은 애플리케이션에 Webhook을 보내며, 이를 통해 애플리케이션 데이터베이스의 구독 상태를 올바르게 업데이트할 수 있습니다. 따라서 Paddle의 상태 변경을 처리할 수 있도록 [Webhook을 올바르게 설정](#handling-paddle-webhooks)하는 것이 중요합니다.

> [!WARNING]
> 구독 상태가 변경된 후 해당 Webhook을 받기까지의 지연은 일반적으로 매우 짧지만, 체크아웃 완료 직후에는 사용자의 구독을 즉시 사용할 수 없을 수도 있다는 점을 애플리케이션에서 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃을 수동으로 렌더링하기

Laravel에 내장된 Blade 컴포넌트를 사용하지 않고 오버레이 체크아웃을 수동으로 렌더링할 수도 있습니다. 시작하려면 [이전 예시에서 보여준 것처럼](#overlay-checkout) 체크아웃 세션을 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

다음으로 Paddle.js를 사용하여 체크아웃을 초기화할 수 있습니다. 이 예시에서는 `paddle_button` 클래스가 지정된 링크를 생성합니다. Paddle.js는 이 클래스를 감지하고 링크를 클릭했을 때 오버레이 체크아웃을 표시합니다.

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
### 인라인 체크아웃

Paddle의 "오버레이" 스타일 체크아웃 위젯을 사용하고 싶지 않다면, Paddle은 위젯을 인라인으로 표시하는 옵션도 제공합니다. 이 방식은 체크아웃의 HTML 필드를 조정할 수는 없지만, 애플리케이션 안에 위젯을 삽입할 수 있습니다.

인라인 체크아웃을 쉽게 시작할 수 있도록 Cashier에는 `paddle-checkout` Blade 컴포넌트가 포함되어 있습니다. 시작하려면 [체크아웃 세션을 생성](#overlay-checkout)해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그런 다음 체크아웃 세션을 컴포넌트의 `checkout` 속성에 전달할 수 있습니다.

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 체크아웃 컴포넌트의 높이를 조정하려면 Blade 컴포넌트에 `height` 속성을 전달할 수 있습니다.

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

인라인 체크아웃의 사용자 정의 옵션에 대한 자세한 내용은 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [사용 가능한 체크아웃 설정](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)을 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃을 수동으로 렌더링하기

Laravel에 내장된 Blade 컴포넌트를 사용하지 않고 인라인 체크아웃을 수동으로 렌더링할 수도 있습니다. 시작하려면 [이전 예시에서 보여준 것처럼](#inline-checkout) 체크아웃 세션을 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

다음으로 Paddle.js를 사용하여 체크아웃을 초기화할 수 있습니다. 이 예시에서는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하여 보여주지만, 자신의 프론트엔드 스택에 맞게 자유롭게 수정할 수 있습니다.

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
### 게스트 체크아웃

때로는 애플리케이션 계정이 필요하지 않은 사용자를 위해 체크아웃 세션을 생성해야 할 수 있습니다. 이렇게 하려면 `guest` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

그런 다음 체크아웃 세션을 [Paddle 버튼](#overlay-checkout) 또는 [인라인 체크아웃](#inline-checkout) Blade 컴포넌트에 제공할 수 있습니다.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle은 통화별로 가격을 사용자 정의할 수 있게 해 주며, 사실상 국가별로 서로 다른 가격을 설정할 수 있습니다. Cashier Paddle은 `previewPrices` 메서드를 사용하여 이러한 가격을 모두 가져올 수 있게 해 줍니다. 이 메서드는 가격을 가져오려는 가격 ID를 인수로 받습니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

통화는 요청의 IP 주소를 기준으로 결정됩니다. 다만 특정 국가를 직접 지정하여 해당 국가의 가격을 가져올 수도 있습니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

가격을 가져온 후에는 원하는 방식으로 표시할 수 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

소계 가격과 세금 금액을 따로 표시할 수도 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

자세한 내용은 [가격 미리보기와 관련된 Paddle의 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 확인하세요.

<a name="customer-price-previews"></a>
### 고객 가격 미리보기

사용자가 이미 고객이고 해당 고객에게 적용되는 가격을 표시하고 싶다면, 고객 인스턴스에서 직접 가격을 가져올 수 있습니다.

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

내부적으로 Cashier는 사용자의 고객 ID를 사용하여 해당 사용자의 통화로 가격을 가져옵니다. 예를 들어 미국에 거주하는 사용자는 미국 달러 가격을 보게 되고, 벨기에에 거주하는 사용자는 유로 가격을 보게 됩니다. 일치하는 통화를 찾을 수 없다면 상품의 기본 통화가 사용됩니다. Paddle 제어판에서 상품 또는 구독 요금제의 모든 가격을 사용자 정의할 수 있습니다.

<a name="price-discounts"></a>
### 할인

할인이 적용된 가격을 표시할 수도 있습니다. `previewPrices` 메서드를 호출할 때 `discount_id` 옵션을 통해 할인 ID를 제공합니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

그런 다음 계산된 가격을 표시합니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

<a name="customers"></a>
## 고객 (Customers)

<a name="customer-defaults"></a>
### 고객 기본값

Cashier는 체크아웃 세션을 생성할 때 고객에 대한 유용한 기본값을 정의할 수 있게 해 줍니다. 이러한 기본값을 설정하면 고객의 이메일 주소와 이름을 미리 채울 수 있으므로, 고객은 체크아웃 위젯에서 바로 결제 단계로 이동할 수 있습니다. 결제 가능 모델에서 다음 메서드를 오버라이드하여 이러한 기본값을 설정할 수 있습니다.

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

이 기본값은 [체크아웃 세션](#checkout-sessions)을 생성하는 Cashier의 모든 작업에 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회

`Cashier::findBillable` 메서드를 사용하여 Paddle Customer ID로 고객을 조회할 수 있습니다. 이 메서드는 결제 가능 모델의 인스턴스를 반환합니다.

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성

때로는 구독을 시작하지 않고 Paddle 고객을 생성하고 싶을 수 있습니다. `createAsCustomer` 메서드를 사용하여 이를 수행할 수 있습니다.

```php
$customer = $user->createAsCustomer();
```

`Laravel\Paddle\Customer` 인스턴스가 반환됩니다. Paddle에 고객이 생성되면 나중에 구독을 시작할 수 있습니다. Paddle API에서 지원하는 추가 [고객 생성 파라미터](https://developer.paddle.com/api-reference/customers/create-customer)를 전달하려면 선택적으로 `$options` 배열을 제공할 수 있습니다.

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면 먼저 데이터베이스에서 결제 가능 모델의 인스턴스를 가져와야 합니다. 일반적으로 이는 `App\Models\User` 인스턴스입니다. 모델 인스턴스를 가져온 후에는 `subscribe` 메서드를 사용하여 해당 모델의 체크아웃 세션을 생성할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe` 메서드에 전달되는 첫 번째 인수는 사용자가 구독할 특정 가격입니다. 이 값은 Paddle의 가격 식별자와 일치해야 합니다. `returnTo` 메서드는 사용자가 체크아웃을 성공적으로 완료한 뒤 리디렉션될 URL을 받습니다. `subscribe` 메서드에 전달되는 두 번째 인수는 구독의 내부 "type"이어야 합니다. 애플리케이션이 하나의 구독만 제공한다면 이를 `default` 또는 `primary`라고 부를 수 있습니다. 이 구독 타입은 애플리케이션 내부 용도로만 사용되며 사용자에게 표시하기 위한 값이 아닙니다. 또한 공백을 포함해서는 안 되며, 구독을 생성한 후에는 절대 변경해서는 안 됩니다.

`customData` 메서드를 사용하여 구독과 관련된 사용자 정의 메타데이터 배열을 제공할 수도 있습니다.

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

구독 체크아웃 세션이 생성되면, 해당 체크아웃 세션을 Cashier Paddle에 포함된 `paddle-button` [Blade 컴포넌트](#overlay-checkout)에 전달할 수 있습니다.

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

사용자가 체크아웃을 완료하면 Paddle에서 `subscription_created` Webhook이 발송됩니다. Cashier는 이 Webhook을 수신하고 고객의 구독을 설정합니다. 모든 Webhook이 애플리케이션에서 올바르게 수신되고 처리되도록 하려면 [Webhook 처리 설정](#handling-paddle-webhooks)을 제대로 완료했는지 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

사용자가 애플리케이션을 구독하면, 여러 편리한 메서드를 사용하여 구독 상태를 확인할 수 있습니다. 먼저 `subscribed` 메서드는 사용자가 유효한 구독을 가지고 있다면, 해당 구독이 현재 체험 기간 중이더라도 `true`를 반환합니다.

```php
if ($user->subscribed()) {
    // ...
}
```

애플리케이션이 여러 구독을 제공한다면, `subscribed` 메서드를 호출할 때 구독을 지정할 수 있습니다.

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 Middleware](/docs/master/middleware)로도 매우 적합합니다. 이를 사용하면 사용자의 구독 상태에 따라 라우트와 컨트롤러에 대한 접근을 필터링할 수 있습니다.

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
사용자가 아직 체험 기간 안에 있는지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이 메서드는 사용자에게 아직 체험 기간 중이라는 경고를 표시해야 하는지 판단할 때 유용합니다.

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

`subscribedToPrice` 메서드는 주어진 Paddle 가격 ID를 기준으로 사용자가 특정 플랜을 구독 중인지 확인하는 데 사용할 수 있습니다. 다음 예제에서는 사용자의 `default` 구독이 월간 가격을 활성 상태로 구독 중인지 확인합니다.

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

`recurring` 메서드는 사용자가 현재 활성 구독 상태이며, 더 이상 체험 기간이나 유예 기간에 있지 않은지 확인하는 데 사용할 수 있습니다.

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태

사용자가 한때 활성 구독자였지만 구독을 취소했는지 확인하려면 `canceled` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

사용자가 구독을 취소했지만 구독이 완전히 만료되기 전까지 "유예 기간"에 있는지도 확인할 수 있습니다. 예를 들어 사용자가 원래 3월 10일에 만료될 예정이던 구독을 3월 5일에 취소했다면, 사용자는 3월 10일까지 "유예 기간"에 있습니다. 또한 이 기간 동안 `subscribed` 메서드는 계속 `true`를 반환합니다.

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 결제 연체 상태

구독 결제가 실패하면 해당 구독은 `past_due`로 표시됩니다. 구독이 이 상태일 때는 고객이 결제 정보를 업데이트하기 전까지 활성 상태가 아닙니다. 구독 인스턴스에서 `pastDue` 메서드를 사용하여 구독이 결제 연체 상태인지 확인할 수 있습니다.

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

구독이 결제 연체 상태라면 사용자에게 [결제 정보를 업데이트](#updating-payment-information)하도록 안내해야 합니다.

구독이 `past_due` 상태일 때도 여전히 유효한 것으로 간주하고 싶다면 Cashier가 제공하는 `keepPastDueSubscriptionsActive` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 `AppServiceProvider`의 `register` 메서드에서 호출해야 합니다.

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
> 구독이 `past_due` 상태이면 결제 정보가 업데이트되기 전까지 변경할 수 없습니다. 따라서 구독이 `past_due` 상태일 때 `swap` 및 `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 스코프

대부분의 구독 상태는 쿼리 스코프로도 제공되므로, 특정 상태의 구독을 데이터베이스에서 쉽게 조회할 수 있습니다.

```php
// Get all valid subscriptions...
$subscriptions = Subscription::query()->valid()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 전체 스코프 목록은 다음과 같습니다.

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
### 구독 단건 청구

구독 단건 청구를 사용하면 구독자에게 구독 요금과 별도로 일회성 요금을 청구할 수 있습니다. `charge` 메서드를 호출할 때 하나 이상의 가격 ID를 제공해야 합니다.

```php
// Charge a single price...
$response = $user->subscription()->charge('pri_123');

// Charge multiple prices at once...
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge` 메서드는 고객의 다음 구독 결제 주기까지 실제로 요금을 청구하지 않습니다. 고객에게 즉시 청구하려면 대신 `chargeAndInvoice` 메서드를 사용할 수 있습니다.

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 항상 구독별로 결제 수단을 저장합니다. 구독의 기본 결제 수단을 업데이트하려면 구독 모델의 `redirectToUpdatePaymentMethod` 메서드를 사용하여 고객을 Paddle이 호스팅하는 결제 수단 업데이트 페이지로 리디렉션해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

사용자가 정보 업데이트를 완료하면 Paddle이 `subscription_updated` Webhook을 발송하고, 애플리케이션 데이터베이스의 구독 상세 정보가 업데이트됩니다.

<a name="changing-plans"></a>
### 플랜 변경

사용자가 애플리케이션을 구독한 뒤에는 가끔 새로운 구독 플랜으로 변경하고 싶어 할 수 있습니다. 사용자의 구독 플랜을 업데이트하려면 Paddle 가격의 식별자를 구독의 `swap` 메서드에 전달해야 합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

다음 결제 주기까지 기다리지 않고 플랜을 변경하면서 사용자에게 즉시 인보이스를 발행하려면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 일할 계산

기본적으로 Paddle은 플랜을 변경할 때 요금을 일할 계산합니다. `noProrate` 메서드를 사용하면 요금을 일할 계산하지 않고 구독을 업데이트할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

일할 계산을 비활성화하고 고객에게 즉시 인보이스를 발행하려면 `noProrate`와 함께 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

또는 구독 변경에 대해 고객에게 요금을 청구하지 않으려면 `doNotBill` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

Paddle의 일할 계산 정책에 대한 자세한 내용은 Paddle의 [일할 계산 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하십시오.

<a name="subscription-quantity"></a>
### 구독 수량

구독은 때때로 "수량"의 영향을 받습니다. 예를 들어 프로젝트 관리 애플리케이션은 프로젝트당 월 $10를 청구할 수 있습니다. 구독 수량을 쉽게 늘리거나 줄이려면 `incrementQuantity` 및 `decrementQuantity` 메서드를 사용하십시오.

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription()->decrementQuantity(5);
```

또는 `updateQuantity` 메서드를 사용하여 특정 수량을 설정할 수 있습니다.

```php
$user->subscription()->updateQuantity(10);
```

`noProrate` 메서드를 사용하면 요금을 일할 계산하지 않고 구독 수량을 업데이트할 수 있습니다.

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 상품이 있는 구독의 수량

구독이 [여러 상품이 있는 구독](#subscriptions-with-multiple-products)이라면, 수량을 늘리거나 줄이려는 가격의 ID를 증가 / 감소 메서드의 두 번째 인수로 전달해야 합니다.

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 상품이 있는 구독

[여러 상품이 있는 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)을 사용하면 하나의 구독에 여러 결제 상품을 할당할 수 있습니다. 예를 들어 월 $10의 기본 구독 가격을 가진 고객 서비스 "헬프데스크" 애플리케이션을 만들고 있으며, 월 $15의 추가 요금으로 라이브 채팅 애드온 상품을 제공한다고 가정해 보겠습니다.

구독 결제 세션을 만들 때 `subscribe` 메서드의 첫 번째 인수로 가격 배열을 전달하여 특정 구독에 여러 상품을 지정할 수 있습니다.

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

위 예제에서 고객의 `default` 구독에는 두 개의 가격이 연결됩니다. 두 가격은 각각의 결제 주기에 따라 청구됩니다. 필요한 경우 각 가격의 특정 수량을 지정하기 위해 키 / 값 쌍의 연관 배열을 전달할 수 있습니다.

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 다른 가격을 추가하려면 구독의 `swap` 메서드를 사용해야 합니다. `swap` 메서드를 호출할 때는 구독의 현재 가격과 수량도 함께 포함해야 합니다.

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

위 예제는 새 가격을 추가하지만, 고객에게는 다음 결제 주기까지 해당 요금이 청구되지 않습니다. 고객에게 즉시 청구하려면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

`swap` 메서드를 사용하면서 제거하려는 가격을 생략하면 구독에서 가격을 제거할 수 있습니다.

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독의 마지막 가격은 제거할 수 없습니다. 대신 구독을 취소해야 합니다.

<a name="multiple-subscriptions"></a>
### 여러 구독

Paddle은 고객이 여러 구독을 동시에 가질 수 있도록 허용합니다. 예를 들어 수영 구독과 웨이트 트레이닝 구독을 제공하는 헬스장을 운영할 수 있으며, 각 구독에는 서로 다른 가격이 적용될 수 있습니다. 물론 고객은 두 플랜 중 하나만 또는 둘 다 구독할 수 있어야 합니다.

애플리케이션에서 구독을 만들 때 `subscribe` 메서드의 두 번째 인수로 구독의 유형을 제공할 수 있습니다. 유형은 사용자가 시작하는 구독의 종류를 나타내는 어떤 문자열이든 될 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

이 예제에서는 고객을 위해 월간 수영 구독을 시작했습니다. 하지만 나중에 연간 구독으로 변경하고 싶어 할 수 있습니다. 고객의 구독을 조정할 때는 `swimming` 구독의 가격만 변경하면 됩니다.

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

물론 구독을 완전히 취소할 수도 있습니다.

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시 중지

구독을 일시 중지하려면 사용자의 구독에서 `pause` 메서드를 호출하십시오.

```php
$user->subscription()->pause();
```

구독이 일시 중지되면 Cashier는 데이터베이스의 `paused_at` 컬럼을 자동으로 설정합니다. 이 컬럼은 `paused` 메서드가 언제부터 `true`를 반환해야 하는지 판단하는 데 사용됩니다. 예를 들어 고객이 3월 1일에 구독을 일시 중지했지만, 해당 구독이 3월 5일까지 갱신될 예정이 아니었다면 `paused` 메서드는 3월 5일까지 계속 `false`를 반환합니다. 일반적으로 사용자는 결제 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있기 때문입니다.

기본적으로 일시 중지는 다음 결제 주기에 적용되므로 고객은 이미 결제한 기간의 남은 부분을 사용할 수 있습니다. 구독을 즉시 일시 중지하려면 `pauseNow` 메서드를 사용할 수 있습니다.

```php
$user->subscription()->pauseNow();
```

`pauseUntil` 메서드를 사용하면 특정 시점까지 구독을 일시 중지할 수 있습니다.

```php
$user->subscription()->pauseUntil(now()->plus(months: 1));
```

또는 `pauseNowUntil` 메서드를 사용하여 구독을 즉시 일시 중지하고 지정한 시점까지 유지할 수 있습니다.

```php
$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```

사용자가 구독을 일시 중지했지만 아직 "유예 기간"에 있는지는 `onPausedGracePeriod` 메서드를 사용하여 확인할 수 있습니다.

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

일시 중지된 구독을 재개하려면 구독에서 `resume` 메서드를 호출하면 됩니다.

```php
$user->subscription()->resume();
```

> [!WARNING]
> 구독이 일시 중지된 동안에는 수정할 수 없습니다. 다른 플랜으로 변경하거나 수량을 업데이트하려면 먼저 구독을 재개해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 사용자의 구독에서 `cancel` 메서드를 호출하십시오.

```php
$user->subscription()->cancel();
```

구독이 취소되면 Cashier는 데이터베이스의 `ends_at` 컬럼을 자동으로 설정합니다. 이 컬럼은 `subscribed` 메서드가 언제부터 `false`를 반환해야 하는지 판단하는 데 사용됩니다. 예를 들어 고객이 3월 1일에 구독을 취소했지만, 해당 구독이 3월 5일까지 종료될 예정이 아니었다면 `subscribed` 메서드는 3월 5일까지 계속 `true`를 반환합니다. 일반적으로 사용자는 결제 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있기 때문입니다.

사용자가 구독을 취소했지만 아직 "유예 기간"에 있는지는 `onGracePeriod` 메서드를 사용하여 확인할 수 있습니다.

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

구독을 즉시 취소하려면 구독에서 `cancelNow` 메서드를 호출할 수 있습니다.

```php
$user->subscription()->cancelNow();
```

유예 기간에 있는 구독이 취소되지 않도록 중지하려면 `stopCancelation` 메서드를 호출할 수 있습니다.

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle의 구독은 취소 후 재개할 수 없습니다. 고객이 구독을 다시 시작하려면 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험 기간 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단을 미리 받는 경우

고객에게 체험 기간을 제공하면서도 결제 수단 정보를 미리 수집하고 싶다면, 고객이 구독하려는 가격에 대해 Paddle 대시보드에서 체험 기간을 설정해야 합니다. 그런 다음 일반적인 방식으로 결제 세션을 시작하십시오.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```
애플리케이션이 `subscription_created` 이벤트를 수신하면, Cashier는 애플리케이션 데이터베이스의 구독 레코드에 체험 기간 종료일을 설정하고, 이 날짜가 지난 뒤에 고객에게 청구를 시작하도록 Paddle에 지시합니다.

> [!WARNING]
> 고객의 구독이 체험 기간 종료일 전에 취소되지 않으면 체험 기간이 만료되는 즉시 요금이 청구됩니다. 따라서 사용자에게 체험 기간 종료일을 반드시 알려야 합니다.

사용자가 체험 기간 내에 있는지는 사용자 인스턴스의 `onTrial` 메서드를 사용하여 확인할 수 있습니다.

```php
if ($user->onTrial()) {
    // ...
}
```

기존 체험 기간이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

사용자가 특정 구독 유형의 체험 기간 중인지 확인하려면 `onTrial` 또는 `hasExpiredTrial` 메서드에 해당 유형을 전달하면 됩니다.

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 수단을 미리 받지 않기

사용자의 결제 수단 정보를 미리 수집하지 않고 체험 기간을 제공하려면, 사용자에 연결된 고객 레코드의 `trial_ends_at` 컬럼을 원하는 체험 종료일로 설정하면 됩니다. 일반적으로 이 작업은 사용자 등록 과정에서 수행합니다.

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->plus(days: 10)
]);
```

Cashier는 이러한 유형의 체험을 "generic trial"이라고 부릅니다. 기존 구독에 연결되어 있지 않기 때문입니다. 현재 날짜가 `trial_ends_at` 값보다 지나지 않았다면 `User` 인스턴스의 `onTrial` 메서드는 `true`를 반환합니다.

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

사용자를 위한 실제 구독을 생성할 준비가 되면, 평소처럼 `subscribe` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

사용자의 체험 종료일을 가져오려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 체험 중이면 Carbon 날짜 인스턴스를 반환하고, 체험 중이 아니면 `null`을 반환합니다. 기본 구독이 아닌 특정 구독의 체험 종료일을 가져오고 싶다면, 선택적으로 구독 유형 파라미터를 전달할 수도 있습니다.

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

사용자가 아직 실제 구독을 생성하지 않았고 "generic" 체험 기간 안에 있는지를 구체적으로 확인하고 싶다면 `onGenericTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험 기간 연장 또는 활성화

`extendTrial` 메서드를 호출하고 체험이 종료되어야 하는 시점을 지정하여 구독의 기존 체험 기간을 연장할 수 있습니다.

```php
$user->subscription()->extendTrial(now()->plus(days: 5));
```

또는 구독에서 `activate` 메서드를 호출하여 체험 기간을 종료하고 구독을 즉시 활성화할 수도 있습니다.

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle Webhook 처리 (Handling Paddle Webhooks)

Paddle은 webhook을 통해 애플리케이션에 다양한 이벤트를 알릴 수 있습니다. 기본적으로 Cashier 서비스 프로바이더는 Cashier의 webhook 컨트롤러를 가리키는 라우트를 등록합니다. 이 컨트롤러는 들어오는 모든 webhook 요청을 처리합니다.

기본적으로 이 컨트롤러는 실패한 결제가 너무 많은 구독의 취소, 구독 업데이트, 결제 수단 변경을 자동으로 처리합니다. 하지만 곧 살펴보겠지만, 이 컨트롤러를 확장하여 원하는 모든 Paddle webhook 이벤트를 처리할 수 있습니다.

애플리케이션이 Paddle webhook을 처리할 수 있도록 하려면 [Paddle control panel에서 webhook URL을 설정](https://vendors.paddle.com/notifications-v2)해야 합니다. 기본적으로 Cashier의 webhook 컨트롤러는 `/paddle/webhook` URL 경로에 응답합니다. Paddle control panel에서 활성화해야 하는 모든 webhook 목록은 다음과 같습니다.

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> 들어오는 요청은 Cashier에 포함된 [webhook 서명 검증](/docs/master/cashier-paddle#verifying-webhook-signatures) Middleware로 반드시 보호해야 합니다.

<a name="webhooks-csrf-protection"></a>
#### Webhook과 CSRF 보호

Paddle webhook은 Laravel의 [CSRF 보호](/docs/master/csrf)를 우회해야 하므로, Laravel이 들어오는 Paddle webhook에 대해 CSRF 토큰을 검증하려고 시도하지 않도록 해야 합니다. 이를 위해 애플리케이션의 `bootstrap/app.php` 파일에서 `paddle/*`를 CSRF 보호 대상에서 제외해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### Webhook과 로컬 개발

로컬 개발 중 Paddle이 애플리케이션에 webhook을 보낼 수 있게 하려면 [Ngrok](https://ngrok.com/) 또는 [Expose](https://expose.dev/docs/introduction) 같은 사이트 공유 서비스를 통해 애플리케이션을 외부에 노출해야 합니다. [Laravel Sail](/docs/master/sail)을 사용해 로컬에서 애플리케이션을 개발하고 있다면 Sail의 [사이트 공유 명령어](/docs/master/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### Webhook 이벤트 핸들러 정의

Cashier는 실패한 결제에 따른 구독 취소와 기타 일반적인 Paddle webhook을 자동으로 처리합니다. 하지만 추가로 처리하고 싶은 webhook 이벤트가 있다면, Cashier가 발생시키는 다음 이벤트를 리스닝하여 처리할 수 있습니다.

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle webhook의 전체 페이로드를 포함합니다. 예를 들어 `transaction.billed` webhook을 처리하고 싶다면, 해당 이벤트를 처리할 [listener](/docs/master/events#defining-listeners)를 등록할 수 있습니다.

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

Cashier는 수신한 webhook 유형에 특화된 이벤트도 발생시킵니다. 이 이벤트들은 Paddle의 전체 페이로드뿐만 아니라, webhook을 처리하는 데 사용된 관련 모델도 포함합니다. 예를 들면 billable 모델, 구독, 영수증 등이 포함됩니다.

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

애플리케이션의 `.env` 파일에 `CASHIER_WEBHOOK` 환경 변수를 정의하여 기본 내장 webhook 라우트를 재정의할 수도 있습니다. 이 값은 webhook 라우트의 전체 URL이어야 하며, Paddle control panel에 설정된 URL과 일치해야 합니다.

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### Webhook 서명 검증

Webhook을 안전하게 보호하려면 [Paddle의 webhook 서명](https://developer.paddle.com/webhooks/signature-verification)을 사용할 수 있습니다. 편의를 위해 Cashier는 들어오는 Paddle webhook 요청이 유효한지 검증하는 Middleware를 자동으로 포함합니다.

Webhook 검증을 활성화하려면 애플리케이션의 `.env` 파일에 `PADDLE_WEBHOOK_SECRET` 환경 변수가 정의되어 있는지 확인하세요. Webhook secret은 Paddle 계정 대시보드에서 가져올 수 있습니다.

<a name="single-charges"></a>
## 단일 결제 (Single Charges)

<a name="charging-for-products"></a>
### 제품 결제

고객의 제품 구매를 시작하려면 billable 모델 인스턴스에서 `checkout` 메서드를 사용하여 구매용 체크아웃 세션을 생성할 수 있습니다. `checkout` 메서드는 하나 또는 여러 개의 price ID를 받습니다. 필요한 경우 연관 배열을 사용하여 구매하는 제품의 수량을 제공할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

체크아웃 세션을 생성한 뒤에는 Cashier가 제공하는 `paddle-button` [Blade 컴포넌트](#overlay-checkout)를 사용하여 사용자가 Paddle 체크아웃 위젯을 보고 구매를 완료할 수 있게 할 수 있습니다.

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

체크아웃 세션에는 `customData` 메서드가 있으며, 이를 통해 기본 트랜잭션 생성 과정에 원하는 사용자 정의 데이터를 전달할 수 있습니다. 사용자 정의 데이터를 전달할 때 사용할 수 있는 옵션에 대해 더 알아보려면 [Paddle 문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하세요.

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 트랜잭션 환불

트랜잭션을 환불하면 구매 시 사용된 고객의 결제 수단으로 환불 금액이 반환됩니다. Paddle 구매를 환불해야 한다면 `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 환불 사유를 받고, 환불할 하나 이상의 price ID를 선택적 금액과 함께 연관 배열로 받습니다. 특정 billable 모델의 트랜잭션은 `transactions` 메서드를 사용하여 가져올 수 있습니다.

예를 들어 `pri_123`과 `pri_456` 가격에 대해 특정 트랜잭션을 환불한다고 가정해 보겠습니다. `pri_123`은 전액 환불하고, `pri_456`은 2달러만 환불하려고 합니다.

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // Fully refund this price...
    'pri_456' => 200, // Only partially refund this price...
]);
```

위 예시는 트랜잭션의 특정 항목을 환불합니다. 전체 트랜잭션을 환불하려면 사유만 제공하면 됩니다.

```php
$response = $transaction->refund('Accidental charge');
```

환불에 대한 자세한 내용은 [Paddle의 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 환불은 완전히 처리되기 전에 항상 Paddle의 승인을 받아야 합니다.

<a name="crediting-transactions"></a>
### 트랜잭션 크레딧 지급

환불과 마찬가지로 트랜잭션에 크레딧을 지급할 수도 있습니다. 트랜잭션에 크레딧을 지급하면 해당 금액이 고객의 잔액에 추가되어 이후 구매에 사용할 수 있습니다. Paddle이 구독 크레딧을 자동으로 처리하므로, 트랜잭션 크레딧 지급은 수동 수금 트랜잭션에만 가능하며 구독처럼 자동 수금되는 트랜잭션에는 사용할 수 없습니다.

```php
$transaction = $user->transactions()->first();

// Credit a specific line item fully...
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [크레딧 지급에 대한 Paddle 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 크레딧은 수동 수금 트랜잭션에만 적용할 수 있습니다. 자동 수금 트랜잭션의 크레딧은 Paddle이 직접 처리합니다.

<a name="transactions"></a>
## 트랜잭션 (Transactions)

`transactions` 속성을 통해 billable 모델의 트랜잭션 배열을 쉽게 가져올 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

트랜잭션은 제품 및 구매에 대한 결제를 나타내며, 송장이 함께 제공됩니다. 완료된 트랜잭션만 애플리케이션 데이터베이스에 저장됩니다.

고객의 트랜잭션을 나열할 때는 트랜잭션 인스턴스의 메서드를 사용하여 관련 결제 정보를 표시할 수 있습니다. 예를 들어 사용자가 각 송장을 쉽게 다운로드할 수 있도록 모든 트랜잭션을 테이블에 나열할 수 있습니다.

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

`download-invoice` 라우트는 다음과 같을 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 지난 결제와 예정된 결제

반복 구독에 대한 고객의 지난 결제 또는 예정된 결제를 가져오고 표시하려면 `lastPayment` 및 `nextPayment` 메서드를 사용할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 하지만 `lastPayment`는 아직 트랜잭션이 webhook으로 동기화되지 않은 경우 `null`을 반환하고, `nextPayment`는 구독이 취소된 경우처럼 청구 주기가 종료된 경우 `null`을 반환합니다.

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트 (Testing)

테스트할 때는 통합이 예상대로 작동하는지 확인하기 위해 결제 흐름을 수동으로 테스트해야 합니다.

CI 환경에서 실행되는 테스트를 포함한 자동화 테스트에서는 Paddle에 대한 HTTP 호출을 가짜로 처리하기 위해 [Laravel의 HTTP Client](/docs/master/http-client#testing)를 사용할 수 있습니다. 이 방법은 Paddle의 실제 응답을 테스트하지는 않지만, 실제로 Paddle API를 호출하지 않고 애플리케이션을 테스트할 수 있는 방법을 제공합니다.
