# 라라벨 Cashier (Paddle) (Laravel Cashier (Paddle))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [구성](#configuration)
    - [청구 모델(Billable Model)](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매하기](#quickstart-selling-products)
    - [구독 판매하기](#quickstart-selling-subscriptions)
- [결제 세션](#checkout-sessions)
    - [오버레이 체크아웃](#overlay-checkout)
    - [인라인 체크아웃](#inline-checkout)
    - [비회원 체크아웃](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객 대상 가격 미리보기](#customer-price-previews)
    - [할인 적용](#price-discounts)
- [고객](#customers)
    - [고객 기본값 설정](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 결제](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량 관리](#subscription-quantity)
    - [여러 상품이 포함된 구독](#subscriptions-with-multiple-products)
    - [여러 개의 구독](#multiple-subscriptions)
    - [구독 일시 정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험(트라이얼)](#subscription-trials)
    - [결제 수단 선결제 방식](#with-payment-method-up-front)
    - [결제 수단 비선결제 방식](#without-payment-method-up-front)
    - [체험 기간 연장 또는 즉시 활성화](#extend-or-activate-a-trial)
- [Paddle Webhook 처리](#handling-paddle-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [상품 결제 처리](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 크레딧 지급](#crediting-transactions)
- [거래 내역](#transactions)
    - [과거 및 예정 결제 내역](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 이 문서는 Cashier Paddle 2.x의 Paddle Billing 통합 문서입니다. 여전히 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 참고하시기 바랍니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스에 대한 직관적이고 유연한 인터페이스를 제공합니다. 반복적이고 복잡한 구독 결제 관련 코드들을 Cashier가 대신 처리해줍니다. 기본적인 구독 관리 외에도 Cashier로는 구독 플랜 변경, 구독 "수량", 구독 일시정지, 취소 유예 기간 등 다양한 기능을 손쉽게 구현할 수 있습니다.

Cashier Paddle을 깊이 있게 사용하기 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 꼭 확인하시기 바랍니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새로운 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 검토하시기 바랍니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 관리자를 사용해 Paddle용 Cashier 패키지를 설치하세요.

```shell
composer require laravel/cashier-paddle
```

다음으로, `vendor:publish` Artisan 명령어를 사용하여 Cashier 마이그레이션 파일을 게시해야 합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이제 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. Cashier 마이그레이션은 `customers` 테이블을 새로 생성합니다. 또한, 모든 고객의 구독 정보를 저장하는 `subscriptions`와 `subscription_items` 테이블, 그리고 고객과 연동된 모든 Paddle 거래 내역을 저장하는 `transactions` 테이블도 생성됩니다.

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 제대로 처리할 수 있도록 반드시 [Cashier의 webhook 처리를 설정](#handling-paddle-webhooks)해야 합니다.

<a name="paddle-sandbox"></a>
### Paddle Sandbox

로컬 및 스테이징 개발 환경에서는 [Paddle Sandbox 계정](https://sandbox-login.paddle.com/signup)을 등록해 사용하는 것이 좋습니다. Sandbox 계정은 실제 결제 없이 애플리케이션 개발과 테스트를 안전하게 수행할 수 있도록 도와줍니다. 다양한 결제 상황을 시뮬레이션하려면 Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 사용하세요.

Sandbox를 사용할 때는 `.env` 파일의 `PADDLE_SANDBOX` 환경 변수 값을 `true`로 설정하세요.

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발이 완료되면 [Paddle 벤더 계정](https://paddle.com)을 신청할 수 있습니다. 프로덕션 배포 전에는 Paddle의 승인을 받아야 하며, Paddle이 애플리케이션의 도메인을 승인해야 실제로 서비스할 수 있습니다.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="billable-model"></a>
### 청구 모델(Billable Model)

Cashier를 사용하려면 먼저 사용자 모델(보통 User 모델)에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 수단 정보 갱신 등 일반적인 결제 작업을 위한 다양한 메서드를 제공합니다.

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 다른 청구 가능한 엔티티(예: 팀 등)가 있다면 해당 모델에도 동일하게 트레이트를 추가할 수 있습니다.

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

다음으로, Paddle API 키를 애플리케이션의 `.env` 파일에 설정하세요. Paddle API 키는 Paddle 컨트롤 패널에서 확인할 수 있습니다.

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

- `PADDLE_SANDBOX`는 [Paddle Sandbox 환경](#paddle-sandbox) 사용 시 `true`로, 프로덕션(실 서비스) 환경에서는 `false`로 설정해야 합니다.
- `PADDLE_RETAIN_KEY`는 선택 사항이며, Paddle [Retain](https://developer.paddle.com/concepts/retain/overview) 기능을 사용할 때만 필요합니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle의 결제 위젯 작동을 위해 Paddle 전용 JavaScript 라이브러리가 필요합니다. 해당 JS 라이브러리는 애플리케이션 레이아웃의 `</head>` 태그 바로 앞에 `@paddleJS` Blade 디렉티브를 추가하여 불러올 수 있습니다.

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

송장 등에 노출되는 금액의 통화/로케일 포맷을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 이용해 통화 로케일을 설정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en`(영어) 외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 기능이 설치 및 설정되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Cashier가 내부적으로 사용하는 모델을 직접 상속하여 확장할 수도 있습니다. 예를 들어, 새 모델을 정의하고 Cashier의 기본 모델을 상속합니다.

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 뒤, Cashier에 사용하려는 커스텀 모델을 `Laravel\Paddle\Cashier` 클래스를 통해 등록하세요. 일반적으로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 커스텀 모델 사용을 지정합니다.

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
### 상품 판매하기 (Selling Products)

> [!NOTE]
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격으로 제품을 정의해야 하며, [Paddle webhook 처리](#handling-paddle-webhooks)도 반드시 구성해야 합니다.

애플리케이션에서 상품 및 구독 결제 기능을 구현하는 작업은 어렵게 느껴질 수 있지만, Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 기능을 사용하면 쉽고 강력하게 결제통합이 가능합니다.

1회성 단일 결제 상품을 고객에게 판매하려면, Cashier를 이용해 Paddle Checkout Overlay로 결제 과정을 진행시키는 방식으로 구현할 수 있습니다. 결제가 완료되면, 고객은 지정한 성공 URL로 리다이렉트됩니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예시에서 보이듯이, Cashier에서 제공하는 `checkout` 메서드를 통해 지정된 "가격 식별자"로 Paddle Checkout Overlay용 객체를 생성합니다. Paddle에서 '가격(Price)'이란 [특정 상품에 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요하다면, `checkout` 메서드는 자동으로 Paddle 내에 고객을 생성하고, 애플리케이션의 사용자 DB와 연동해 연결됩니다. 결제 과정을 마치면 고객은 지정한 성공 페이지로 이동하며, 이곳에서 안내 메시지를 띄울 수 있습니다.

`buy` 뷰에서는, Checkout Overlay를 띄울 수 있는 버튼을 포함하면 됩니다. Cashier에는 `paddle-button` Blade 컴포넌트가 함께 제공되며, 직접 [오버레이 체크아웃을 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타데이터 제공하기

상품 판매 시, 애플리케이션 자체의 `Cart`나 `Order` 모델을 통해 주문 및 구매내역을 관리하는 경우가 많습니다. Paddle Checkout Overlay로 리다이렉트할 때, 기존 주문 ID 등을 함께 전달하면, 결제 완료 후 고객이 다시 돌아왔을 때 해당 구입 기록을 연동할 수 있습니다.

이를 위해, `checkout` 메서드에 메타데이터 배열을 전달하는 방식으로 구현할 수 있습니다. 예를 들어, 사용자가 구매 프로세스를 시작할 때 임시 `Order`를 생성하고, 해당 정보를 Checkout에 넘깁니다. 아래 예시의 `Cart`와 `Order` 모델은 Cashier에서 직접 제공하지 않으며, 애플리케이션 요구사항에 맞게 자유롭게 구현할 수 있습니다.

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

위와 같이, 사용자가 체크아웃을 시작할 때 해당 장바구니/주문에 포함된 Paddle 가격 식별자를 모두 `checkout`에 전달하고, 주문 ID를 `customData`로 넘깁니다. 결제 완료 후, Paddle에서 발생시키는 Webhook을 Cashier 이벤트로 받아 주문 상태를 'complete'로 변경하면 됩니다.

이를 위해, Cashier에서 제공하는 `TransactionCompleted` 이벤트를 리스닝하도록 하면 됩니다. 일반적으로는 `AppServiceProvider`의 `boot` 메서드에서 이벤트 리스너를 등록합니다.

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

리스너(`CompleteOrder`) 예시는 아래와 같습니다.

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

Paddle에서 발생하는 [`transaction.completed` 이벤트의 데이터](https://developer.paddle.com/webhooks/transactions/transaction-completed) 구조에 대해서는 공식 문서를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매하기 (Selling Subscriptions)

> [!NOTE]
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격으로 상품을 정의해야 하며, [Paddle webhook 처리](#handling-paddle-webhooks)도 반드시 구성해야 합니다.

애플리케이션에서 상품 또는 구독 결제 기능을 구현하는 것은 어렵게 느껴질 수 있지만, Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 기능을 통해 현대적이고 강력한 결제 시스템을 손쉽게 구축할 수 있습니다.

구독 판매 예시로, 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 요금제를 가진 "Basic" 상품(`pro_basic`)과 "Expert" 플랜(`pro_expert`)이 있다고 가정하겠습니다.

먼저, 고객이 서비스를 어떻게 구독할 수 있는지 살펴보겠습니다. 예를 들어, 요금제 페이지에서 '구독하기' 버튼 클릭 시 Paddle Checkout Overlay 를 띄웁니다.

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 Checkout Overlay를 띄울 수 있는 버튼을 추가합니다. `paddle-button` Blade 컴포넌트를 사용할 수 있으며, [오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)하는 것도 가능합니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 'Subscribe' 버튼을 클릭하면 고객은 결제 정보를 입력하고 구독을 시작할 수 있습니다. 일부 결제 수단은 약간의 처리 시간이 필요할 수 있으므로, [Cashier의 webhook 처리를 구성](#handling-paddle-webhooks)해야 구독 상태 동기화가 가능합니다.

구독이 시작되었다면, 애플리케이션에서 구독한 사용자만 특정 서비스에 접근할 수 있도록 제한할 필요가 있습니다. Cashier의 `Billable` 트레이트에서 제공하는 `subscribed` 메서드로 사용자의 구독 상태를 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

또한, 특정 상품이나 가격에 대한 구독 유무도 쉽게 확인할 수 있습니다.

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 전용 미들웨어 만들기

요금 결제 여부에 따라 라우트 접근을 제어하는 [미들웨어](/docs/master/middleware)를 제작할 수 있습니다. 이렇게 하면 미들웨어로 구독하지 않은 사용자가 해당 라우트에 접근하지 못하도록 쉽게 제어할 수 있습니다.

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
            // 사용자에게 결제 안내 페이지로 리다이렉트...
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

미들웨어 정의 후에는 해당 라우트에 적용하면 됩니다.

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객의 요금제 관리 허용하기

고객이 구독 플랜을 다른 상품이나 요금제로 변경하는 기능도 필요합니다. 예를 들어, 월간 구독에서 연간 구독으로 변경하려면 아래와 같이 버튼을 만들어 해당 라우트로 연결하면 됩니다.

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 이 예시에서 "$price"는 "price_basic_yearly" 등

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

플랜 변경은 물론이고, 구독을 취소할 수 있는 기능도 제공합니다. 아래와 같이 취소 버튼을 구현하여 해당 라우트로 연결할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이렇게 하면, 구독은 다음 결제 주기 말에 취소됩니다.

> [!NOTE]
> Cashier의 webhook 처리를 설정했다면, Cashier는 Paddle에서 수신하는 webhook을 분석해서 Cashier 관련 데이터베이스 테이블을 자동으로 동기화합니다. 예를 들어, Paddle 대시보드에서 구독을 취소하면 Cashier도 웹훅을 수신해 데이터베이스의 구독 상태를 'canceled'로 변경합니다.

<a name="checkout-sessions"></a>
## 결제 세션 (Checkout Sessions)

고객을 청구하는 대부분의 연산은 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 통한 "체크아웃 세션" 방식으로 수행합니다.

결제 전, Paddle의 체크아웃 설정 대시보드에서 [애플리케이션의 기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 반드시 설정해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 체크아웃 (Overlay Checkout)

Checkout Overlay 위젯을 실행하기 전에, Cashier를 이용해 체크아웃 세션을 생성해야 합니다. 이러한 세션은 결제 위젯에 어떤 결제 작업을 수행할지 알려줍니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier는 `paddle-button` [Blade 컴포넌트](/docs/master/blade#components)를 제공합니다. 체크아웃 세션을 이 컴포넌트의 prop으로 전달하면, 버튼 클릭 시 Paddle의 결제 위젯이 표시됩니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이렇게 하면 기본 디자인의 위젯이 표시되며, 제공되는 Paddle 지원 속성([Paddle HTML data attributes](https://developer.paddle.com/paddlejs/html-data-attributes))을 활용해 위젯을 꾸밀 수 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기적으로 동작합니다. 사용자가 위젯에서 구독 생성 후, Paddle이 웹훅으로 애플리케이션에 알림을 보내고, 그에 따라 데이터베이스의 구독 상태를 갱신해야 하므로 [웹훅 설정](#handling-paddle-webhooks)이 매우 중요합니다.

> [!WARNING]
> 구독 상태 변경 후 웹훅 수신까지는 보통 짧지만, 결제 직후에 사용자의 구독이 곧바로 활성화되지 않을 수 있으므로 앱에서 이 점을 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃 수동 렌더링

Blade 컴포넌트를 사용하지 않고 오버레이 체크아웃을 수동으로 렌더링할 수도 있습니다. 먼저, [이전 예시](#overlay-checkout)처럼 체크아웃 세션을 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그런 다음 Paddle.js를 직접 사용해 결제 위젯을 초기화할 수 있습니다. 아래 예시는 `paddle_button` 클래스를 가진 링크를 구성하고, Paddle.js가 이 클래스를 감지해 클릭 시 오버레이 위젯을 표시하는 방식입니다.

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
### 인라인 체크아웃 (Inline Checkout)

오버레이 스타일 위젯이 아닌, Paddle에서 제공하는 '인라인' 형태의 체크아웃 위젯을 사용할 수도 있습니다. 인라인 방식은 HTML 필드를 수정할 수는 없지만, 해당 위젯을 애플리케이션 내에 직접 임베드할 수 있습니다.

Cashier는 인라인 체크아웃을 쉽게 시작할 수 있도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. [오버레이 예시](#overlay-checkout)와 마찬가지로 체크아웃 세션을 생성한 후, 컴포넌트에 전달하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

컴포넌트 사용 예시:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 체크아웃 컴포넌트의 높이는 `height` 속성으로 조절할 수 있습니다.

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

더 다양한 인라인 체크아웃 옵션 및 커스터마이징 방법은 [Paddle의 인라인 체크아웃 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [관련 문서](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 수동 렌더링

Blade 컴포넌트를 사용하지 않고도 인라인 체크아웃을 직접 구현할 수 있습니다. 체크아웃 세션 생성은 [앞선 예제](#inline-checkout)와 동일합니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

이제 Paddle.js를 사용해 인라인 체크아웃을 직접 초기화합니다. 아래는 [Alpine.js](https://github.com/alpinejs/alpine)를 활용한 예시이며, 프론트엔드 스택에 맞게 얼마든지 수정 가능합니다.

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
### 비회원 체크아웃 (Guest Checkouts)

애플리케이션에 회원가입이 반드시 필요하지 않은 경우, 비회원도 체크아웃 세션을 생성할 수 있습니다. 이때는 `guest` 메서드를 사용하세요.

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

체크아웃 세션을 Paddle 버튼 또는 인라인 컴포넌트에 동일하게 전달할 수 있습니다.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle은 통화 단위별로 서로 다른 가격을 지정할 수 있습니다. Cashier는 `previewPrices` 메서드로 원하는 가격 ID의 다양한 통화 가격 정보를 조회할 수 있습니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

기본적으로 요청자의 IP를 기준으로 통화와 지역이 자동 판단되며, 필요시 특정 국가 정보를 직접 전달할 수 있습니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

조회된 가격 정보는 원하는 방식으로 화면에 표시 가능하며,

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

합계와 세금 금액을 별도로 표시할 수도 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

자세한 내용은 [Paddle의 가격 미리보기 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하십시오.

<a name="customer-price-previews"></a>
### 고객 대상 가격 미리보기 (Customer Price Previews)

이미 고객이 된 사용자라면, 해당 고객에게 적용되는 각 가격 정보를 바로 조회할 수 있습니다.

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

Cashier는 내부적으로 사용자의 Paddle 고객 ID를 이용해 해당 통화로 가격을 조회합니다. 미국 사용자라면 달러($), 벨기에 사용자라면 유로(€)와 같이 표기됩니다. 매칭되는 통화가 없을 경우, 상품의 기본 통화가 사용됩니다. 상품이나 구독 요금제별 모든 가격은 Paddle 대시보드에서 자유롭게 조정할 수 있습니다.

<a name="price-discounts"></a>
### 할인 적용 (Discounts)

할인된 가격을 조회하고 싶다면, `previewPrices` 호출 시 `discount_id` 옵션을 전달하세요.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 할인 가격은 동일하게 출력하면 됩니다.

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
### 고객 기본값 설정 (Customer Defaults)

Cashier에서는 체크아웃 세션 생성 시, 고객의 이메일과 이름 등 기본 정보를 미리 채워넣도록 설정할 수 있습니다. 이를 위해 청구 모델에 아래 메서드를 오버라이드 하면 됩니다.

```php
/**
 * Paddle에 연동될 고객 이름 반환
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Paddle에 연동될 고객 이메일 반환
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

이 설정은 [체크아웃 세션](#checkout-sessions) 생성에 관련된 모든 Cashier 액션에서 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회 (Retrieving Customers)

Paddle 고객 ID로 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용할 수 있습니다. 이 메서드는 청구 모델 인스턴스를 반환합니다.

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

가끔은 구독을 시작하지 않아도 Paddle 고객만 먼저 생성해야 할 때가 있습니다. 이럴 때는 `createAsCustomer` 메서드를 사용하세요.

```php
$customer = $user->createAsCustomer();
```

결과로 `Laravel\Paddle\Customer` 인스턴스가 반환됩니다. 고객 생성 후 언제든 구독을 추가할 수 있습니다. `$options` 배열을 전달하여, [Paddle API가 지원하는 고객 생성 파라미터](https://developer.paddle.com/api-reference/customers/create-customer)도 함께 넘길 수 있습니다.

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독을 생성하려면 먼저 데이터베이스에서 청구 모델 인스턴스를 조회해야 합니다. 보통은 `App\Models\User` 인스턴스가 됩니다. 모델 인스턴스가 준비되었다면, `subscribe` 메서드로 구독용 체크아웃 세션을 생성할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe`의 첫 번째 인수는 구독할 가격의 식별자이며, Paddle에서 지정한 ID와 일치해야 합니다. `returnTo` 메서드는 결제 완료 후 사용자가 이동할 URL을 지정합니다. 두 번째 인수는 애플리케이션 내부에서 사용하는 구독 구분용 "type"으로, 하나의 구독만 제공하는 경우 `default` 또는 `primary`로 지정하면 됩니다. 이 타입은 사용자에게 노출되는 값이 아니며, 한 번 생성 후 변경해서는 안 됩니다.

구독과 관련된 메타데이터를 `customData` 메서드로 전달할 수도 있습니다.

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

체크아웃 세션 생성이 끝났다면, Paddle 대시보드에 포함된 `paddle-button` [Blade 컴포넌트](#overlay-checkout)로 전달할 수 있습니다.

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

구독 완료 시, Paddle이 `subscription_created` 웹훅을 보내고, Cashier가 이 웹훅을 수신해 고객의 구독 정보를 설정합니다. [웹훅 처리가 제대로 이루어지는지](#handling-paddle-webhooks) 반드시 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

사용자가 애플리케이션에서 구독 중인지 다양한 방법으로 간편하게 체크할 수 있습니다. 예를 들어, 대표 구독이 존재하면 `subscribed` 메서드가 구독 유무를 반환합니다(트라이얼 기간이어도 true 반환).

```php
if ($user->subscribed()) {
    // ...
}
```

여러 개의 구독이 있을 때는 인자로 구독 type을 넘길 수 있습니다.

```php
if ($user->subscribed('default')) {
    // ...
}
```

이 `subscribed` 메서드는 [라우트 미들웨어](/docs/master/middleware)로 사용해, 구독 유무에 따라 특정 경로와 컨트롤러 접근을 제어할 때 적합합니다.

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
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed()) {
            // 유료회원이 아닐 경우...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

트라이얼(체험) 기간인지 확인할 때는 `onTrial` 메서드를 활용합니다.

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 Paddle 가격 ID로 구독 중인지 확인하고 싶을 땐, `subscribedToPrice` 메서드를 사용할 수 있습니다. 예를 들어, 현재 사용자가 `default` 구독에서 월간 구독 플랜을 사용 중인지 확인합니다.

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

트라이얼 기간이 끝났거나, 다시 반복 결제주기에 들어갔는지 알기 위해서는 `recurring` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 구독 취소 상태

이전에 구독자였으나 지금은 취소한 사용자인지 확인하려면 `canceled` 메서드를 사용하세요.

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

취소했지만 아직 "유예 기간"(grace period)이 남아 있는지도 체크할 수 있습니다. 예를 들어, 3월 5일에 취소하여 3월 10일까지 유지되는 경우, 3월 10일까지는 여전히 `subscribed`가 true입니다.

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체(past due) 상태

결제 실패 시, 구독은 `past_due` 상태로 마킹됩니다. 이 상황에서는 결제가 완료되기 전까지 구독이 활성화되지 않으니, `pastDue` 메서드로 상태를 점검하세요.

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

이 경우 고객에게 [결제 정보 업데이트](#updating-payment-information)를 안내해야 합니다.

연체 상태에서도 구독을 유효하다고 처리하려면 Cashier의 `keepPastDueSubscriptionsActive` 메서드를 사용하면 됩니다. 일반적으로 `AppServiceProvider`의 `register`에서 호출합니다.

```php
use Laravel\Paddle\Cashier;

public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!WARNING]
> `past_due` 상태에서는 구독 변경(swap) 및 수량 변경(updateQuantity)이 불가능합니다. 해당 상태에서는 두 메서드 모두 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 쿼리 스코프

거의 모든 구독 상태는 쿼리 스코프로도 제공되어 원하는 조건의 구독만 쉽게 조회할 수 있습니다.

```php
// 모든 유효한 구독 조회
$subscriptions = Subscription::query()->valid()->get();

// 사용자의 취소된 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

지원되는 전체 쿼리 스코프는 아래와 같습니다.

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
### 구독 단일 결제 (Subscription Single Charges)

기존 구독에 추가로 1회성 요금제를 청구할 수 있습니다. `charge` 메서드에 가격 ID(들)를 전달하면 됩니다.

```php
// 단일 가격을 청구
$response = $user->subscription()->charge('pri_123');

// 여러 가격을 한 번에 청구
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

이렇게 청구한 금액은 실제로는 다음 결제 주기에 합산되어 청구됩니다. 즉시 청구해야 한다면 `chargeAndInvoice` 메서드를 사용하세요.

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독별 결제 수단을 관리합니다. 기본 결제수단을 변경하려면, 구독 모델의 `redirectToUpdatePaymentMethod`로 Paddle이 제공하는 결제 정보 변경 페이지로 리다이렉트할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

사용자가 결제 수단 정보를 변경 완료하면 Paddle에서 `subscription_updated` 웹훅을 보내고, 애플리케이션 DB의 구독 정보가 갱신됩니다.

<a name="changing-plans"></a>
### 플랜 변경 (Changing Plans)

구독 중에 다른 요금제로 변경하고자 할 때, 변경하려는 가격 식별자를 `swap` 메서드에 전달하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 인보이스 처리(즉시 결제)를 원할 경우에는 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 잔여 기간 정산(Prorations)

Paddle은 기본적으로 요금제 교체 시 잔여 기간 정산(프로레이션)을 적용합니다. 정산 없이 단순 변경만 하고 싶다면 `noProrate` 메서드를 사용하세요.

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

정산 없이 즉시 인보이스(즉시 결제)를 처리하려면 `swapAndInvoice`와 `noProrate`를 조합하면 됩니다.

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

변경에 대해 고객에게 추가 요금을 부과하지 않으려면 `doNotBill` 메서드를 활용하세요.

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

관련 정책은 [Paddle의 프로레이션 가이드](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량 관리 (Subscription Quantity)

일부 구독은 '수량'에 따라 요금이 달라집니다. 예를 들어, 프로젝트당 월 $10의 SaaS처럼 수량을 쉽게 증감하려면 아래와 같이 `incrementQuantity`, `decrementQuantity` 메서드를 활용하세요.

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 현재 수량에 5개 추가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 현재 수량에서 5개 감소
$user->subscription()->decrementQuantity(5);
```

정확한 수량을 명시적으로 지정하려면 `updateQuantity`를 사용하세요.

```php
$user->subscription()->updateQuantity(10);
```

수량 변경 시에도 정산을 원치 않는다면 `noProrate`와 함께 사용하면 됩니다.

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 상품이 포함된 구독의 수량

[여러 상품이 포함된 구독](#subscriptions-with-multiple-products)의 경우, 수량을 변경하려는 가격 식별자를 두 번째 인자로 명시해야 합니다.

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 상품이 포함된 구독 (Subscriptions With Multiple Products)

[여러 상품이 포함된 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons) 기능을 활용하면, 하나의 구독에 여러 요금제를 묶을 수 있습니다. 예를 들어, 기본 구독에는 월 $10, 실시간 채팅 애드온은 월 $15의 추가 요금 식으로 여러 상품을 조합할 수 있습니다.

구독 체크아웃 세션 생성 시, 가격들의 배열을 첫 번째 인자로 넘기면 됩니다.

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

위 예시에서는 고객의 `default` 구독에 두 가격이 모두 포함됩니다. 각 가격별로 수량을 지정하려면 연관 배열로 넘기면 됩니다.

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 가격을 추가하려면 `swap` 메서드를 사용해야 하며, 현재 요금제 정보도 함께 전달해야 합니다.

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

이때는 다음 결제 주기부터 청구됩니다. 즉시 인보이스(즉시 청구)를 원할 경우 `swapAndInvoice`를 사용하세요.

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

특정 가격을 구독에서 제거하고자 한다면, 해당 가격을 배열에서 빼고 `swap` 하세요.

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독에서 마지막 가격을 제거할 수는 없습니다. 이 경우 단순히 구독을 취소하세요.

<a name="multiple-subscriptions"></a>
### 여러 개의 구독 (Multiple Subscriptions)

Paddle은 한 명의 고객이 여러 개의 구독을 동시에 가질 수 있습니다. 예를 들어, 수영 구독과 웨이트 구독을 별개의 플랜으로 분리하는 것이 가능합니다.

구독 생성 시, `subscribe`의 두 번째 인자로 구독 'type'을 지정하면 됩니다. 이 값은 자유롭게 정하면 됩니다.

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

일정 후 연간 구독으로 플랜 변경도 가능합니다. 이 경우 해당 구독 타입에 대해 swap 호출만 하면 됩니다.

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

구독 전체 취소도 아래처럼 할 수 있습니다.

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시 정지 (Pausing Subscriptions)

구독을 일시 정지하려면 구독 인스턴스의 `pause` 메서드를 호출합니다.

```php
$user->subscription()->pause();
```

구독 일시정지 시 Cashier가 자동으로 DB의 `paused_at` 컬럼을 설정합니다. 이 컬럼은 결제 주기 마지막에 `paused` 메서드가 true를 반환하도록 기준이 됩니다. 기본값은 다음 결제 주기에 정지되어, 사용자는 남은 결제 기간 동안 서비스를 계속 이용할 수 있습니다.

즉시 일시정지를 원한다면 `pauseNow`를 사용하세요.

```php
$user->subscription()->pauseNow();
```

특정 시점까지 정지하려면 `pauseUntil`을, 즉시 특정 시점까지 정지하려면 `pauseNowUntil`을 사용하세요.

```php
$user->subscription()->pauseUntil(now()->plus(months: 1));
$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```

"유예 기간" 중에 정지 상태인지 확인하려면 `onPausedGracePeriod` 메서드를 이용하세요.

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

일시정지한 구독을 재개하려면 `resume` 메서드를 실행하면 됩니다.

```php
$user->subscription()->resume();
```

> [!WARNING]
> 일시정지된 상태에서는 구독을 수정할 수 없습니다. 플랜 변경이나 수량 업데이트 등은 반드시 먼저 재개(resume)한 후에 시도해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소 (Canceling Subscriptions)

구독 취소는 구독 인스턴스의 `cancel` 메서드를 호출하면 됩니다.

```php
$user->subscription()->cancel();
```

구독 취소 시 Cashier는 자동으로 `ends_at` 컬럼을 기록하여, 결제 주기가 끝나면 `subscribed` 메서드가 false를 반환하도록 합니다. 예를 들어, 3월 1일에 취소 처리가 일어나고 3월 5일까지 이용이 가능하도록 유예기간을 둡니다.

유예기간 동안인지 확인하려면 `onGracePeriod`를 사용하면 됩니다.

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 구독을 종료하고 싶다면 `cancelNow`를 호출하세요.

```php
$user->subscription()->cancelNow();
```

취소 유예 중인 구독을 취소되지 않도록 막으려면 `stopCancelation` 메서드를 사용할 수 있습니다.

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle의 구독은 취소 후 재개가 불가능합니다. 고객이 다시 사용하려면 새 구독을 만들어야 합니다.

<a name="subscription-trials"></a>
## 구독 체험(트라이얼) (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단 선결제 방식 (With Payment Method Up Front)

결제 수단 정보를 미리 받아둔 상태로 체험 기간을 운영하고자 한다면, Paddle 대시보드에서 해당 가격에 트라이얼 기간을 지정하고, 평소처럼 체크아웃 세션을 시작하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscription_created` 이벤트 수신 시 Cashier가 구독 레코드에 트라이얼 종료일을 기록하고, 해당 시점까지는 결제가 이뤄지지 않도록 Paddle에 지시합니다.

> [!WARNING]
> 고객이 트라이얼 종료일 전까지 구독을 취소하지 않으면, 트라이얼이 만료되는 즉시 결제가 발생하니 사용자에게 충분히 안내하세요.

트라이얼 기간 중인지 체크하려면, 유저 인스턴스의 `onTrial` 메서드를 사용하면 됩니다.

```php
if ($user->onTrial()) {
    // ...
}
```

트라이얼이 만료됐는지 확인하고 싶으면 `hasExpiredTrial` 메서드를 사용하세요.

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

특정 구독 타입에 대한 트라이얼 확인도 가능합니다.

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 수단 비선결제 방식 (Without Payment Method Up Front)

결제 정보를 먼저 받지 않고 트라이얼을 운용하고 싶으면 유저와 연동된 customer 레코드의 `trial_ends_at` 칼럼에 트라이얼 종료일을 설정하면 됩니다. 주로 회원 가입 시 이런 방식이 사용됩니다.

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->plus(days: 10)
]);
```

이 트라이얼은 "제네릭(일반)" 체험판으로 관리되며, 해당 사용자가 트라이얼 중인지 확인할 때는 아래처럼 할 수 있습니다.

```php
if ($user->onTrial()) {
    // ...
}
```

정식 구독으로 전환할 때는 평소처럼 `subscribe`를 호출하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

트라이얼 종료일을 가져오려면 `trialEndsAt` 메서드를 사용하세요. 구독 타입도 옵션으로 지정할 수 있습니다.

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

아직 구독하지 않은 순수한 "제네릭 트라이얼" 기간인지 알고 싶을 때는 `onGenericTrial` 메서드를 활용하세요.

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험 기간 연장 또는 즉시 활성화 (Extend or Activate a Trial)

기존 트라이얼을 연장하려면 `extendTrial` 메서드를 사용하고, 특정 시점을 인자로 넘기세요.

```php
$user->subscription()->extendTrial(now()->plus(days: 5));
```

즉시 구독을 활성화하려면 `activate` 메서드를 호출하면 됩니다.

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle Webhook 처리 (Handling Paddle Webhooks)

Paddle은 다양한 이벤트를 웹훅으로 애플리케이션에 알릴 수 있습니다. Cashier 서비스 프로바이더가 자동으로 웹훅 컨트롤러 경로를 등록하고, 이 컨트롤러가 웹훅 요청을 처리합니다.

이 기본 컨트롤러는 반복 청구 실패로 인한 자동 구독 취소, 구독 및 결제 정보 갱신 등 Paddle의 주요 이벤트를 자동으로 처리합니다. 추가적으로 커스텀 이벤트 처리가 필요하다면 해당 컨트롤러를 확장하거나, 이벤트 리스너를 활용할 수 있습니다.

Paddle 웹훅 처리하려면, [Paddle 컨트롤 패널의 webhook URL을 설정](https://vendors.paddle.com/notifications-v2)해야 합니다. 기본적으로 Cashier의 웹훅 컨트롤러는 `/paddle/webhook` 경로를 사용합니다. Paddle 컨트롤 패널에서 아래 웹훅들을 활성화해야 합니다.

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> Cashier에 포함된 [웹훅 서명 검증 미들웨어](/docs/master/cashier-paddle#verifying-webhook-signatures)로 보안을 강화하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Paddle 웹훅은 Laravel의 [CSRF 보호](/docs/master/csrf)를 우회해야 합니다. 이를 위해 `bootstrap/app.php`에서 `paddle/*` 경로를 CSRF 보호 예외 처리에 추가하세요.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 로컬 개발 중 웹훅 수신

로컬 개발 환경에서 Paddle 웹훅을 받으려면 [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction)와 같은 사이트 공유 서비스를 활용해야 합니다. [Laravel Sail](/docs/master/sail)로 개발한다면 Sail의 [site sharing 커맨드](/docs/master/sail#sharing-your-site)를 참고하세요.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의 (Defining Webhook Event Handlers)

Cashier는 구독 실패/취소 등 일반적인 Paddle 웹훅을 자동 처리합니다. 그 외에 추가적으로 원하는 웹훅 이벤트를 다루고 싶다면, Cashier가 발생시키는 다음 이벤트를 리스닝하면 됩니다.

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅의 전체 payload가 포함되어 있습니다. 예를 들어, `transaction.billed` 웹훅을 직접 처리하고 싶다면 아래와 같이 [리스너](/docs/master/events#defining-listeners)를 등록하세요.

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
            // 추가 동작 구현...
        }
    }
}
```

Cashier는 웹훅 타입에 따라 더 세분화된 이벤트도 발생시킵니다. Paddle의 원본 payload뿐 아니라, 해당 webhook 처리를 위해 사용된 billable 모델, 구독, 영수증 등 관련 모델 객체도 포함됩니다.

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

기본 webhook 라우트를 오버라이드하려면, `.env` 파일에 `CASHIER_WEBHOOK` 환경변수를 정의하세요. 이 값은 완전한 URL이어야 하며 Paddle 컨트롤 패널에 등록한 주소와 동일해야 합니다.

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증 (Verifying Webhook Signatures)

보안을 위해 [Paddle 웹훅 서명](https://developer.paddle.com/webhooks/signature-verification) 기능을 활용하세요. Cashier는 이를 자동 검증하는 미들웨어를 기본 제공하므로, `.env`의 `PADDLE_WEBHOOK_SECRET`에 Paddle 대시보드에서 확인 가능한 웹훅 시크릿을 반드시 등록해야 합니다.

<a name="single-charges"></a>
## 단일 결제 (Single Charges)

<a name="charging-for-products"></a>
### 상품 결제 처리 (Charging for Products)

고객에게 단일 상품 결제를 제공하고자 할 때, billable 모델 인스턴스에서 `checkout` 메서드를 호출해 결제 세션을 생성할 수 있습니다. 이때 가격 ID(들)를 전달하며, 연관 배열로 수량도 함께 지정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

결제 세션 생성 후, `paddle-button` [Blade 컴포넌트](#overlay-checkout)로 사용자가 Paddle 결제 위젯을 통해 결제 완료할 수 있도록 안내하면 됩니다.

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

체크아웃 세션에는 `customData` 메서드로 Paddle에 추가 데이터를 넘길 수도 있습니다. 자세한 옵션은 [Paddle 공식문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하십시오.

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불 (Refunding Transactions)

거래 환불은 고객의 결제 수단으로 환불 금액이 반환되는 방식입니다. Paddle 구매 건을 환불하려면, `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 활용하세요. 인수로는 환불 사유, 환불할 가격 ID(들) 및 각 가격별 금액을 지정할 수 있습니다. 해당 billable 모델의 `transactions` 메서드로 거래 내역을 가져올 수 있습니다.

아래는 특정 거래에서 `pri_123`, `pri_456`를 환불하는 예시입니다. `pri_123`은 전액 환불, `pri_456`은 $2(200단위 환산)만 환불합니다.

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전액 환불
    'pri_456' => 200, // 부분 환불
]);
```

거래 전체를 환불하려면 환불 사유만 입력하면 됩니다.

```php
$response = $transaction->refund('Accidental charge');
```

자세한 환불 정책은 [Paddle의 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 환불 처리는 최종적으로 Paddle의 승인을 거쳐야 완료됩니다.

<a name="crediting-transactions"></a>
### 거래 크레딧 지급 (Crediting Transactions)

환불뿐만 아니라 크레딧(적립금) 지급도 가능합니다. 크레딧 처리는 환불처럼 금액이 바로 환급되지 않고, 고객의 잔액에 적립되어 추후 결제에 사용됩니다. 단, Paddle에서 수동 결제한 거래에만 적용할 수 있습니다. 구독 등 자동 결제 건은 Paddle이 크레딧을 자동 관리합니다.

```php
$transaction = $user->transactions()->first();

// 특정 항목 전체 금액 크레딧 지급
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [Paddle의 크레딧 지급 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 수동 결제 건에서만 크레딧 처리 가능합니다. 자동 결제 건은 Paddle에서 직접 크레딧을 관리합니다.

<a name="transactions"></a>
## 거래 내역 (Transactions)

청구 모델 인스턴스의 `transactions` 프로퍼티로 간편하게 거래 내역 배열을 가져올 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래는 상품 및 구매에 대한 결제와 인보이스가 1:1로 매칭되며, 완료된 거래만 DB에 저장됩니다.

사용자의 거래 내역을 테이블로 나열하고, 각각의 인보이스를 쉽게 다운로드할 수 있는 예시는 아래와 같습니다.

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

인보이스 다운로드 라우트는 아래처럼 구성할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 과거 및 예정 결제 내역 (Past and Upcoming Payments)

정기 구독의 경우, 직전/다음 결제(청구) 정보를 바로 가져올 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드 모두 `Laravel\Paddle\Payment` 인스턴스를 반환하며, 아직 거래가 동기화되지 않았거나 결제 주기가 끝났을 때는 `null`을 반환할 수 있습니다.

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트 (Testing)

테스트를 진행할 때는 실제 결제 흐름이 기대한 대로 동작하는지 직접 수동 테스트가 꼭 필요합니다.

CI 환경 등 자동화 테스트에서는 [Laravel의 HTTP 클라이언트](/docs/master/http-client#testing)를 사용해 Paddle로 가는 HTTP 요청을 fake 처리할 수 있습니다. Paddle의 실제 응답을 테스트하는 것은 아니지만, 외부 API 호출 없이 애플리케이션 로직은 테스트할 수 있습니다.
