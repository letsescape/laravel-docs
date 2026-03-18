# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
- [구성](#configuration)
    - [청구 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 구성](#currency-configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [결제 세션](#checkout-sessions)
    - [오버레이 체크아웃](#overlay-checkout)
    - [인라인 결제](#inline-checkout)
    - [비회원 결제](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객 가격 미리보기](#customer-price-previews)
    - [할인](#price-discounts)
- [고객](#customers)
    - [고객 기본값](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 현황 확인](#checking-subscription-status)
    - [구독 단일 요금](#subscription-single-charges)
    - [결제정보 업데이트](#updating-payment-information)
    - [계획 변경](#changing-plans)
    - [구독수량](#subscription-quantity)
    - [여러 제품에 대한 구독](#subscriptions-with-multiple-products)
    - [복수구독](#multiple-subscriptions)
    - [구독 일시중지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 평가판](#subscription-trials)
    - [결제 수단이 선불인 경우](#with-payment-method-up-front)
    - [선불 결제 수단 없음](#without-payment-method-up-front)
    - [평가판 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 처리기 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 확인](#verifying-webhook-signatures)
- [1회 충전](#single-charges)
    - [상품 충전](#charging-for-products)
    - [환불 거래](#refunding-transactions)
    - [크레딧 거래](#crediting-transactions)
- [거래](#transactions)
    - [과거 및 향후 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 이 문서는 Cashier Paddle 2.x와 Paddle Billing의 통합을 위한 것입니다. 아직 Paddle Classic을 사용하고 있다면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 사용해야 합니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)는 [Paddle's](https://paddle.com) 구독 청구 서비스에 표현력이 풍부하고 유창한 인터페이스를 제공합니다. 당신이 두려워하는 거의 모든 상용구 구독 청구 코드를 처리합니다. 기본적인 구독 관리 외에도 Cashier는 구독 교환, 구독 "수량", 구독 일시 중지, 취소 유예 기간 등을 처리할 수 있습니다.

Cashier Paddle를 자세히 알아보기 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview) 및 [API 문서](https://developer.paddle.com/api-reference/overview)도 검토하는 것이 좋습니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 주의 깊게 검토하는 것이 중요합니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 사용하여 Paddle용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier-paddle
```

다음으로, `vendor:publish` Artisan 명령을 사용하여 Cashier 마이그레이션 파일을 게시해야 합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그런 다음 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. Cashier 마이그레이션은 새로운 `customers` 테이블을 생성합니다. 또한 고객의 모든 구독을 저장하기 위해 새로운 `subscriptions` 및 `subscription_items` 테이블이 생성됩니다. 마지막으로 고객과 관련된 모든 Paddle 트랜잭션을 저장하기 위해 새로운 `transactions` 테이블이 생성됩니다.

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 올바르게 처리하도록 하려면 [Cashier의 웹훅 ​​처리 설정](#handling-paddle-webhooks)을 수행하세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 및 스테이징 개발 중에는 [Paddle 샌드박스 계정을 등록](https://sandbox-login.paddle.com/signup)해야 합니다. 이 계정은 실제 결제 없이 애플리케이션을 테스트하고 개발할 수 있는 샌드박스 환경을 제공합니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 사용하여 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

Paddle 샌드박스 환경을 사용하는 경우 애플리케이션의 `.env` 파일 내에서 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다.

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발을 마친 후 [Paddle 공급업체 계정을 신청](https://paddle.com)할 수 있습니다. 애플리케이션이 프로덕션에 배치되기 전에 Paddle는 애플리케이션 도메인을 승인해야 합니다.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="billable-model"></a>
### 청구 가능 모델

Cashier를 사용하기 전에 사용자 모델 정의에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성 및 결제 방법 정보 업데이트와 같은 일반적인 청구 작업을 수행할 수 있는 다양한 메서드를 제공합니다.

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 청구 가능한 엔터티가 있는 경우 해당 클래스에 트레이트를 추가할 수도 있습니다.

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

다음으로, 애플리케이션의 `.env` 파일에서 Paddle 키를 구성해야 합니다. Paddle 제어판에서 Paddle API 키를 검색할 수 있습니다.

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

[Paddle의 샌드박스 환경](#paddle-sandbox)을 사용하는 경우에는 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다. 애플리케이션을 프로덕션에 배포하고 Paddle의 라이브 공급업체 환경을 사용하는 경우 `PADDLE_SANDBOX` 변수를 `false`로 설정해야 합니다.

`PADDLE_RETAIN_KEY`는 선택 사항이며 [Retain](https://developer.paddle.com/concepts/retain/overview)과 함께 Paddle를 사용하는 경우에만 설정해야 합니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle는 자체 JavaScript 라이브러리를 사용하여 Paddle 결제 위젯을 시작합니다. 애플리케이션 레이아웃의 닫는 `</head>` 태그 바로 앞에 `@paddleJS` Blade 지시문을 배치하여 JavaScript 라이브러리를 로드할 수 있습니다.

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 구성

송장에 표시할 금액 값의 형식을 지정할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용하여 통화 로케일을 설정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로캘을 사용하려면 `ext-intl` PHP 확장이 서버에 설치 및 구성되어 있는지 확인하세요.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

자신만의 모델을 정의하고 해당 Cashier 모델을 확장하여 Cashier에서 내부적으로 사용되는 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후 `Laravel\Paddle\Cashier` 클래스를 통해 사용자 지정 모델을 사용하도록 Cashier에 지시할 수 있습니다. 일반적으로 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 사용자 지정 모델에 대해 Cashier에 알려야 합니다.

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
### 상품 판매

> [!NOTE]
> Paddle Checkout을 활용하기 전에 Paddle 대시보드에서 고정 가격으로 제품을 정의해야 합니다. 또한 [Paddle의 웹훅 ​​처리를 구성](#handling-paddle-webhooks)해야 합니다.

애플리케이션을 통해 제품 및 구독 청구를 제공하는 것은 어려울 수 있습니다. 그러나 Cashier 및 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 덕분에 현대적이고 강력한 결제 통합을 쉽게 구축할 수 있습니다.

일회성 비반복 제품에 대해 고객에게 비용을 청구하기 위해 우리는 Cashier를 활용하여 Paddle의 결제 오버레이로 고객에게 비용을 청구할 것입니다. 여기서 고객은 결제 세부 정보를 제공하고 구매를 확인하게 됩니다. Checkout Overlay를 통해 결제가 완료되면 고객은 애플리케이션 내에서 선택한 성공 URL로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위의 예에서 볼 수 있듯이 Cashier에서 제공하는 `checkout` 메서드를 활용하여 고객에게 지정된 "가격 식별자"에 대한 Paddle 결제 오버레이를 제공하는 결제 개체를 생성합니다. Paddle 사용 시 "가격"은 [특정 제품에 대해 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요한 경우 `checkout` 메서드는 자동으로 Paddle에 고객을 생성하고 해당 Paddle 고객 레코드를 애플리케이션 데이터베이스의 해당 사용자에 연결합니다. 결제 세션을 완료하면 고객은 정보 메시지를 표시할 수 있는 전용 성공 페이지로 리디렉션됩니다.

`buy` 뷰에는 결제 오버레이를 표시하는 버튼이 포함됩니다. `paddle-button` Blade 컴포넌트는 Cashier Paddle에 포함되어 있습니다. 그러나 [오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타데이터 제공

제품을 판매할 때 자체 애플리케이션에서 정의한 `Cart` 및 `Order` 모델을 통해 완료된 주문과 구매한 제품을 추적하는 것이 일반적입니다. 구매를 완료하기 위해 고객을 Paddle의 결제 오버레이로 리디렉션할 때 고객이 애플리케이션으로 다시 리디렉션될 때 완료된 구매를 해당 주문과 연결할 수 있도록 기존 주문 식별자를 제공해야 할 수도 있습니다.

이를 달성하기 위해 `checkout` 메서드에 사용자 지정 데이터 배열을 제공할 수 있습니다. 사용자가 결제 프로세스를 시작할 때 애플리케이션 내에서 보류 중인 `Order`가 생성된다고 가정해 보겠습니다. 이 예의 `Cart` 및 `Order` 모델은 설명을 위한 것이며 Cashier에서 제공되지 않습니다. 자신의 애플리케이션 요구 사항에 따라 다음 개념을 자유롭게 구현할 수 있습니다.

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

위의 예에서 볼 수 있듯이 사용자가 결제 프로세스를 시작하면 장바구니/주문과 관련된 모든 Paddle 가격 식별자를 `checkout` 메서드에 제공합니다. 물론 애플리케이션은 이러한 항목을 "장바구니"와 연결하거나 고객이 항목을 추가할 때 주문하는 일을 담당합니다. 또한 `customData` 메서드를 통해 Paddle Checkout Overlay에 주문 ID를 제공합니다.

물론 고객이 결제 프로세스를 완료하면 주문을 "완료"로 표시하고 싶을 것입니다. 이를 달성하려면 Paddle의 웹후크 디스패치를 수신하고 Cashier의 이벤트를 통해 발생하여 데이터베이스에 주문 정보를 저장할 수 있습니다.

시작하려면 Cashier의 `TransactionCompleted` 이벤트 디스패치를 들어보세요. 일반적으로 애플리케이션 `AppServiceProvider`의 `boot` 메서드에 이벤트 리스너를 등록해야 합니다.

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

이 예에서 `CompleteOrder` 리스너는 다음과 같습니다.

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

[`transaction.completed` 이벤트에 포함된 데이터](https://developer.paddle.com/webhooks/transactions/transaction-completed)에 대한 자세한 내용은 Paddle의 설명서를 참조하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]
> Paddle Checkout을 활용하기 전에 Paddle 대시보드에서 고정 가격으로 제품을 정의해야 합니다. 또한 [Paddle의 웹훅 ​​처리를 구성](#handling-paddle-webhooks)해야 합니다.

애플리케이션을 통해 제품 및 구독 청구를 제공하는 것은 어려울 수 있습니다. 그러나 Cashier 및 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 덕분에 현대적이고 강력한 결제 통합을 쉽게 구축할 수 있습니다.

Cashier 및 Paddle의 결제 오버레이를 사용하여 구독을 판매하는 방법을 알아보려면 기본 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 요금제를 사용하는 구독 서비스의 간단한 시나리오를 고려해 보겠습니다. 이 두 가지 가격은 Paddle 대시보드의 "기본" 제품(`pro_basic`)으로 그룹화될 수 있습니다. 또한 당사의 구독 서비스는 `pro_expert`와 같은 "전문가" 계획을 제공할 수 있습니다.

먼저 고객이 당사 서비스에 가입할 수 있는 방법을 살펴보겠습니다. 물론 고객이 애플리케이션 가격 페이지에서 기본 요금제에 대한 "구독" 버튼을 클릭할 수도 있다고 상상할 수 있습니다. 이 버튼은 선택한 계획에 대한 Paddle 결제 오버레이를 호출합니다. 시작하려면 `checkout` 메서드를 통해 결제 세션을 시작해 보겠습니다.

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에는 결제 오버레이를 표시하는 버튼이 포함됩니다. `paddle-button` Blade 컴포넌트는 Cashier Paddle에 포함되어 있습니다. 그러나 [오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 구독 버튼을 클릭하면 고객이 결제 세부정보를 입력하고 구독을 시작할 수 있습니다. 구독이 실제로 언제 시작되었는지 확인하려면(일부 결제 방법을 처리하는 데 몇 초가 걸리기 때문에) [Cashier의 웹훅 ​​처리를 구성](#handling-paddle-webhooks)해야 합니다.

이제 고객이 구독을 시작할 수 있으므로 구독한 사용자만 액세스할 수 있도록 애플리케이션의 특정 부분을 제한해야 합니다. 물론, Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 통해 언제든지 사용자의 현재 구독 상태를 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

사용자가 특정 제품이나 가격을 구독하는지 쉽게 확인할 수도 있습니다.

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독된 미들웨어 구축

편의를 위해 수신 요청이 구독 사용자로부터 오는 것인지 확인하는 [미들웨어](/docs/13.x/middleware)를 생성할 수 있습니다. 이 미들웨어가 정의되면 이를 라우트에 쉽게 할당하여 구독하지 않은 사용자가 라우트에 액세스하지 못하도록 방지할 수 있습니다.

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

미들웨어가 정의되면 이를 라우트에 할당할 수 있습니다.

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 청구 계획을 관리할 수 있도록 허용

물론 고객은 구독 계획을 다른 제품이나 "계층"으로 변경하기를 원할 수도 있습니다. 위의 예에서는 고객이 월간 구독에서 연간 구독으로 요금제를 변경할 수 있도록 허용하려고 합니다. 이를 위해서는 아래 라우트로 연결되는 버튼과 같은 것을 구현해야 합니다.

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // With "$price" being "price_basic_yearly" for this example.

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

요금제를 바꾸는 것 외에도 고객이 구독을 취소할 수 있도록 허용해야 합니다. 계획 교환과 마찬가지로 다음 라우트로 연결되는 버튼을 제공하세요.

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이제 청구 기간이 끝나면 구독이 취소됩니다.

> [!NOTE]
> Cashier의 웹훅 ​​처리를 구성한 한, Cashier는 Paddle에서 들어오는 웹훅을 검사하여 자동으로 애플리케이션의 계산원 관련 데이터베이스 테이블을 동기화된 상태로 유지합니다. 예를 들어 Paddle 대시보드를 통해 고객의 구독을 취소하면 Cashier는 해당 웹훅을 수신하고 애플리케이션 데이터베이스에서 구독을 "취소됨"으로 표시합니다.

<a name="checkout-sessions"></a>
## 결제 세션 (Checkout Sessions)

고객에게 청구하는 대부분의 작업은 Paddle의 [체크아웃 오버레이 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)을 통한 "체크아웃"을 사용하거나 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 활용하여 수행됩니다.

Paddle를 사용하여 체크아웃 결제를 처리하기 전에 Paddle 체크아웃 설정 대시보드에서 애플리케이션의 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 정의해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 결제

결제 오버레이 위젯을 표시하기 전에 Cashier를 사용하여 결제 세션을 생성해야 합니다. 결제 세션은 수행해야 하는 청구 작업을 결제 위젯에 알려줍니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier에는 `paddle-button` [Blade 컴포넌트](/docs/13.x/blade#components)가 포함되어 있습니다. 결제 세션을 이 컴포넌트에 "prop"로 전달할 수 있습니다. 그런 다음 이 버튼을 클릭하면 Paddle의 결제 위젯이 표시됩니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 Paddle의 기본 스타일을 사용하여 위젯이 표시됩니다. `data-theme='light'` 속성과 같은 [Paddle 지원 속성](https://developer.paddle.com/paddlejs/html-data-attributes)을 컴포넌트에 추가하여 위젯을 사용자 지정할 수 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 결제 위젯은 비동기식입니다. 사용자가 위젯 내에서 구독을 생성하면 Paddle는 애플리케이션 데이터베이스에서 구독 상태를 적절하게 업데이트할 수 있도록 애플리케이션에 웹후크를 보냅니다. 따라서 Paddle의 상태 변경을 수용할 수 있도록 적절하게 [웹후크를 설정](#handling-paddle-webhooks)하는 것이 중요합니다.

> [!WARNING]
> 구독 상태가 변경된 후 해당 웹훅 수신 지연은 일반적으로 최소화되지만, 체크아웃을 완료한 후 사용자의 구독이 즉시 사용 가능하지 않을 수 있다는 점을 고려하여 애플리케이션에서 이를 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃을 수동으로 렌더링

Laravel에 내장된 Blade 컴포넌트를 사용하지 않고 수동으로 오버레이 체크아웃을 렌더링할 수도 있습니다. 시작하려면 [이전 예에서 설명한 대로](#overlay-checkout) 결제 세션을 생성하세요.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

다음으로 Paddle.js를 사용하여 결제를 초기화할 수 있습니다. 이 예에서는 `paddle_button` 클래스가 할당된 링크를 생성합니다. Paddle.js는 이 클래스를 감지하고 링크를 클릭하면 오버레이 체크아웃을 표시합니다.

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

Paddle의 "오버레이" 스타일 체크아웃 위젯을 사용하지 않으려는 경우 Paddle는 위젯을 인라인으로 표시하는 옵션도 제공합니다. 이 접근 방식을 사용하면 체크아웃의 HTML 필드를 조정할 수는 없지만 애플리케이션 내에 위젯을 삽입할 수는 있습니다.

인라인 결제를 쉽게 시작할 수 있도록 Cashier에는 `paddle-checkout` Blade 컴포넌트가 포함되어 있습니다. 시작하려면 [결제 세션을 생성](#overlay-checkout)해야 합니다.

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

인라인 체크아웃 컴포넌트의 높이를 조정하려면 `height` 속성을 Blade 컴포넌트에 전달할 수 있습니다.

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

인라인 체크아웃의 사용자 지정 옵션에 대한 자세한 내용은 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) 및 [사용 가능한 체크아웃 설정](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)을 참조하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 결제를 수동으로 렌더링

Laravel에 내장된 Blade 컴포넌트를 사용하지 않고 인라인 결제를 수동으로 렌더링할 수도 있습니다. 시작하려면 [이전 예에서 설명한 대로](#inline-checkout) 결제 세션을 생성하세요.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

다음으로 Paddle.js를 사용하여 결제를 초기화할 수 있습니다. 이 예에서는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하여 이를 시연합니다. 그러나 자신의 프론트엔드 스택에 맞게 이 예제를 자유롭게 수정할 수 있습니다.

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

때로는 애플리케이션에 계정이 필요하지 않은 사용자를 위해 체크아웃 세션을 생성해야 할 수도 있습니다. 그렇게 하려면 `guest` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

그런 다음 [Paddle 버튼](#overlay-checkout) 또는 [인라인 체크아웃](#inline-checkout) Blade 컴포넌트에 체크아웃 세션을 제공할 수 있습니다.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle를 사용하면 통화당 가격을 맞춤설정할 수 있으므로 기본적으로 국가별로 서로 다른 가격을 구성할 수 있습니다. Cashier Paddle를 사용하면 `previewPrices` 메서드를 사용하여 이러한 가격을 모두 검색할 수 있습니다. 이 메서드는 가격을 검색하려는 가격 ID를 허용합니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

통화는 요청의 IP 주소에 따라 결정됩니다. 그러나 선택적으로 특정 국가를 제공하여 다음에 대한 가격을 검색할 수 있습니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

가격을 검색한 후 원하는 대로 표시할 수 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

소계 가격과 세액을 별도로 표시할 수도 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

자세한 내용은 [가격 미리보기에 관한 Paddle의 API 문서를 확인](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)하세요.

<a name="customer-price-previews"></a>
### 고객 가격 미리보기

사용자가 이미 고객이고 해당 고객에게 적용되는 가격을 표시하려는 경우 고객 인스턴스에서 직접 가격을 검색하여 표시할 수 있습니다.

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

내부적으로 Cashier는 사용자의 고객 ID를 사용하여 해당 통화로 가격을 검색합니다. 예를 들어 미국에 거주하는 사용자에게는 가격이 미국 달러로 표시되고 벨기에 사용자에게는 가격이 유로로 표시됩니다. 일치하는 통화를 찾을 수 없는 경우 제품의 기본 통화가 사용됩니다. Paddle 제어판에서 제품 가격이나 구독 계획의 모든 가격을 맞춤 설정할 수 있습니다.

<a name="price-discounts"></a>
### 할인

할인 후 가격을 표시하도록 선택할 수도 있습니다. `previewPrices` 메서드를 호출할 때 `discount_id` 옵션을 통해 할인 ID를 제공합니다.

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

Cashier를 사용하면 결제 세션을 생성할 때 고객을 위한 몇 가지 유용한 기본값을 정의할 수 있습니다. 이러한 기본값을 설정하면 고객의 이메일 주소와 이름을 미리 입력하여 결제 위젯의 결제 부분으로 즉시 이동할 수 있습니다. 청구 가능한 모델에서 다음 메서드를 재정의하여 이러한 기본값을 설정할 수 있습니다.

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

이러한 기본값은 [체크아웃 세션](#checkout-sessions)을 생성하는 Cashier의 모든 작업에 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 검색

`Cashier::findBillable` 메서드를 사용하여 Paddle 고객 ID로 고객을 검색할 수 있습니다. 이 메서드는 청구 가능한 모델의 인스턴스를 반환합니다.

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성

Occasionally, you may wish to create a Paddle customer without beginning a subscription. `createAsCustomer` 메서드를 사용하여 이 작업을 수행할 수 있습니다.

```php
$customer = $user->createAsCustomer();
```

`Laravel\Paddle\Customer`의 인스턴스가 반환됩니다. Paddle에서 고객이 생성되면 나중에 구독을 시작할 수 있습니다. 추가 [Paddle API에서 지원하는 고객 생성 매개변수](https://developer.paddle.com/api-reference/customers/create-customer)를 전달하기 위해 선택적 `$options` 배열을 제공할 수 있습니다.

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 만들기

구독을 생성하려면 먼저 데이터베이스에서 청구 가능한 모델 인스턴스를 검색하세요. 이 인스턴스는 일반적으로 `App\Models\User` 인스턴스입니다. 모델 인스턴스를 검색한 후에는 `subscribe` 메서드를 사용하여 모델의 체크아웃 세션을 생성할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe` 메서드에 제공된 첫 번째 인수는 사용자가 구독하는 특정 가격입니다. 이 값은 Paddle의 가격 식별자와 일치해야 합니다. `returnTo` 메서드는 사용자가 체크아웃을 성공적으로 완료한 후 리디렉션되는 URL를 허용합니다. `subscribe` 메서드에 전달된 두 번째 인수는 구독의 내부 "유형"이어야 합니다. 애플리케이션이 단일 구독만 제공하는 경우 이를 `default` 또는 `primary`로 호출할 수 있습니다. 이 구독 유형은 내부 애플리케이션 용도로만 사용되며 사용자에게 표시되지 않습니다. 또한 공백이 없어야 하며 구독을 만든 후에는 변경하면 안 됩니다.

`customData` 메서드를 사용하여 구독과 관련된 사용자 지정 메타데이터 배열을 제공할 수도 있습니다.

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

구독 결제 세션이 생성되면 Cashier Paddle에 포함된 `paddle-button` [Blade 컴포넌트](#overlay-checkout)에 결제 세션이 제공될 수 있습니다.

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

사용자가 결제를 완료하면 `subscription_created` 웹훅은 Paddle의 디스패치가 됩니다. Cashier는 이 웹훅을 수신하고 고객을 위한 구독을 설정합니다. 모든 웹훅이 애플리케이션에서 올바르게 수신되고 처리되도록 하려면 [웹훅 처리 설정](#handling-paddle-webhooks)이 제대로 이루어졌는지 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

사용자가 애플리케이션을 구독하면 다양하고 편리한 메서드를 사용하여 구독 상태를 확인할 수 있습니다. 먼저, `subscribed` 메서드는 구독이 현재 평가판 기간 내에 있더라도 사용자에게 유효한 구독이 있는 경우 `true`를 반환합니다.

```php
if ($user->subscribed()) {
    // ...
}
```

애플리케이션이 여러 구독을 제공하는 경우 `subscribed` 메서드를 호출할 때 구독을 지정할 수 있습니다.

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 또한 [라우트 미들웨어](/docs/13.x/middleware)에 대한 훌륭한 후보가 되어 사용자의 구독 상태에 따라 라우트 및 컨트롤러에 대한 액세스를 필터링할 수 있습니다.

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

사용자가 아직 평가판 기간 내에 있는지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이 메서드는 사용자에게 아직 평가판 기간에 있다는 경고를 표시해야 하는지 결정하는 데 유용할 수 있습니다.

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

`subscribedToPrice` 메서드는 사용자가 주어진 Paddle 가격 ID를 기반으로 특정 요금제에 가입했는지 확인하는 데 사용될 수 있습니다. 이 예에서는 사용자의 `default` 구독이 월별 가격을 적극적으로 구독하고 있는지 확인합니다.

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

`recurring` 메서드는 사용자가 현재 활성 구독 상태이고 더 이상 평가판 기간이나 유예 기간에 있지 않은지 확인하는 데 사용할 수 있습니다.

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태

사용자가 한때 활성 구독자였으나 구독을 취소했는지 확인하려면 `canceled` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

사용자가 구독을 취소했지만 구독이 완전히 만료될 때까지 여전히 '유예 기간'에 있는지 확인할 수도 있습니다. 예를 들어 원래 3월 10일에 만료될 예정이었던 구독을 사용자가 3월 5일에 취소한 경우 사용자는 3월 10일까지 '유예 기간'을 유지하게 됩니다. 또한 이 시간 동안 `subscribed` 메서드는 계속해서 `true`를 반환합니다.

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체 상태

구독 결제에 실패하면 `past_due`로 표시됩니다. 구독이 이 상태이면 고객이 결제 정보를 업데이트할 때까지 활성화되지 않습니다. 구독 인스턴스에서 `pastDue` 메서드를 사용하여 구독 기한이 지났는지 확인할 수 있습니다.

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

구독 기한이 연체된 경우 사용자에게 [결제 정보를 업데이트](#updating-payment-information)하도록 안내해야 합니다.

`past_due`인 구독이 여전히 유효한 것으로 간주되도록 하려면 Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 `AppServiceProvider`의 `register` 메서드에서 호출되어야 합니다.

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
> 구독이 `past_due` 상태인 경우 결제 정보가 업데이트될 때까지 변경할 수 없습니다. 따라서 구독이 `past_due` 상태에 있을 때 `swap` 및 `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 범위

대부분의 구독 상태는 쿼리 범위로도 사용할 수 있으므로 특정 상태에 있는 구독에 대해 데이터베이스를 쉽게 쿼리할 수 있습니다.

```php
// Get all valid subscriptions...
$subscriptions = Subscription::query()->valid()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 범위의 전체 목록은 아래에서 확인할 수 있습니다.

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
### 구독 단일 요금

구독 단일 요금을 사용하면 구독에 추가로 일회성 요금을 구독자에게 청구할 수 있습니다. `charge` 메서드를 호출할 때 하나 이상의 가격 ID를 제공해야 합니다.

```php
// Charge a single price...
$response = $user->subscription()->charge('pri_123');

// Charge multiple prices at once...
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge` 메서드는 구독의 다음 청구 간격까지 실제로 고객에게 요금을 청구하지 않습니다. 고객에게 즉시 비용을 청구하려면 대신 `chargeAndInvoice` 메서드를 사용할 수 있습니다.

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle는 항상 구독당 결제 수단을 저장합니다. 구독에 대한 기본 결제 방법을 업데이트하려면 구독 모델에서 `redirectToUpdatePaymentMethod` 메서드를 사용하여 고객을 Paddle의 호스팅 결제 방법 업데이트 페이지로 리디렉션해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

사용자가 정보 업데이트를 마치면 `subscription_updated` 웹후크가 디스패치 by Paddle가 되고 구독 세부정보가 애플리케이션 데이터베이스에서 업데이트됩니다.

<a name="changing-plans"></a>
### 계획 변경

사용자가 애플리케이션을 구독한 후 때때로 새 구독 계획으로 변경하고 싶을 수도 있습니다. 사용자의 구독 계획을 업데이트하려면 Paddle 가격 식별자를 구독의 `swap` 메서드에 전달해야 합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

요금제를 바꾸고 다음 청구 주기를 기다리지 않고 즉시 사용자에게 청구하려면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 비례 배분

기본적으로 Paddle는 요금제 간 전환 시 요금을 비례 배분합니다. `noProrate` 메서드를 사용하면 요금을 비례 배분하지 않고 구독을 업데이트할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

비례 배분 및 송장 고객을 즉시 비활성화하려면 `noProrate`와 함께 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

또는 구독 변경에 대해 고객에게 비용을 청구하지 않으려면 `doNotBill` 메서드를 활용할 수 있습니다.

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

Paddle의 비례 배분 정책에 대한 자세한 내용은 Paddle의 [배분 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참조하세요.

<a name="subscription-quantity"></a>
### 구독 수량

때때로 구독은 "수량"의 ​​영향을 받습니다. 예를 들어 프로젝트 관리 애플리케이션은 프로젝트당 월 10달러를 청구할 수 있습니다. 구독 수량을 쉽게 늘리거나 줄이려면 `incrementQuantity` 및 `decrementQuantity` 메서드를 사용하세요.

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription()->decrementQuantity(5);
```

또는 `updateQuantity` 메서드를 사용하여 특정 수량을 설정할 수도 있습니다.

```php
$user->subscription()->updateQuantity(10);
```

`noProrate` 메서드를 사용하면 요금을 비례배분하지 않고 구독 수량을 업데이트할 수 있습니다.

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 제품이 포함된 구독 수량

구독이 [여러 제품에 대한 구독](#subscriptions-with-multiple-products)인 경우 수량을 늘리거나 줄이려는 가격의 ID를 증가/감소 메서드의 두 번째 인수로 전달해야 합니다.

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 제품이 포함된 구독

[여러 제품이 포함된 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)을 사용하면 단일 구독에 여러 결제 제품을 할당할 수 있습니다. 예를 들어, 기본 구독 가격이 월 10달러이지만 추가 월 15달러에 실시간 채팅 추가 기능 제품을 제공하는 고객 서비스 "헬프데스크" 애플리케이션을 구축한다고 가정해 보겠습니다.

구독 결제 세션을 생성할 때 가격 배열을 `subscribe` 메서드의 첫 번째 인수로 전달하여 특정 구독에 대해 여러 제품을 지정할 수 있습니다.

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

위의 예에서 고객은 `default` 구독에 두 가지 가격을 첨부하게 됩니다. 두 가격 모두 해당 청구 간격에 따라 청구됩니다. 필요한 경우 각 가격의 특정 수량을 나타내기 위해 키/값 쌍의 연관 배열을 전달할 수 있습니다.

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 다른 가격을 추가하려면 구독의 `swap` 메서드를 사용해야 합니다. `swap` 메서드를 호출할 때 구독의 현재 가격과 수량도 포함해야 합니다.

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

위의 예에서는 새 가격을 추가하지만 다음 청구 주기까지 고객에게 해당 가격이 청구되지 않습니다. 고객에게 즉시 비용을 청구하려면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

`swap` 메서드를 사용하고 제거하려는 가격을 생략하여 구독에서 가격을 제거할 수 있습니다.

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독의 마지막 가격은 제거할 수 없습니다. 대신 구독을 취소하면 됩니다.

<a name="multiple-subscriptions"></a>
### 다중 구독

Paddle를 사용하면 고객이 동시에 여러 구독을 가질 수 있습니다. 예를 들어 수영 구독과 역도 구독을 제공하는 체육관을 운영할 수 있으며 각 구독마다 가격이 다를 수 있습니다. 물론 고객은 둘 중 하나 또는 두 가지 요금제 모두에 가입할 수 있어야 합니다.

애플리케이션이 구독을 생성할 때 구독 유형을 `subscribe` 메서드에 두 번째 인수로 제공할 수 있습니다. 유형은 사용자가 시작하는 구독 유형을 나타내는 문자열일 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

이 예에서는 고객을 위해 월간 수영 구독을 시작했습니다. 그러나 나중에 연간 구독으로 전환할 수도 있습니다. 고객의 구독을 조정할 때 `swimming` 구독의 가격을 간단히 교환할 수 있습니다.

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

물론 구독을 완전히 취소할 수도 있습니다.

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시중지

구독을 일시 중지하려면 사용자 구독에서 `pause` 메서드를 호출하세요.

```php
$user->subscription()->pause();
```

구독이 일시 중지되면 Cashier는 데이터베이스에 `paused_at` 열을 자동으로 설정합니다. 이 열은 `paused` 메서드가 `true` 반환을 시작해야 하는 시기를 결정하는 데 사용됩니다. 예를 들어 고객이 3월 1일에 구독을 일시 중지했지만 구독이 3월 5일까지 반복되도록 예약되지 않은 경우 `paused` 메서드는 3월 5일까지 `false`를 계속 반환합니다. 이는 일반적으로 사용자가 청구 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있기 때문입니다.

기본적으로 일시 중지는 다음 청구 간격에 발생하므로 고객은 지불한 기간의 나머지 부분을 사용할 수 있습니다. 구독을 즉시 일시 중지하려면 `pauseNow` 메서드를 사용하세요:

```php
$user->subscription()->pauseNow();
```

`pauseUntil` 메서드를 사용하면 특정 시점까지 구독을 일시 중지할 수 있습니다.

```php
$user->subscription()->pauseUntil(now()->plus(months: 1));
```

또는 `pauseNowUntil` 메서드를 사용하여 특정 시점까지 구독을 즉시 일시 중지할 수 있습니다.

```php
$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```

`onPausedGracePeriod` 메서드를 사용하여 사용자가 구독을 일시중지했지만 여전히 '유예 기간'에 있는지 확인할 수 있습니다.

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
> 일시중지된 구독은 수정할 수 없습니다. 다른 플랜으로 교체하거나 수량을 업데이트하려면 먼저 구독을 재개해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 사용자 구독에서 `cancel` 메서드를 호출하세요.

```php
$user->subscription()->cancel();
```

구독이 취소되면 Cashier는 데이터베이스에 `ends_at` 열을 자동으로 설정합니다. 이 열은 `subscribed` 메서드가 `false` 반환을 시작해야 하는 시기를 결정하는 데 사용됩니다. 예를 들어 고객이 3월 1일에 구독을 취소했지만 구독이 3월 5일까지 종료될 예정이 아닌 경우 `subscribed` 메서드는 3월 5일까지 `true`를 계속 반환합니다. 이는 일반적으로 사용자가 청구 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있도록 허용되기 때문에 수행됩니다.

`onGracePeriod` 메서드를 사용하여 사용자가 구독을 취소했지만 여전히 "유예 기간"에 있는지 확인할 수 있습니다.

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

구독을 즉시 취소하려면 구독에서 `cancelNow` 메서드를 호출하면 됩니다.

```php
$user->subscription()->cancelNow();
```

유예 기간 동안 구독 취소를 중지하려면 `stopCancelation` 메서드를 호출하면 됩니다.

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> 취소 후에는 Paddle의 구독을 재개할 수 없습니다. 고객이 구독을 재개하려면 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 평가판 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단을 먼저 선택하세요.

결제 방법 정보를 미리 수집하면서 고객에게 평가판 기간을 제공하려면 고객이 구독하는 가격에 대해 Paddle 대시보드에서 평가판 기간을 설정해야 합니다. 그런 다음 정상적으로 결제 세션을 시작합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

애플리케이션이 `subscription_created` 이벤트를 수신하면 Cashier는 애플리케이션 데이터베이스 내의 구독 기록에 평가판 기간 종료 날짜를 설정하고 이 날짜 이후까지 고객에게 청구를 시작하지 않도록 Paddle에 지시합니다.

> [!WARNING]
> 평가판 종료 날짜 이전에 고객의 구독을 취소하지 않으면 평가판이 만료되는 즉시 요금이 청구되므로 사용자에게 평가판 종료 날짜를 알려야 합니다.

사용자 인스턴스의 `onTrial` 메서드를 사용하여 사용자가 평가판 기간 내에 있는지 확인할 수 있습니다.

```php
if ($user->onTrial()) {
    // ...
}
```

기존 평가판이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

사용자가 특정 구독 유형에 대해 평가판을 받고 있는지 확인하려면 `onTrial` 또는 `hasExpiredTrial` 메서드에 유형을 제공할 수 있습니다.

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 수단 없음

사용자의 결제 방법 정보를 미리 수집하지 않고 평가판 기간을 제공하려는 경우 사용자에게 첨부된 고객 기록의 `trial_ends_at` 열을 원하는 평가판 종료 날짜로 설정하면 됩니다. 이는 일반적으로 사용자 등록 중에 수행됩니다.

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->plus(days: 10)
]);
```

Cashier는 이러한 유형의 평가판을 "일반 평가판"이라고 부릅니다. 기존 구독에 연결되어 있지 않기 때문입니다. `User` 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 값을 지나지 않은 경우 `true`를 반환합니다.

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

사용자를 위한 실제 구독을 생성할 준비가 되면 평소처럼 `subscribe` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

사용자의 평가판 종료 날짜를 검색하려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 평가판을 사용 중인 경우 Carbon 날짜 인스턴스를 반환하고 그렇지 않은 경우 `null`를 반환합니다. 기본 구독이 아닌 특정 구독에 대한 평가판 종료 날짜를 확인하려는 경우 선택적 구독 유형 매개변수를 전달할 수도 있습니다.

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

사용자가 "일반" 평가판 기간 내에 있고 아직 실제 구독을 생성하지 않았는지 구체적으로 알고 싶다면 `onGenericTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extend-or-activate-a-trial"></a>
### 평가판 연장 또는 활성화

`extendTrial` 메서드를 호출하고 평가판이 종료되어야 하는 시점을 지정하여 구독의 기존 평가판 기간을 연장할 수 있습니다.

```php
$user->subscription()->extendTrial(now()->plus(days: 5));
```

또는 구독에서 `activate` 메서드를 호출하여 평가판을 종료하여 구독을 즉시 활성화할 수 있습니다.

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리 (Handling Paddle Webhooks)

Paddle는 웹후크를 통해 다양한 이벤트를 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier의 웹훅 ​​컨트롤러를 가리키는 라우트는 Cashier 서비스 프로바이더에 의해 등록됩니다. 이 컨트롤러는 들어오는 모든 웹훅 요청을 처리합니다.

기본적으로 이 컨트롤러는 청구 실패 횟수가 너무 많은 구독 취소, 구독 업데이트 및 결제 방법 변경을 자동으로 처리합니다. 그러나 곧 알게 되겠지만 이 컨트롤러를 확장하여 원하는 Paddle 웹훅 이벤트를 처리할 수 있습니다.

애플리케이션이 Paddle 웹후크를 처리할 수 있도록 하려면 [Paddle 제어판에서 웹후크 URL를 구성](https://vendors.paddle.com/notifications-v2)해야 합니다. 기본적으로 Cashier의 웹훅 ​​컨트롤러는 `/paddle/webhook` URL 경로에 응답합니다. Paddle 제어판에서 활성화해야 하는 모든 웹후크의 전체 목록은 다음과 같습니다.

- 고객이 업데이트됨
- 거래 완료
- 거래가 업데이트되었습니다.
- 구독이 생성되었습니다.
- 구독이 업데이트되었습니다.
- 구독이 일시중지됨
- 구독이 취소되었습니다

> [!WARNING]
> Cashier에 포함된 [웹훅 서명 확인](/docs/13.x/cashier-paddle#verifying-webhook-signatures) 미들웨어를 사용하여 들어오는 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅 및 CSRF 보호

Paddle 웹후크는 Laravel의 [CSRF 보호](/docs/13.x/csrf)를 우회해야 하므로 Laravel가 수신 Paddle 웹후크에 대해 CSRF 토큰을 확인하려고 시도하지 않도록 해야 합니다. 이를 달성하려면 애플리케이션의 `bootstrap/app.php` 파일의 CSRF 보호에서 `paddle/*`를 제외해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 웹훅 및 로컬 개발

Paddle가 로컬 개발 중에 애플리케이션 웹후크를 보낼 수 있으려면 [Ngrok](https://ngrok.com/) 또는 [Expose](https://expose.dev/docs/introduction)와 같은 사이트 공유 서비스를 통해 애플리케이션을 노출해야 합니다. [Laravel Sail](/docs/13.x/sail)을 사용하여 로컬에서 애플리케이션을 개발하는 경우 Sail의 [사이트 공유 명령](/docs/13.x/sail#sharing-your-site)을 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 청구 실패 및 기타 일반적인 Paddle 웹후크에 대한 구독 취소를 자동으로 처리합니다. 그러나 처리하고 싶은 추가 웹훅 이벤트가 있는 경우 Cashier의 디스패치인 다음 이벤트를 청취하여 처리할 수 있습니다.

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅의 전체 페이로드를 포함합니다. 예를 들어, `transaction.billed` 웹훅을 처리하려는 경우 이벤트를 처리할 [리스너](/docs/13.x/events#defining-listeners)를 등록할 수 있습니다.

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

Cashier는 수신된 웹훅 유형 전용 이벤트도 내보냅니다. Paddle의 전체 페이로드 외에도 청구 가능한 모델, 구독 또는 영수증과 같은 웹훅을 처리하는 데 사용된 관련 모델도 포함되어 있습니다.

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

또한 애플리케이션의 `.env` 파일에서 `CASHIER_WEBHOOK` 환경 변수를 정의하여 기본 내장 웹후크 라우트를 재정의할 수도 있습니다. 이 값은 웹후크 라우트에 대한 전체 URL여야 하며 Paddle 제어판에 설정된 URL와 일치해야 합니다.

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 확인

웹훅을 보호하려면 [Paddle의 웹훅 ​​서명](https://developer.paddle.com/webhooks/signature-verification)을 사용할 수 있습니다. 편의를 위해 Cashier에는 들어오는 Paddle 웹훅 요청이 유효한지 확인하는 미들웨어가 자동으로 포함됩니다.

웹훅 확인을 활성화하려면 `PADDLE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 정의되어 있는지 확인하세요. 웹훅 비밀은 Paddle 계정 대시보드에서 검색할 수 있습니다.

<a name="single-charges"></a>
## 단일 요금 (Single Charges)

<a name="charging-for-products"></a>
### 제품 충전

고객을 위한 제품 구매를 시작하려면 청구 가능한 모델 인스턴스에서 `checkout` 메서드를 사용하여 구매에 대한 결제 세션을 생성할 수 있습니다. `checkout` 메서드는 하나 이상의 가격 ID를 허용합니다. 필요한 경우 구매하는 제품의 수량을 제공하기 위해 연관 배열을 사용할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

결제 세션을 생성한 후 Cashier가 제공한 `paddle-button` [Blade 컴포넌트](#overlay-checkout)를 사용하여 사용자가 Paddle 결제 위젯을 뷰하고 구매를 완료할 수 있도록 할 수 있습니다.

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

체크아웃 세션에는 `customData` 메서드가 있어 원하는 사용자 지정 데이터를 기본 트랜잭션 생성에 전달할 수 있습니다. 사용자 지정 데이터를 전달할 때 사용할 수 있는 옵션에 대해 자세히 알아보려면 [Paddle 문서](https://developer.paddle.com/build/transactions/custom-data)를 참조하세요.

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불

환불 거래를 수행하면 환불 금액이 구매 당시 사용된 고객의 결제 수단으로 반환됩니다. Paddle 구매를 환불해야 하는 경우 `Cashier\Paddle\Transaction` 모델에서 `refund` 메서드를 사용할 수 있습니다. 이 메서드는 이유를 첫 번째 인수로 받아들이고, 선택적인 금액을 연관 배열로 사용하여 환불할 하나 이상의 가격 ID를 받아들입니다. `transactions` 메서드를 사용하여 특정 청구 가능 모델에 대한 거래를 검색할 수 있습니다.

예를 들어 `pri_123` 및 `pri_456` 가격에 대한 특정 거래를 환불한다고 가정해 보겠습니다. `pri_123`를 전액 환불하고 싶지만 `pri_456`에 대해서는 2달러만 환불하고 싶습니다.

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // Fully refund this price...
    'pri_456' => 200, // Only partially refund this price...
]);
```

위의 예는 거래의 특정 품목을 환불합니다. 전체 거래를 환불하려면 이유를 입력하세요.

```php
$response = $transaction->refund('Accidental charge');
```

환불에 대한 자세한 내용은 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참조하세요.

> [!WARNING]
> 환불은 완전히 처리되기 전에 항상 Paddle의 승인을 받아야 합니다.

<a name="crediting-transactions"></a>
### 신용 거래

환불과 마찬가지로 거래에 크레딧을 적용할 수도 있습니다. 신용 거래를 통해 고객의 잔액에 자금이 추가되므로 향후 구매에 사용될 수 있습니다. Paddle가 구독 크레딧을 자동으로 처리하므로 크레딧 거래는 수동으로 수집된 거래에 대해서만 수행할 수 있으며 자동으로 수집된 거래(예: 구독)에는 수행할 수 없습니다.

```php
$transaction = $user->transactions()->first();

// Credit a specific line item fully...
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [크레딧에 대한 Paddle 문서 참조](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참조하세요.

> [!WARNING]
> 크레딧은 수동으로 수집한 거래에만 적용할 수 있습니다. 자동으로 수집된 거래는 Paddle 자체에 의해 적립됩니다.

<a name="transactions"></a>
## 거래 (Transactions)

`transactions` 속성을 통해 청구 가능한 모델의 거래 배열을 쉽게 검색할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래는 귀하의 제품 및 구매에 대한 지불을 의미하며 송장과 함께 제공됩니다. 완료된 트랜잭션만 애플리케이션의 데이터베이스에 저장됩니다.

고객의 거래를 나열할 때 거래 인스턴스의 메서드를 사용하여 관련 결제 정보를 표시할 수 있습니다. 예를 들어, 모든 거래를 테이블에 나열하여 사용자가 송장을 쉽게 다운로드할 수 있도록 할 수 있습니다.

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

`download-invoice` 라우트는 다음과 같습니다.

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 과거 및 향후 지불

`lastPayment` 및 `nextPayment` 메서드를 사용하여 반복 구독에 대한 고객의 과거 또는 향후 지불을 검색하고 표시할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

이 두 메서드 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 그러나 `lastPayment`는 거래가 웹후크에 의해 아직 동기화되지 않은 경우 `null`를 반환하고, 청구 주기가 종료되면(예: 구독이 취소된 경우) `nextPayment`는 `null`를 반환합니다.

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트 (Testing)

테스트하는 동안 청구 흐름을 수동으로 테스트하여 통합이 예상대로 작동하는지 확인해야 합니다.

CI 환경 내에서 실행되는 테스트를 포함하여 자동화된 테스트의 경우 [Laravel의 HTTP 클라이언트](/docs/13.x/http-client#testing)를 사용하여 Paddle에 대한 HTTP 호출을 가짜로 만들 수 있습니다. 이는 Paddle의 실제 응답을 테스트하지는 않지만 실제로 Paddle의 API를 호출하지 않고 애플리케이션을 테스트하는 방법을 제공합니다.
