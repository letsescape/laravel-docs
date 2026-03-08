# Laravel Cashier (Paddle) (Laravel Cashier (Paddle))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
- [설정](#configuration)
    - [청구 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [결제 세션](#checkout-sessions)
    - [오버레이 결제](#overlay-checkout)
    - [인라인 결제](#inline-checkout)
    - [비회원 결제](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객별 가격 미리보기](#customer-price-previews)
    - [할인](#price-discounts)
- [고객](#customers)
    - [고객 기본값](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 청구](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [여러 상품이 포함된 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [선결제방식 체험](#with-payment-method-up-front)
    - [결제정보 없이 체험](#without-payment-method-up-front)
    - [체험 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [상품 청구](#charging-for-products)
    - [트랜잭션 환불](#refunding-transactions)
    - [트랜잭션 크레딧](#crediting-transactions)
- [트랜잭션](#transactions)
    - [이전 및 예정 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 이 문서는 Cashier Paddle 2.x 버전에서 Paddle Billing과의 통합을 위한 내용입니다. Paddle Classic을 사용하는 경우에는 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 사용해야 합니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 청구 서비스에 대해 명확하고 직관적인 인터페이스를 제공합니다. 반복적인 청구 관련 코드를 대부분 대신 처리해주므로 부담을 줄여줍니다. 기본적인 구독 관리 외에도, Cashier는 구독 교체(스왑), 구독 "수량", 구독 일시정지, 취소 유예 기간 등 다양한 고급 기능들을 지원합니다.

Cashier Paddle을 사용하기 전에, Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 참고하시기 바랍니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier를 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 사용해 Paddle용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier-paddle
```

다음으로, `vendor:publish` Artisan 명령어를 실행해 Cashier 마이그레이션 파일을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이제 애플리케이션의 데이터베이스 마이그레이션을 실행합니다. Cashier의 마이그레이션을 통해 새로운 `customers` 테이블이 생성됩니다. 추가로 고객의 모든 구독 정보를 저장하는 `subscriptions` 및 `subscription_items` 테이블이 생성되고, 고객과 연관된 모든 Paddle 트랜잭션을 저장하는 `transactions` 테이블도 생성됩니다:

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 Paddle의 모든 이벤트를 정상적으로 처리하도록 하려면 반드시 [Cashier의 웹훅 핸들링 설정](#handling-paddle-webhooks)을 완료해야 합니다.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스 (Paddle Sandbox)

로컬 및 스테이징 개발 환경에서는 [Paddle 샌드박스 계정](https://sandbox-login.paddle.com/signup)을 등록해야 합니다. 이 계정을 통해 실제 결제 없이 애플리케이션을 테스트하고 개발할 수 있습니다. 다양한 결제 시나리오를 시뮬레이션하려면 Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)도 활용할 수 있습니다.

Paddle 샌드박스 환경을 사용하는 경우, 애플리케이션의 `.env` 파일에서 `PADDLE_SANDBOX` 환경 변수를 `true`로 지정합니다:

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발이 끝나면 [Paddle 판매자 계정](https://paddle.com)을 신청할 수 있습니다. 운영 환경으로 애플리케이션을 옮기기 전, Paddle에서 도메인 승인이 필요합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 청구 가능 모델 (Billable Model)

Cashier를 사용하기 전에, 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 정보 업데이트 등 청구 작업을 쉽게 처리할 수 있는 다양한 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자 외에 청구 가능한 엔티티(예: 팀 등)가 있다면 해당 클래스에도 트레이트를 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
### API 키 (API Keys)

다음으로, Paddle API 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Paddle 제어판에서 관련 API 키를 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 환경 변수는 [Paddle 샌드박스 환경](#paddle-sandbox)을 사용하는 경우 `true`로, 운영 환경에서는 `false`로 지정해야 합니다.

`PADDLE_RETAIN_KEY`는 선택 사항으로, [Retain](https://developer.paddle.com/concepts/retain/overview) 기능을 활용할 때만 지정하면 됩니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle 결제 창(Checkout)을 띄우기 위해서는 Paddle의 자바스크립트 라이브러리가 필요합니다. 애플리케이션 레이아웃의 종료 `</head>` 태그 바로 위에 `@paddleJS` Blade 디렉티브를 추가해 JS를 불러올 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

송장(인보이스)에 표시되는 금액의 통화 지역(locale)을 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 이용하여 통화 로케일을 적용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드 (Overriding Default Models)

Cashier 내부에서 사용하는 모델을 자유롭게 확장할 수 있습니다. 자신만의 모델을 정의하고, 기존 Cashier 모델을 상속하면 됩니다:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후, `Laravel\Paddle\Cashier` 클래스를 통해 Cashier가 새 모델을 사용하도록 지시할 수 있습니다. 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 이를 지정합니다:

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
### 상품 판매 (Selling Products)

> [!NOTE]
> Paddle 결제를 사용하기 전에, Paddle 대시보드에서 고정 가격의 상품을 반드시 정의해야 합니다. 또한 [Paddle의 웹훅 처리](#handling-paddle-webhooks)도 설정해야 합니다.

애플리케이션에서 상품/구독 과금 기능을 제공하는 것은 처음에는 부담스러울 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 사용하면 현대적이고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

반복되지 않는 단일 상품 청구를 위해, Cashier의 `checkout` 메서드를 활용해 Paddle Checkout Overlay를 띄웁니다. 사용자가 결제를 완료하면, 애플리케이션 내에서 원하는 성공 URL로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예시처럼, Cashier에서 제공하는 `checkout` 메서드로 Paddle Checkout Overlay에 표시할 "가격 식별자"에 대해 결제 객체를 생성합니다. Paddle에서는 "prices"가 [특정 상품별로 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요 시, `checkout` 메서드는 Paddle에서 고객을 자동 생성하며, 이 고객 정보를 애플리케이션의 사용자와 연결해줍니다. 결제 세션이 완료되면, 사용자는 지정한 성공 페이지로 이동하여 안내 메시지를 볼 수 있습니다.

`buy` 뷰에는 Checkout Overlay를 띄울 버튼이 포함되어야 하며, `paddle-button` Blade 컴포넌트가 Cashier Paddle에 내장되어 있습니다. 물론, [직접 오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout으로 메타데이터 전달하기

상품 판매 시, 애플리케이션에 정의된 `Cart` 및 `Order` 모델로 주문 완료 내역을 추적하는 경우가 많습니다. Paddle Checkout Overlay로 결제 시, 기존 주문 ID 등을 함께 전달하면 고객이 결제를 마치고 돌아올 때 해당 주문과 연동할 수 있습니다.

이때, `checkout` 메서드에 커스텀 데이터를 배열로 전달할 수 있습니다. 예를 들어, 사용자가 결제 프로세스를 시작하면 애플리케이션에 `Order`가 먼저 생성됩니다. 아래 `Cart`, `Order` 모델은 예시이며, 실제 구현은 각자 애플리케이션에 맞게 하시면 됩니다:

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

사용자가 결제를 시작하면, 해당 카트/주문의 Paddle 가격 식별자를 모두 `checkout` 메서드에 넘깁니다. 이 때, `customData` 메서드로 주문 ID 역시 Paddle Checkout Overlay에 전달합니다.

결제 완료 후 주문 상태를 "완료"로 바꾸려면, Paddle에서 전송되는 웹훅과 Cashier가 발생시키는 이벤트를 감지해 데이터베이스에 반영하면 됩니다.

우선, Cashier에서 발생하는 `TransactionCompleted` 이벤트를 수신하도록 리스너를 등록합니다. 일반적으로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트 리스너를 등록합니다:

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

`CompleteOrder` 리스너 예시는 다음과 같습니다:

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

`transaction.completed` 이벤트의 상세 데이터는 Paddle 공식 문서를 참고하세요: [Paddle Webhooks: Transaction Completed](https://developer.paddle.com/webhooks/transactions/transaction-completed).

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매 (Selling Subscriptions)

> [!NOTE]
> Paddle 결제를 사용하기 전에, Paddle 대시보드에서 고정 가격의 상품을 반드시 정의해야 합니다. 또한 [Paddle의 웹훅 처리](#handling-paddle-webhooks)도 설정해야 합니다.

상품/구독 과금 통합은 익숙하지 않을 수 있지만, Cashier와 [Paddle Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 덕분에 견고한 결제 처리를 쉽게 구축할 수 있습니다.

예를 들어, 월간(`price_basic_monthly`)과 연간(`price_basic_yearly`) 플랜이 있는 "Basic" 상품(`pro_basic`)이 있다고 가정해 봅니다. 또, "Expert" 플랜(`pro_expert`)도 존재할 수 있습니다.

먼저, 기본 월간 구독에 고객이 가입하는 흐름을 살펴봅니다. 사용자는 가격 페이지에서 "구독" 버튼을 클릭하며, 해당 플랜의 Paddle Checkout Overlay가 띄워집니다. 먼저 `checkout` 메서드를 활용한 결제 세션을 생성합니다:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 Checkout Overlay를 띄울 버튼을 표시합니다. `paddle-button` Blade 컴포넌트가 Cashier에 포함되어 있지만, [직접 오버레이를 구현](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 "Subscribe" 버튼 클릭 시, 고객은 결제 정보를 입력하고 구독에 가입할 수 있습니다. 구독이 실제로 시작되는 시점(일부 결제 수단의 처리 지연 등)을 파악하려면 [Cashier 웹훅 핸들링](#handling-paddle-webhooks) 설정도 반드시 필요합니다.

구독이 시작되면, 애플리케이션의 특정 영역을 구독한 사용자만 접근 가능하게 제한해야 할 경우가 있습니다. `Billable` 트레이트의 `subscribed` 메서드로 현재 구독 상태를 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 구독되어 있는지도 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 여부를 확인하는 미들웨어 만들기

편리하게 사용하기 위해 [미들웨어](/docs/12.x/middleware)에서 요청 사용자가 구독자인지 판별하도록 만들 수 있습니다. 이렇게 정의한 미들웨어는 해당 라우트에 쉽게 연결할 수 있습니다:

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
            // 사용자에게 결제 페이지로 이동하여 구독하라고 안내...
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

미들웨어를 라우트에 연결하는 예:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 자신의 구독 플랜을 직접 변경할 수 있도록 하기

고객이 구독 플랜을 다른 상품이나 "티어"로 변경하길 원할 수 있습니다. 예를 들어, 월 구독에서 연간 구독으로 변경하는 버튼을 다음과 같이 구현합니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 여기서 "$price"는 예를 들면 "price_basic_yearly"

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

구독 변경뿐 아니라 구독 해지도 직접 할 수 있도록 버튼을 만들어 다음 라우트에 연결하면 됩니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이렇게 하면 구독은 결제 기간이 끝났을 때 취소 처리됩니다.

> [!NOTE]
> Cashier의 웹훅 처리를 설정했다면, Paddle에서 수신하는 웹훅을 통해 Cashier가 데이터베이스의 구독 상태를 자동으로 동기화합니다. 예를 들어 Paddle 대시보드에서 구독이 취소된 경우에도 Cashier가 이를 받아 애플리케이션상의 구독을 "canceled"로 표시합니다.

<a name="checkout-sessions"></a>
## 결제 세션 (Checkout Sessions)

고객 과금 대부분은 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 결제](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)를 통해 진행됩니다.

결제 처리 전에 Paddle 대시보드에서 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 설정해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 결제 (Overlay Checkout)

Checkout Overlay 위젯을 표시하기 전에 Cashier를 사용해 결제 세션을 먼저 생성해야 합니다. 이는 결제 위젯에 어떤 과금 처리를 할지 알려줍니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier에는 `paddle-button` [Blade 컴포넌트](/docs/12.x/blade#components)가 내장되어 있습니다. 결제 세션을 prop으로 넘겨주면, 버튼 클릭 시 Paddle 결제 위젯이 표시됩니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 위젯은 Paddle의 기본 스타일로 표시됩니다. [Paddle에서 지원하는 속성](https://developer.paddle.com/paddlejs/html-data-attributes)을 Blade 컴포넌트에 추가해 커스터마이즈할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 결제 위젯은 비동기로 동작하며, 사용자가 위젯 내에서 구독을 생성하면 Paddle이 웹훅을 통해 애플리케이션에 상태 변경을 알립니다. 따라서 [웹훅 처리](#handling-paddle-webhooks)를 반드시 설정해야 합니다.

> [!WARNING]
> 구독 상태 변경 후 웹훅 수신까지의 지연은 보통 크지 않지만, 결제 완료 즉시 구독이 활성화되지 않을 수 있음을 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 결제 수동 렌더링

Blade 컴포넌트를 사용하지 않고 직접 오버레이 결제를 렌더링할 수도 있습니다. [이전 예시](#overlay-checkout)처럼 결제 세션을 생성한 후:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Paddle.js로 결제를 초기화할 수 있습니다. 이 예시는 `paddle_button` 클래스를 가진 링크를 생성하며, Paddle.js가 이를 감지해 오버레이를 표시합니다:

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
### 인라인 결제 (Inline Checkout)

Paddle의 "오버레이" 방식 대신, 결제 위젯을 페이지에 직접 삽입할 수도 있습니다. 이 방법은 결제 HTML 필드 조정은 불가하지만, 애플리케이션 내 원하는 위치에 위젯을 내장하는 데 유용합니다.

Cashier에는 인라인 결제를 쉽게 시작할 수 있는 `paddle-checkout` Blade 컴포넌트가 포함되어 있습니다. [오버레이 결제와 동일하게](#overlay-checkout) 결제 세션을 생성한 후:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그리고 아래와 같이 Blade 컴포넌트에 전달합니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 컴포넌트의 높이를 조정하려면 `height` 속성을 사용할 수 있습니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

인라인 결제 커스터마이즈에 대한 더 자세한 내용은 Paddle의 [인라인 결제 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [설정 문서](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 결제 수동 렌더링

Blade 컴포넌트를 사용하지 않고 직접 인라인 위젯을 렌더링하려면, [위에서처럼](#inline-checkout) 결제 세션을 생성한 뒤 다음과 같이 구현합니다. 예시에서는 [Alpine.js](https://github.com/alpinejs/alpine)를 썼지만, 프론트엔드 스택에 맞게 수정할 수 있습니다:

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
### 비회원 결제 (Guest Checkouts)

계정 없이 결제를 원하는 사용자를 위해 비회원용 결제 세션을 만들 수 있습니다. `guest` 메서드를 사용하세요:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

이렇게 생성한 결제 세션을 [Paddle 버튼](#overlay-checkout)이나 [인라인 결제](#inline-checkout) 컴포넌트에 넘겨 사용할 수 있습니다.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle은 서로 다른 국가별로 다른 통화와 가격을 설정할 수 있습니다. Cashier Paddle의 `previewPrices` 메서드를 사용하면 모든 통화에 대한 가격을 조회할 수 있습니다. 조회하려는 가격 ID를 배열로 전달합니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

통화는 기본적으로 요청 IP 기반으로 결정되지만, 다음처럼 명시적으로 국가를 지정할 수도 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

가져온 가격을 원하는 형식으로 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

금액(소계, 세금)을 분리해서 보여줄 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

자세한 내용은 [Paddle의 가격 미리보기 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 고객별 가격 미리보기 (Customer Price Previews)

이미 고객인 사용자의 통화에 맞춰 가격을 미리 보고 싶다면 해당 고객 인스턴스에서 가격을 가져올 수 있습니다:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

내부적으로 Cashier는 고객의 Paddle 고객 ID를 사용해 사용자의 통화로 가격을 가져옵니다. 예를 들어 미국 사용자에겐 달러, 벨기에 사용자에겐 유로로 표시됩니다. 일치하는 통화가 없으면 기본 상품 통화가 사용됩니다. 통화/가격 관리(설정)는 Paddle 대시보드에서 가능합니다.

<a name="price-discounts"></a>
### 할인 (Discounts)

가격 미리보기에 할인도 반영할 수 있습니다. `previewPrices` 호출 시 옵션에 `discount_id`를 추가합니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 가격을 표시합니다:

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
### 고객 기본값 (Customer Defaults)

Cashier는 결제 세션 생성 시 고객 정보를 미리 채울 기본값을 정의할 수 있습니다. 기본 설정을 통해 고객의 이름/이메일을 Paddle 결제창에 자동 입력할 수 있습니다. 해당 메서드를 `Billable` 모델에 오버라이드하세요:

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

이 기본 정보는 Cashier가 [결제 세션](#checkout-sessions)을 생성할 때마다 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회 (Retrieving Customers)

Paddle 고객 ID로 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용하세요. 해당 메서드는 청구 가능 모델 인스턴스를 반환합니다:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

별도의 구독 없이 Paddle 고객을 먼저 생성하고 싶은 경우, `createAsCustomer` 메서드를 사용할 수 있습니다:

```php
$customer = $user->createAsCustomer();
```

`Laravel\Paddle\Customer` 인스턴스를 반환합니다. 고객 생성 후 나중에 구독을 시작할 수 있습니다. 필요에 따라 `$options` 배열을 추가로 넘겨 [Paddle API에서 지원하는 파라미터](https://developer.paddle.com/api-reference/customers/create-customer)를 전달할 수 있습니다:

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독을 생성하려면 데이터베이스에서 청구 가능 모델 인스턴스를 먼저 조회하세요. 보통은 `App\Models\User` 인스턴스입니다. 다음으로, `subscribe` 메서드로 해당 모델의 결제 세션을 생성합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe` 메서드의 첫 번째 인자는 구독할 Paddle 가격 ID입니다. 이 값은 Paddle 상품 가격의 식별자여야 합니다. `returnTo`는 결제가 끝난 뒤 사용자를 리디렉트할 URL입니다. 두 번째 인자는 구독의 내부 "타입"이며, 애플리케이션에서 내부적으로만 사용되므로 `default`나 `primary`처럼 단순하게 지정하면 됩니다. 구독 타입에는 공백을 포함하지 않아야 하며, 구독 생성 후에는 변경하면 안 됩니다.

구독에 대한 커스텀 메타데이터는 `customData` 메서드로 전달할 수 있습니다:

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

세션이 생성되면, Cashier Paddle에 내장된 `paddle-button` [Blade 컴포넌트](#overlay-checkout)에 넘겨 사용할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

구독이 완료되면, Paddle에서 `subscription_created` 웹훅을 보내고, Cashier가 이를 받아 구독을 세팅합니다. 모든 웹훅이 제대로 수신/처리되는지 항상 [웹훅 처리 설정](#handling-paddle-webhooks)을 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

사용자 구독 상태는 편리한 메서드들을 통해 쉽게 확인할 수 있습니다. `subscribed` 메서드는 사용자가 유효한 구독(체험 기간 포함)을 갖고 있으면 `true`를 반환합니다:

```php
if ($user->subscribed()) {
    // ...
}
```

여러 구독이 있다면, 인자로 구독 타입을 지정할 수도 있습니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/12.x/middleware)로 사용해, 구독 유무에 따라 접근을 제한할 때 활용할 수 있습니다:

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
            // 유료 고객이 아님...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

사용자가 체험 기간 내에 있는지 확인하려면 `onTrial` 메서드를 활용하면 됩니다. 보통 체험 마지막일 때 안내 메시지를 표시할 때 유용합니다:

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 가격 ID 기반으로 특정 플랜에 구독 중인지 확인할 땐 `subscribedToPrice` 메서드를 사용합니다. 예시는 다음과 같습니다:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

현재 구독이 활성 상태(체험 기간, 유예 기간 아님)임을 확인하려면 `recurring` 메서드를 사용하세요:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 구독 해지(취소) 상태

한때 활성 구독자였으나 구독을 해지한 사용자인지 확인하려면 `canceled` 메서드를 사용하세요:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

구독 해지 직후부터 완전 만료 사이의 "유예 기간(grace period)" 여부는 `onGracePeriod`로 확인합니다. 즉, 3월 5일 구독 취소 → 3월 10일 만료라면, 3월 10일까지는 유예 기간입니다. 이 기간 동안 `subscribed`도 여전히 `true`를 반환합니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체(past_due) 상태

구독 결제 실패 시, 상태는 `past_due`로 변경됩니다. 결제 정보가 갱신되기 전까지 비활성화됩니다. 구독이 연체인지 확인은 `pastDue` 메서드로 할 수 있습니다:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

이 경우 사용자가 [결제 정보를 업데이트](#updating-payment-information)하도록 안내하십시오.

연체 상태에도 구독을 유효하게 처리하고 싶다면, Cashier의 `keepPastDueSubscriptionsActive` 메서드를 `AppServiceProvider`의 `register` 메서드에서 호출합니다:

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
> 연체 상태에서는 구독을 변경할 수 없습니다. `swap`, `updateQuantity` 등 변경 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 상태 쿼리 스코프

대부분의 구독 상태는 쿼리 스코프로도 제공되므로, 데이터베이스에서 원하는 상태의 구독만 쉽게 조회할 수 있습니다:

```php
// 모든 유효 구독 조회
$subscriptions = Subscription::query()->valid()->get();

// 한 사용자의 모든 취소된 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 전체 쿼리 스코프는 다음과 같습니다:

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
### 구독 단일 청구 (Subscription Single Charges)

구독자에게 추가로 1회성 청구를 진행할 수 있습니다. `charge` 메서드에 가격 ID 하나 또는 배열을 넘기세요:

```php
// 가격 1개 청구
$response = $user->subscription()->charge('pri_123');

// 가격 여러개 동시 청구
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

이때 고객에게 실제 청구는 구독의 다음 청구 주기에서 이뤄집니다. 즉시 청구하고 싶다면 `chargeAndInvoice` 메서드를 사용하세요:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트 (Updating Payment Information)

Paddle은 구독별로 결제 정보를 별도로 저장합니다. 기본 결제 수단을 업데이트하려면 `redirectToUpdatePaymentMethod` 메서드로 Paddle의 결제 정보 수정 페이지로 리디렉션하세요:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

사용자가 정보를 갱신하면 Paddle은 `subscription_updated` 웹훅을 보내주며, 애플리케이션의 구독 정보가 갱신됩니다.

<a name="changing-plans"></a>
### 플랜 변경 (Changing Plans)

사용자가 구독 중간에 플랜을 바꾸길 원할 때는, 변경 대상 가격의 식별자를 구독의 `swap` 메서드에 전달하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 청구와 함께 플랜을 변경하려면 `swapAndInvoice` 메서드를 사용하세요:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 일할 계산(Prorations)

기본적으로 Paddle은 플랜 변경 시 요금을 일할 계산합니다. 청구 일할 계산 없이 즉시 변경만 원할 때는 `noProrate` 메서드를 사용합니다:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

일할 계산 없이 즉시 청구까지 원한다면 다음과 같이 조합할 수 있습니다:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

고객에게 요금 청구 없이 플랜만 변경하려면 `doNotBill` 메서드를 활용하세요:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

일할 계산 정책 관련 자세한 내용은 Paddle의 [공식 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량 (Subscription Quantity)

일부 구독은 "수량"에 따라 요금이 달라집니다(예: 프로젝트별 월 $10 과금 등). 수량을 손쉽게 늘리거나 줄일 때는 다음 메서드를 사용하세요:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 수량 5개 추가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 수량 5개 차감
$user->subscription()->decrementQuantity(5);
```

`updateQuantity` 메서드로 원하는 수량으로 직접 설정할 수도 있습니다:

```php
$user->subscription()->updateQuantity(10);
```

일할 계산 없이 수량만 업데이트하려면 `noProrate`와 함께 사용하세요:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 상품이 포함된 구독의 수량 조절

[여러 상품 구독](#subscriptions-with-multiple-products) 환경에서는 수량 변경 대상 가격 ID를 두 번째 인자로 넘기세요:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 상품이 포함된 구독 (Subscriptions With Multiple Products)

[여러 상품이 포함된 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons) 기능을 이용하면 하나의 구독에 여러 개의 상품을 묶어 요금 청구가 가능합니다. 예를 들어, 헬프데스크 베이스 구독($10/월)과 라이브챗 부가 상품($15/월)을 동시에 제공할 수 있습니다.

구독 세션 생성 시 여러 상품 가격을 배열로 넘기면 됩니다:

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

각 가격의 수량을 지정하려면 키/값 쌍의 연관 배열로 넘깁니다:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 상품을 추가하려면 `swap` 메서드를 이용하며, 기존 가격과 수량도 같이 전달해야 합니다:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

새 상품에 대한 청구도 즉시 하려면 `swapAndInvoice`를 사용하세요:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

상품 제거는 삭제할 가격을 배열에서 빼고 나머지만 넘겨주면 됩니다:

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독에서 마지막 가격을 제거할 수는 없습니다. 이 경우 구독을 아예 취소해야 합니다.

<a name="multiple-subscriptions"></a>
### 다중 구독 (Multiple Subscriptions)

Paddle은 한 고객이 여러 구독을 동시에 가질 수 있습니다. 예를 들어, 헬스장 수영 구독과 헬스 구독을 각각 운영하며, 고객이 둘 중 하나 또는 둘 다 구독할 수 있습니다.

구독 생성 시 `subscribe` 메서드의 두 번째 인자로 구독 타입을 넘기면 됩니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

나중에 연간 구독 등 다른 플랜으로 전환할 때는 해당 구독 타입을 지정해 `swap`을 사용하면 됩니다:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

구독 해지 시에도 동일하게 사용할 수 있습니다:

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시정지 (Pausing Subscriptions)

구독을 일시정지하려면 `pause` 메서드를 호출하세요:

```php
$user->subscription()->pause();
```

일시정지 시 Cashier는 `paused_at` 열을 기록합니다. 예를 들어 3월 1일 일시정지 요청 → 다음 결제 예정이 3월 5일이면, 3월 5일까지는 `paused` 메서드가 `false`를 반환하며, 이후부터 `true`가 됩니다.

일반적으로 일시정지는 결제 주기가 끝날 때부터 적용되지만, 즉시 일시정지 하고 싶으면 `pauseNow`를 사용하세요:

```php
$user->subscription()->pauseNow();
```

특정 시점까지 일시정지하려면 `pauseUntil`:

```php
$user->subscription()->pauseUntil(now()->plus(months: 1));
```

즉시 일시정지 후 지정 시점까지 일시정지하려면 `pauseNowUntil`:

```php
$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```

유예 기간 내 일시정지 상태인지 확인하려면 `onPausedGracePeriod`를 사용하세요:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

일시정지된 구독을 재개하려면 `resume`:

```php
$user->subscription()->resume();
```

> [!WARNING]
> 일시정지 중인 구독은 변경이 불가합니다. 플랜 변경, 수량 조정 등을 위해서는 먼저 일시정지를 풀어야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소 (Canceling Subscriptions)

구독을 취소하려면 `cancel` 메서드를 호출합니다:

```php
$user->subscription()->cancel();
```

취소 시 Cashier는 `ends_at` 필드를 기록합니다. 예를 들어 3월 1일 취소 요청 → 3월 5일 만기라면, 3월 5일까지 `subscribed`는 계속 `true`입니다.

유예 기간 중인 구독 여부는 `onGracePeriod`로 알 수 있습니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 구독을 취소하고 싶으면 `cancelNow`를 사용하세요:

```php
$user->subscription()->cancelNow();
```

유예 기간의 취소를 멈추려면 `stopCancelation` 메서드:

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle 구독은 취소 후 재개가 불가능합니다. 고객이 다시 구독을 원하면 신규 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험 기간 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 정보 기반 체험 (With Payment Method Up Front)

체험 기간 동안 결제 정보도 미리 수집하고 싶다면, Paddle 대시보드에서 가격의 체험 기간을 설정한 뒤 일반적인 결제 세션을 생성하세요:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

구독 생성 이벤트(`subscription_created`) 수신 시, Cashier는 구독 레코드에 체험 만료일을 설정하고, 해당 일까지 실제 청구가 발생하지 않도록 Paddle에 지시합니다.

> [!WARNING]
> 체험 만료일까지 구독을 취소하지 않으면 만료 즉시 요금이 청구되므로, 반드시 체험 종료일을 사용자에게 고지하세요.

사용자가 체험 기간 내에 있는지 확인하려면 모델 인스턴스의 `onTrial`을 사용합니다:

```php
if ($user->onTrial()) {
    // ...
}
```

체험이 만료되었는지는 `hasExpiredTrial`로 확인:

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

특정 구독 타입의 체험 상태를 확인하려면 타입명을 인자로 넘기세요:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 체험 기간만 부여 (Without Payment Method Up Front)

결제 정보를 미리 받지 않는 체험을 제공하려면, 사용자 등록 과정에서 해당 고객 레코드의 `trial_ends_at`을 원하는 체험 종료일로 설정하세요:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->plus(days: 10)
]);
```

Cashier는 이를 "일반 체험(generic trial)"이라 부릅니다. 실제 구독 없이 체험을 부여하는 것이기 때문입니다. 현재 일자가 `trial_ends_at` 이전이면 `onTrial` 메서드가 `true`를 반환합니다:

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

체험이 끝난 후에는 일반 구독 생성과 같이 `subscribe` 메서드로 실구독을 시작하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

사용자의 체험 만료일은 `trialEndsAt`로 확인할 수 있습니다:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

아직 실제 구독 없이 "일반" 체험 기간만 적용되었는지 확인하려면 `onGenericTrial`을 사용하세요:

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험 연장 및 활성화 (Extend or Activate a Trial)

기존 구독의 체험 기간을 연장하려면 `extendTrial`에 원하는 만료일을 지정하세요:

```php
$user->subscription()->extendTrial(now()->plus(days: 5));
```

즉시 체험을 종료하고 구독을 활성화하려면 `activate` 메서드를 사용합니다:

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리 (Handling Paddle Webhooks)

Paddle은 다양한 이벤트를 웹훅으로 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier 서비스 프로바이더는 Cashier의 웹훅 컨트롤러로 연결되는 라우트를 등록합니다.

이 컨트롤러는 과도한 결제 실패로 인한 구독 취소, 구독 정보 갱신, 결제 수단 변경 등 대부분의 Paddle 웹훅을 자동 처리합니다. 추가 웹훅을 처리하고 싶다면, 컨트롤러를 확장해 구현할 수 있습니다.

Paddle 웹훅을 수신하려면, Paddle 제어판에 [웹훅 URL을 등록](https://vendors.paddle.com/notifications-v2)해야 합니다. 기본적으로 Cashier는 `/paddle/webhook` 경로에서 웹훅 요청을 받습니다. Paddle 제어판에서는 아래 모든 웹훅을 활성화해야 합니다:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> 웹훅 요청을 보호하려면 Cashier에서 제공하는 [웹훅 서명 검증 미들웨어](/docs/12.x/cashier-paddle#verifying-webhook-signatures)를 반드시 사용하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Paddle 웹훅 요청이 Laravel의 [CSRF 보호](/docs/12.x/csrf)를 우회해야 하므로, `bootstrap/app.php`에서 웹훅 경로를 CSRF 예외로 지정해야 합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 로컬 개발 환경에서의 웹훅 처리

로컬 개발 환경에서 Paddle 웹훅을 테스트하려면 [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction) 등의 사이트 공유 서비스를 사용해야 합니다. [Laravel Sail](/docs/12.x/sail)로 개발 중이라면 Sail의 [사이트 공유 명령어](/docs/12.x/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의 (Defining Webhook Event Handlers)

Cashier는 기본적으로 결제 실패에 따른 구독 해지 등 일반 웹훅을 자동 처리합니다. 추가로 원하는 Paddle 웹훅을 처리하려면 Cashier에서 발생시키는 다음 이벤트를 리스닝하면 됩니다:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅의 전체 페이로드를 포함합니다. 예를 들어 `transaction.billed` 웹훅을 처리하려면 아래와 같이 리스너를 정의할 수 있습니다:

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
            // 이벤트 처리...
        }
    }
}
```

Cashier는 웹훅 종류별로도 전용 이벤트를 발생시킵니다. Paddle에서 받은 전체 페이로드와 함께, 처리된 모델(청구 가능 모델, 구독, 영수증 등)도 함께 전달됩니다:

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

기본 웹훅 라우트를 오버라이드 하려면 `.env` 파일에서 `CASHIER_WEBHOOK` 환경 변수를 설정하세요. 이 값은 웹훅 경로의 전체 URL이어야 하며, Paddle 제어판의 URL과 동일해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증 (Verifying Webhook Signatures)

웹훅 보안을 위해 [Paddle의 웹훅 서명 기능](https://developer.paddle.com/webhooks/signature-verification)을 활용할 수 있습니다. Cashier는 Paddle 웹훅 요청의 유효성을 확인하는 미들웨어를 자동으로 제공합니다.

웹훅 검증을 활성화하려면 `.env` 파일의 `PADDLE_WEBHOOK_SECRET` 환경 변수를 반드시 지정해야 하며, 이 값은 Paddle 계정 대시보드에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 청구 (Single Charges)

<a name="charging-for-products"></a>
### 상품 청구 (Charging for Products)

고객에게 즉시 상품을 판매하고 싶을 때, 청구 가능한 모델 인스턴스의 `checkout` 메서드를 이용해 결제 세션을 생성합니다. 하나 또는 여러 가격 ID, 그리고 필요시 각 상품별 수량을 연관 배열로 넘길 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

세션 생성 후, Cashier의 `paddle-button` [Blade 컴포넌트](#overlay-checkout)로 고객에게 결제 위젯을 띄웁니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

특정 트랜잭션 생성 시 원하는 커스텀 데이터를 추가하려면 checkout 세션의 `customData` 메서드를 사용합니다. [Paddle 공식문서의 Custom Data](https://developer.paddle.com/build/transactions/custom-data)도 참고하세요:

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 트랜잭션 환불 (Refunding Transactions)

환불은 고객이 결제했던 동일 결제수단으로 금액을 환급합니다. Paddle 구매를 환불하려면 `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 사용하세요. 첫 인자는 환불 사유, 두 번째 인자는 하나 이상의 가격 ID(필요하면 각 가격별 환불 금액)입니다. 트랜잭션 목록은 모델의 `transactions` 메서드로 얻을 수 있습니다.

예시: 가격 `pri_123`은 전체, `pri_456`은 $2만 환불하려면:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전체 환불
    'pri_456' => 200, // $2만 환불
]);
```

전체 환불은 사유만 넘기면 됩니다:

```php
$response = $transaction->refund('Accidental charge');
```

환불 관련 자세한 내용은 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 환불은 항상 Paddle의 승인이 필요합니다.

<a name="crediting-transactions"></a>
### 트랜잭션 크레딧 (Crediting Transactions)

환불과 유사하게 크레딧도 적용할 수 있습니다. 크레딧을 부여하면 고객의 결제 잔액에 금액이 적립되어, 향후 결제에 사용 가능합니다. 단, 크레딧 적용은 수동으로 결제된 트랜잭션에만 사용할 수 있습니다(구독과 같은 자동 결제 트랜잭션에는 Paddle이 자체적으로 크레딧을 처리):

```php
$transaction = $user->transactions()->first();

// 특정 라인 아이템 전체 크레딧
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 정보는 [Paddle 크레딧 가이드](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참조하세요.

> [!WARNING]
> 자동 결제 트랜잭션(구독 등)에는 직접 크레딧을 적용할 수 없습니다. 구독 관련 크레딧은 Paddle에서 자동 처리합니다.

<a name="transactions"></a>
## 트랜잭션 (Transactions)

청구 가능 모델의 트랜잭션 리스트는 `transactions` 속성으로 쉽게 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

트랜잭션은 실제 결제 및 구매 내역을 나타내며, 각 결제에는 인보이스가 첨부됩니다. 완료된 트랜잭션만 데이터베이스에 기록됩니다.

사용자 트랜잭션을 테이블로 나열하고, 각 행에서 인보이스 다운로드 기능을 구현할 수 있습니다:

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

다운로드 라우트 예시는 다음과 같습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 이전 및 예정 결제 (Past and Upcoming Payments)

`lastPayment`, `nextPayment` 메서드로 반복 구독 고객의 과거 결제와 예정 결제를 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 단, `lastPayment`는 아직 웹훅을 통한 동기화가 안됐다면 `null`을 반환하며, `nextPayment`는 결제 주기가 종료됐다면(구독 종료 등) 역시 `null`을 반환합니다:

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트 (Testing)

테스트할 때는 실제 결제 흐름을 직접 충분히 검증하는 것이 좋습니다.

자동화 테스트 및 CI 환경 등에서는 [Laravel HTTP 클라이언트](/docs/12.x/http-client#testing)로 Paddle로의 HTTP 요청을 fake 처리할 수 있습니다. 이는 Paddle 응답을 실제로 테스트하지는 않지만, Paddle API 호출 없이 애플리케이션 동작 검증에 도움이 됩니다.
