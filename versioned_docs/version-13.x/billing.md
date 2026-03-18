# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [구성](#configuration)
    - [청구 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [통화 구성](#currency-configuration)
    - [세금 구성](#tax-configuration)
    - [로깅](#logging)
    - [사용자 지정 모델 사용](#using-custom-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 업데이트](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [결제 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제수단 저장](#storing-payment-methods)
    - [결제수단 조회](#retrieving-payment-methods)
    - [결제 수단 유무](#payment-method-presence)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 현황 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독수량](#subscription-quantity)
    - [여러 제품에 대한 구독](#subscriptions-with-multiple-products)
    - [복수구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독세](#subscription-taxes)
    - [구독 앵커 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 평가판](#subscription-trials)
    - [결제 수단이 선불인 경우](#with-payment-method-up-front)
    - [선불 결제 수단 없음](#without-payment-method-up-front)
    - [평가판 연장](#extending-trials)
- [Stripe 웹훅 처리](#handling-stripe-webhooks)
    - [웹훅 이벤트 처리기 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 확인](#verifying-webhook-signatures)
- [1회 충전](#single-charges)
    - [간편충전](#simple-charge)
    - [송장으로 청구](#charge-with-invoice)
    - [결제 의도 생성](#creating-payment-intents)
    - [환불 수수료](#refunding-charges)
- [송장](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정된 인보이스](#upcoming-invoices)
    - [구독 송장 미리보기](#previewing-subscription-invoices)
    - [송장 PDF 생성](#generating-invoice-pdfs)
- [결제](#checkout)
    - [제품 결제](#product-checkouts)
    - [1회 충전 결제](#single-charge-checkouts)
    - [구독 결제](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원 결제](#guest-checkouts)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프 세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe's](https://stripe.com) 구독 청구 서비스에 표현력이 풍부하고 유창한 인터페이스를 제공합니다. 작성하기 두려운 상용구 구독 청구 코드를 거의 모두 처리합니다. 기본 구독 관리 외에도 Cashier는 쿠폰, 구독 교환, 구독 "수량", 취소 유예 기간을 처리하고 송장 PDF를 생성할 수도 있습니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md)를 주의 깊게 검토하는 것이 중요합니다.

> [!WARNING]
> 주요 변경을 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 16은 Stripe API 버전 `2025-06-30.basil`를 활용합니다. Stripe API 버전은 새로운 Stripe 기능과 개선 사항을 활용하기 위해 부 릴리스에서 업데이트될 예정입니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 사용하여 Stripe용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier
```

패키지를 설치한 후 `vendor:publish` Artisan 명령을 사용하여 Cashier의 마이그레이션을 게시합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그런 다음 데이터베이스를 마이그레이션합니다.

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 열을 추가합니다. 또한 고객의 모든 구독을 보관하기 위한 새로운 `subscriptions` 테이블과 다양한 가격의 구독을 위한 `subscription_items` 테이블을 생성합니다.

원하는 경우 `vendor:publish` Artisan 명령을 사용하여 Cashier의 구성 파일을 게시할 수도 있습니다.

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 모든 Stripe 이벤트를 올바르게 처리하도록 하려면 [Cashier의 웹훅 ​​처리 구성](#handling-stripe-webhooks)을 기억하세요.

> [!WARNING]
> Stripe에서는 Stripe 식별자를 저장하는 데 사용되는 모든 열에서 대소문자를 구분할 것을 권장합니다. 따라서 MySQL을 사용할 때 `stripe_id` 열의 열 데이터 정렬이 `utf8_bin`로 설정되어 있는지 확인해야 합니다. 이에 대한 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인할 수 있습니다.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="billable-model"></a>
### 청구 가능 모델

Cashier를 사용하기 전에 청구 가능한 모델 정의에 `Billable` 트레이트를 추가하세요. 일반적으로 이는 `App\Models\User` 모델입니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트와 같은 일반적인 청구 작업을 수행할 수 있는 다양한 메서드를 제공합니다.

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 청구 가능한 모델이 Laravel와 함께 제공되는 `App\Models\User` 클래스라고 가정합니다. 이를 변경하려면 `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출되어야 합니다.

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
> Laravel에서 제공한 `App\Models\User` 모델 이외의 모델을 사용하는 경우 대체 모델의 테이블 이름과 일치하도록 제공된 [Cashier 마이그레이션](#installation)를 게시하고 변경해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, 애플리케이션의 `.env` 파일에서 Stripe API 키를 구성해야 합니다. Stripe 제어판에서 Stripe API 키를 검색할 수 있습니다.

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 정의되어 있는지 확인해야 합니다. 이 변수는 들어오는 웹후크가 실제로 Stripe에서 오는지 확인하는 데 사용되기 때문입니다.

<a name="currency-configuration"></a>
### 통화 구성

기본 Cashier 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일 내에서 `CASHIER_CURRENCY` 환경 변수를 설정하여 기본 통화를 변경할 수 있습니다.

```ini
CASHIER_CURRENCY=eur
```

Cashier의 통화를 구성하는 것 외에도 송장에 표시할 화폐 값의 형식을 지정할 때 사용할 로케일을 지정할 수도 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용하여 통화 로케일을 설정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로캘을 사용하려면 `ext-intl` PHP 확장이 서버에 설치 및 구성되어 있는지 확인하세요.

<a name="tax-configuration"></a>
### 세금 구성

[Stripe 세금](https://stripe.com/tax) 덕분에 Stripe에서 생성된 모든 송장에 대한 세금을 자동으로 계산할 수 있습니다. 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하여 자동 세금 계산을 활성화할 수 있습니다.

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

세금 계산이 활성화되면 모든 신규 구독과 생성된 일회성 송장에 자동 세금 계산이 적용됩니다.

이 기능이 제대로 작동하려면 고객 이름, 주소, 세금 ID 등 고객의 청구 세부정보를 Stripe에 동기화해야 합니다. 이를 수행하려면 Cashier에서 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [세금 ID](#tax-ids) 메서드를 사용할 수 있습니다.

<a name="logging"></a>
### 로깅

Cashier를 사용하면 치명적인 Stripe 오류를 기록할 때 사용할 로그 채널을 지정할 수 있습니다. 애플리케이션의 `.env` 파일 내에서 `CASHIER_LOGGER` 환경 변수를 정의하여 로그 채널을 지정할 수 있습니다.

```ini
CASHIER_LOGGER=stack
```

Stripe에 대한 API 호출로 생성된 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 사용자 지정 모델 사용

자신만의 모델을 정의하고 해당 Cashier 모델을 확장하여 Cashier에서 내부적으로 사용되는 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후 `Laravel\Cashier\Cashier` 클래스를 통해 사용자 지정 모델을 사용하도록 Cashier에 지시할 수 있습니다. 일반적으로 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 사용자 지정 모델에 대해 Cashier에 알려야 합니다.

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
## 빠른 시작 (Quickstart)

<a name="quickstart-selling-products"></a>
### 상품 판매

> [!NOTE]
> Stripe Checkout을 활용하기 전에 Stripe 대시보드에서 고정 가격으로 제품을 정의해야 합니다. 또한 [Cashier의 웹훅 ​​처리를 구성](#handling-stripe-webhooks)해야 합니다.

애플리케이션을 통해 제품 및 구독 청구를 제공하는 것은 어려울 수 있습니다. 그러나 Cashier 및 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 현대적이고 강력한 결제 통합을 쉽게 구축할 수 있습니다.

반복되지 않는 단일 청구 제품에 대해 고객에게 비용을 청구하기 위해 Cashier를 활용하여 고객을 Stripe Checkout으로 안내합니다. 여기서 고객은 결제 세부 정보를 제공하고 구매를 확인하게 됩니다. Checkout을 통해 결제가 완료되면 고객은 애플리케이션 내에서 선택한 성공 URL로 리디렉션됩니다.

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

위의 예에서 볼 수 있듯이 Cashier에서 제공하는 `checkout` 메서드를 활용하여 지정된 "가격 식별자"에 대해 고객을 Stripe Checkout으로 리디렉션합니다. Stripe 사용 시 "가격"은 [특정 제품에 대해 정의된 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요한 경우 `checkout` 메서드는 자동으로 Stripe에 고객을 생성하고 해당 Stripe 고객 레코드를 애플리케이션 데이터베이스의 해당 사용자에 연결합니다. 결제 세션을 완료한 후 고객은 고객에게 정보 메시지를 표시할 수 있는 전용 성공 또는 취소 페이지로 리디렉션됩니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 제공

제품을 판매할 때 자체 애플리케이션에서 정의한 `Cart` 및 `Order` 모델을 통해 완료된 주문과 구매한 제품을 추적하는 것이 일반적입니다. 구매를 완료하기 위해 고객을 Stripe Checkout으로 리디렉션할 때 고객이 애플리케이션으로 다시 리디렉션될 때 완료된 구매를 해당 주문과 연결할 수 있도록 기존 주문 식별자를 제공해야 할 수도 있습니다.

이를 달성하기 위해 `metadata` 배열을 `checkout` 메서드에 제공할 수 있습니다. 사용자가 결제 프로세스를 시작할 때 애플리케이션 내에서 보류 중인 `Order`가 생성된다고 가정해 보겠습니다. 이 예의 `Cart` 및 `Order` 모델은 설명을 위한 것이며 Cashier에서 제공되지 않습니다. 자신의 애플리케이션 요구 사항에 따라 다음 개념을 자유롭게 구현할 수 있습니다.

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

위의 예에서 볼 수 있듯이 사용자가 결제 프로세스를 시작하면 장바구니/주문과 관련된 모든 Stripe 가격 식별자를 `checkout` 메서드에 제공합니다. 물론 애플리케이션은 이러한 항목을 "장바구니"와 연결하거나 고객이 항목을 추가할 때 주문하는 일을 담당합니다. 또한 `metadata` 배열을 통해 Stripe Checkout 세션에 주문 ID를 제공합니다. 마지막으로 Checkout 성공 라우트에 `CHECKOUT_SESSION_ID` 템플릿 변수를 추가했습니다. Stripe가 고객을 애플리케이션으로 다시 리디렉션하면 이 템플릿 변수가 자동으로 Checkout 세션 ID로 채워집니다.

다음으로 Checkout 성공 라우트를 구축해 보겠습니다. Stripe 체크아웃을 통해 구매가 완료된 후 사용자가 리디렉션되는 라우트입니다. 이 라우트 내에서 제공된 메타 데이터에 액세스하고 그에 따라 고객의 주문을 업데이트하기 위해 Stripe Checkout 세션 ID 및 연결된 Stripe Checkout 인스턴스를 검색할 수 있습니다.

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

[체크아웃 세션 개체에 포함된 데이터](https://stripe.com/docs/api/checkout/sessions/object)에 대한 자세한 내용은 Stripe의 설명서를 참조하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]
> Stripe Checkout을 활용하기 전에 Stripe 대시보드에서 고정 가격으로 제품을 정의해야 합니다. 또한 [Cashier의 웹훅 ​​처리를 구성](#handling-stripe-webhooks)해야 합니다.

애플리케이션을 통해 제품 및 구독 청구를 제공하는 것은 어려울 수 있습니다. 그러나 Cashier 및 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 현대적이고 강력한 결제 통합을 쉽게 구축할 수 있습니다.

Cashier 및 Stripe Checkout을 사용하여 구독을 판매하는 방법을 알아보려면 기본 월별(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 요금제를 사용하는 구독 서비스의 간단한 시나리오를 고려해 보겠습니다. 이 두 가지 가격은 Stripe 대시보드의 "기본" 제품(`pro_basic`)으로 그룹화될 수 있습니다. 또한 당사의 구독 서비스에서는 `pro_expert`와 같은 Expert 플랜을 제공할 수도 있습니다.

먼저 고객이 당사 서비스에 가입할 수 있는 방법을 살펴보겠습니다. 물론 고객이 애플리케이션 가격 페이지에서 기본 요금제에 대한 "구독" 버튼을 클릭할 수도 있다고 상상할 수 있습니다. 이 버튼 또는 링크는 선택한 계획에 대한 Stripe 체크아웃 세션을 생성하는 Laravel 라우트로 사용자를 연결해야 합니다.

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

위의 예에서 볼 수 있듯이 고객을 Stripe Checkout 세션으로 리디렉션하여 기본 플랜을 구독할 수 있도록 합니다. 성공적으로 체크아웃하거나 취소한 후 고객은 `checkout` 메서드에 제공한 URL로 다시 리디렉션됩니다. 구독이 실제로 언제 시작되었는지 확인하려면(일부 결제 수단을 처리하는 데 몇 초가 걸리기 때문에) [Cashier의 웹훅 ​​처리 구성](#handling-stripe-webhooks)도 필요합니다.

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
            return redirect('/billing');
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

물론 고객은 구독 계획을 다른 제품이나 "계층"으로 변경하기를 원할 수도 있습니다. 이를 허용하는 가장 쉬운 방법은 고객을 Stripe의 [고객 청구 포털](https://stripe.com/docs/no-code/customer-portal)로 안내하는 것입니다. 이 포털에서는 고객이 송장을 다운로드하고, 결제 수단을 업데이트하고, 구독 요금제를 변경할 수 있는 호스팅된 사용자 인터페이스를 제공합니다.

먼저, 청구 포털 세션을 시작하는 데 활용할 Laravel 라우트로 사용자를 안내하는 링크나 버튼을 애플리케이션 내에서 정의합니다.

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

다음으로, Stripe 고객 청구 포털 세션을 시작하고 사용자를 포털로 리디렉션하는 라우트를 정의해 보겠습니다. `redirectToBillingPortal` 메서드는 포털을 종료할 때 사용자가 반환되어야 하는 URL를 허용합니다.

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 웹훅 ​​처리를 구성한 한, Cashier는 Stripe에서 들어오는 웹훅을 검사하여 자동으로 애플리케이션의 계산원 관련 데이터베이스 테이블을 동기화된 상태로 유지합니다. 예를 들어 사용자가 Stripe의 고객 청구 포털을 통해 구독을 취소하면 Cashier는 해당 웹후크를 수신하고 애플리케이션 데이터베이스에서 구독을 "취소됨"으로 표시합니다.

<a name="customers"></a>
## 고객 (Customers)

<a name="retrieving-customers"></a>
### 고객 검색

`Cashier::findBillable` 메서드를 사용하여 Stripe ID로 고객을 검색할 수 있습니다. 이 메서드는 청구 가능한 모델의 인스턴스를 반환합니다.

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성

경우에 따라 구독을 시작하지 않고 Stripe 고객을 생성하고 싶을 수 있습니다. `createAsStripeCustomer` 메서드를 사용하여 이 작업을 수행할 수 있습니다.

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

Stripe에서 고객이 생성되면 나중에 구독을 시작할 수 있습니다. 추가 [Stripe API에서 지원하는 고객 생성 매개변수](https://stripe.com/docs/api/customers/create)를 전달하기 위해 선택적 `$options` 배열을 제공할 수 있습니다.

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

청구 가능한 모델에 대해 Stripe 고객 개체를 반환하려는 경우 `asStripeCustomer` 메서드를 사용할 수 있습니다.

```php
$stripeCustomer = $user->asStripeCustomer();
```

지정된 청구 가능 모델에 대한 Stripe 고객 개체를 검색하고 싶지만 청구 가능 모델이 이미 Stripe 내의 고객인지 확실하지 않은 경우 `createOrGetStripeCustomer` 메서드를 사용할 수 있습니다. 이 메서드는 아직 존재하지 않는 경우 Stripe에 새 고객을 생성합니다.

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 업데이트

경우에 따라 Stripe 고객에게 추가 정보를 직접 업데이트하고 싶을 수도 있습니다. `updateStripeCustomer` 메서드를 사용하여 이 작업을 수행할 수 있습니다. 이 메서드는 [Stripe API에서 지원하는 고객 업데이트 옵션](https://stripe.com/docs/api/customers/update) 배열을 허용합니다.

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액

Stripe를 사용하면 고객의 "잔액"을 입금하거나 출금할 수 있습니다. 나중에 이 잔액은 새 송장에 기입되거나 차감됩니다. 고객의 총 잔액을 확인하려면 청구 가능한 모델에서 사용할 수 있는 `balance` 메서드를 사용할 수 있습니다. `balance` 메서드는 고객의 통화 잔액을 형식화된 문자열 표현으로 반환합니다.

```php
$balance = $user->balance();
```

고객의 잔액을 적립하려면 `creditBalance` 메서드에 값을 제공할 수 있습니다. 원하는 경우 설명을 제공할 수도 있습니다.

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

`debitBalance` 메서드에 값을 제공하면 고객 잔액이 인출됩니다.

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

`applyBalance` 메서드는 고객을 위한 새로운 고객 잔액 거래를 생성합니다. `balanceTransactions` 메서드를 사용하여 이러한 거래 기록을 검색할 수 있습니다. 이는 고객이 검토할 대변 및 차변 로그를 제공하는 데 유용할 수 있습니다.

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
### 세금 ID

Cashier는 고객의 세금 ID를 관리하는 쉬운 방법을 제공합니다. 예를 들어, `taxIds` 메서드를 사용하여 고객에게 컬렉션으로 할당된 모든 [세금 ID](https://stripe.com/docs/api/customer_tax_ids/object)를 검색할 수 있습니다.

```php
$taxIds = $user->taxIds();
```

식별자로 고객의 특정 세금 ID를 검색할 수도 있습니다.

```php
$taxId = $user->findTaxId('txi_belgium');
```

유효한 [유형](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) 및 값을 `createTaxId` 메서드에 제공하여 새 세금 ID를 생성할 수 있습니다.

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId` 메서드는 VAT ID를 고객 계정에 즉시 추가합니다. [VAT ID 확인은 Stripe에서도 수행됩니다](https://stripe.com/docs/invoicing/customer/tax-ids#validation); 그러나 이는 비동기 프로세스입니다. `customer.tax_id.updated` 웹훅 이벤트를 구독하고 [VAT ID `verification` 매개변수](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 검사하면 검증 업데이트 알림을 받을 수 있습니다. 웹훅 처리에 대한 자세한 내용은 [웹훅 처리기 정의 문서](#handling-stripe-webhooks)를 참조하세요.

`deleteTaxId` 메서드를 사용하여 세금 ID를 삭제할 수 있습니다.

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### Stripe와 고객 데이터 동기화

일반적으로 애플리케이션 사용자가 이름, 이메일 주소 또는 Stripe에 저장되어 있는 기타 정보를 업데이트하는 경우 Stripe에 업데이트 내용을 알려야 합니다. 이렇게 하면 Stripe의 정보 사본이 귀하의 애플리케이션 정보와 동기화됩니다.

이를 자동화하려면 모델의 `updated` 이벤트에 반응하는 청구 가능한 모델에 이벤트 리스너를 정의할 수 있습니다. 그런 다음 이벤트 리스너 내에서 모델의 `syncStripeCustomerDetails` 메서드를 호출할 수 있습니다.

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

이제 고객 모델이 업데이트될 때마다 해당 정보가 Stripe와 동기화됩니다. 편의를 위해 Cashier는 고객을 처음 생성할 때 고객 정보를 Stripe와 자동으로 동기화합니다.

Cashier에서 제공하는 다양한 메서드를 재정의하여 고객 정보를 Stripe에 동기화하는 데 사용되는 열을 사용자 지정할 수 있습니다. 예를 들어, Cashier가 고객 정보를 Stripe에 동기화할 때 고객의 "이름"으로 간주되어야 하는 속성을 사용자 지정하기 위해 `stripeName` 메서드를 재정의할 수 있습니다.

```php
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

마찬가지로 `stripeEmail`, `stripePhone`(최대 20자), `stripeAddress` 및 `stripePreferredLocales` 메서드를 재정의할 수 있습니다. 이러한 메서드는 [Stripe 고객 개체 업데이트](https://stripe.com/docs/api/customers/update) 시 해당 고객 매개변수에 정보를 동기화합니다. 고객 정보 동기화 프로세스를 완전히 제어하려면 `syncStripeCustomerDetails` 메서드를 재정의할 수 있습니다.

<a name="billing-portal"></a>
### 청구 포털

Stripe는 고객이 구독, 결제 수단 및 청구 내역을 뷰 관리할 수 있도록 [청구 포털을 설정하는 쉬운 방법](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 컨트롤러 또는 라우트에서 청구 가능한 모델에 대해 `redirectToBillingPortal` 메서드를 호출하여 사용자를 청구 포털로 리디렉션할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

기본적으로 사용자가 구독 관리를 마치면 Stripe 청구 포털 내의 링크를 통해 애플리케이션의 `home` 라우트로 돌아갈 수 있습니다. URL를 `redirectToBillingPortal` 메서드에 인수로 전달하여 사용자가 반환해야 하는 사용자 지정 URL를 제공할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

HTTP 리디렉션 응답을 생성하지 않고 청구 포털에 URL를 생성하려는 경우 `billingPortalUrl` 메서드를 호출할 수 있습니다.

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 결제 수단 (Payment Methods)

<a name="storing-payment-methods"></a>
### 결제 수단 저장

Stripe를 사용하여 구독을 생성하거나 "일회성" 청구를 수행하려면 결제 수단을 저장하고 Stripe에서 해당 식별자를 검색해야 합니다. 이를 달성하는 데 사용되는 접근 방식은 구독 또는 단일 청구에 대한 결제 수단을 사용할지 여부에 따라 다르므로 아래에서 두 가지를 모두 검토하겠습니다.

<a name="payment-methods-for-subscriptions"></a>
#### 구독 결제 수단

나중에 구독을 통해 사용할 수 있도록 고객의 신용 카드 정보를 저장할 때 Stripe "설정 의도" API를 사용하여 고객의 결제 수단 세부 정보를 안전하게 수집해야 합니다. "설정 의도"는 Stripe에 고객의 결제 수단으로 요금을 청구하려는 의도를 나타냅니다. Cashier의 `Billable` 트레이트에는 새로운 설정 의도를 쉽게 생성할 수 있는 `createSetupIntent` 메서드가 포함되어 있습니다. 고객의 결제 수단 세부정보를 수집하는 양식을 렌더링하는 라우트 또는 컨트롤러에서 이 메서드를 호출해야 합니다.

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

설정 인텐트를 생성하여 뷰에 전달한 후에는 결제 수단을 수집할 요소에 해당 비밀 정보를 첨부해야 합니다. 예를 들어 다음 "결제 수단 업데이트" 양식을 고려해 보세요.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

다음으로, Stripe.js 라이브러리를 사용하여 [Stripe 요소](https://stripe.com/docs/stripe-js)를 양식에 첨부하고 고객의 결제 세부정보를 안전하게 수집할 수 있습니다.

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

다음으로, 카드를 확인하고 [Stripe의 `confirmCardSetup` 메서드](https://stripe.com/docs/js/setup_intents/confirm_card_setup)을 사용하여 Stripe에서 안전한 "결제 수단 식별자"를 검색할 수 있습니다.

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

Stripe에서 카드를 확인한 후 결과 `setupIntent.payment_method` 식별자를 Laravel 애플리케이션에 전달하여 고객에게 연결할 수 있습니다. 결제 수단은 [새 결제 수단으로 추가](#adding-payment-methods)하거나 [기본 결제 수단 업데이트에 사용](#updating-the-default-payment-method)할 수 있습니다. 또한 결제 수단 식별자를 즉시 ​​사용하여 [새 구독을 생성](#creating-subscriptions)할 수도 있습니다.

> [!NOTE]
> 설정 의도 및 고객 결제 세부정보 수집에 대한 자세한 내용을 보려면 [Stripe에서 제공한 개요를 검토](https://stripe.com/docs/payments/save-and-reuse#php)하세요.

<a name="payment-methods-for-single-charges"></a>
#### 단일 청구에 대한 결제 수단

물론 고객의 결제 수단에 대해 단일 요금을 청구하는 경우 결제 수단 식별자는 한 번만 사용하면 됩니다. Stripe 제한으로 인해 단일 청구에 대해 고객의 저장된 기본 결제 수단을 사용할 수 없습니다. 고객이 Stripe.js 라이브러리를 사용하여 결제 수단 세부정보를 입력할 수 있도록 허용해야 합니다. 예를 들어 다음 형식을 고려해보세요.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

이러한 양식을 정의한 후 Stripe.js 라이브러리를 사용하여 [Stripe 요소](https://stripe.com/docs/stripe-js)를 양식에 첨부하고 고객의 결제 세부정보를 안전하게 수집할 수 있습니다.

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

다음으로, 카드를 확인하고 [Stripe의 `createPaymentMethod` 메서드](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method)을 사용하여 Stripe에서 안전한 "결제 수단 식별자"를 검색할 수 있습니다.

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

카드가 성공적으로 인증되면 `paymentMethod.id`를 Laravel 애플리케이션에 전달하고 [1회 청구](#simple-charge)를 처리할 수 있습니다.

<a name="retrieving-payment-methods"></a>
### 결제 수단 조회

청구 가능한 모델 인스턴스의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다.

```php
$paymentMethods = $user->paymentMethods();
```

기본적으로 이 메서드는 모든 유형의 결제 수단을 반환합니다. 특정 유형의 결제 수단을 검색하려면 `type`를 메서드에 대한 인수로 전달할 수 있습니다.

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

고객의 기본 결제 수단을 검색하려면 `defaultPaymentMethod` 메서드를 사용할 수 있습니다.

```php
$paymentMethod = $user->defaultPaymentMethod();
```

`findPaymentMethod` 메서드를 사용하여 청구 가능한 모델에 연결된 특정 결제 수단을 검색할 수 있습니다.

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
### 결제 수단 존재

청구 가능한 모델의 계정에 기본 결제 수단이 연결되어 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 호출하세요.

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

`hasPaymentMethod` 메서드를 사용하여 청구 가능한 모델의 계정에 하나 이상의 결제 수단이 연결되어 있는지 확인할 수 있습니다.

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```

이 메서드는 청구 가능한 모델에 결제 수단이 있는지 확인합니다. 모델에 대한 특정 유형의 결제 수단이 존재하는지 확인하려면 `type`를 메서드에 대한 인수로 전달할 수 있습니다.

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 업데이트

`updateDefaultPaymentMethod` 메서드는 고객의 기본 결제 수단 정보를 업데이트하는 데 사용될 수 있습니다. 이 메서드는 Stripe 결제 수단 식별자를 허용하고 새 결제 수단을 기본 청구 결제 수단으로 할당합니다.

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

기본 결제 수단 정보를 Stripe의 고객 기본 결제 수단 정보와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용할 수 있습니다.

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 고객의 기본 결제 수단은 송장 발행 및 새 구독 생성에만 사용할 수 있습니다. Stripe의 제한으로 인해 단일 충전에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
### 결제 수단 추가

새 결제 수단을 추가하려면 청구 가능한 모델에서 `addPaymentMethod` 메서드를 호출하여 결제 수단 식별자를 전달하면 됩니다.

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 식별자를 검색하는 방법을 알아보려면 [결제 수단 저장 문서](#storing-payment-methods)를 검토하세요.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제

결제 수단을 삭제하려면 삭제하려는 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```php
$paymentMethod->delete();
```

`deletePaymentMethod` 메서드는 청구 가능한 모델에서 특정 결제 수단을 삭제합니다.

```php
$user->deletePaymentMethod('pm_visa');
```

`deletePaymentMethods` 메서드는 청구 가능한 모델에 대한 모든 결제 수단 정보를 삭제합니다.

```php
$user->deletePaymentMethods();
```

기본적으로 이 메서드는 모든 유형의 결제 수단을 삭제합니다. 특정 유형의 결제 수단을 삭제하려면 `type`를 메서드에 대한 인수로 전달할 수 있습니다.

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 사용자가 활성 구독을 갖고 있는 경우 애플리케이션은 사용자가 기본 결제 수단을 삭제하도록 허용해서는 안 됩니다.

<a name="subscriptions"></a>
## 구독 (Subscriptions)

구독은 고객에 대한 반복 결제를 설정하는 방법을 제공합니다. Cashier에서 관리하는 Stripe 구독은 다양한 구독 가격, 구독 수량, 평가판 등에 대한 지원을 제공합니다.

<a name="creating-subscriptions"></a>
### 구독 만들기

구독을 생성하려면 먼저 청구 가능한 모델의 인스턴스를 검색하세요. 이는 일반적으로 `App\Models\User`의 인스턴스입니다. 모델 인스턴스를 검색한 후에는 `newSubscription` 메서드를 사용하여 모델 구독을 생성할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

`newSubscription` 메서드에 전달된 첫 번째 인수는 구독의 내부 유형이어야 합니다. 애플리케이션이 단일 구독만 제공하는 경우 이를 `default` 또는 `primary`로 호출할 수 있습니다. 이 구독 유형은 내부 애플리케이션 용도로만 사용되며 사용자에게 표시되지 않습니다. 또한 공백이 없어야 하며 구독을 만든 후에는 변경하면 안 됩니다. 두 번째 인수는 사용자가 구독하는 특정 가격입니다. 이 값은 Stripe의 가격 식별자와 일치해야 합니다.

[Stripe 결제 수단 식별자](#storing-payment-methods) 또는 Stripe `PaymentMethod` 개체를 허용하는 `create` 메서드는 구독을 시작하고 청구 가능한 모델의 Stripe 고객 ID 및 기타 관련 청구 정보로 데이터베이스를 업데이트합니다.

> [!WARNING]
> 결제 수단 식별자를 `create` 구독 메서드에 직접 전달하면 사용자의 저장된 결제 수단에도 자동으로 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 송장 이메일을 통해 반복 결제 수집

고객의 반복 결제를 자동으로 수집하는 대신, 반복 결제 기한이 다가올 때마다 고객에게 송장을 이메일로 보내도록 Stripe에 지시할 수 있습니다. 그런 다음 고객은 청구서를 받은 후 수동으로 지불할 수 있습니다. 고객은 송장을 통해 반복 결제를 받을 때 결제 수단을 미리 제공할 필요가 없습니다.

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

구독이 취소되기 전에 고객이 청구서를 지불해야 하는 기간은 `days_until_due` 옵션에 따라 결정됩니다. 기본적으로 이는 30일입니다. 그러나 원하는 경우 이 옵션에 특정 값을 제공할 수 있습니다.

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### 수량

구독을 생성할 때 가격에 특정 [수량](https://stripe.com/docs/billing/subscriptions/quantities)을 설정하려면 구독을 생성하기 전에 구독 빌더에서 `quantity` 메서드를 호출해야 합니다.

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 추가 세부정보

Stripe에서 지원하는 추가 [고객](https://stripe.com/docs/api/customers/create) 또는 [구독](https://stripe.com/docs/api/subscriptions/create) 옵션을 지정하려면 해당 옵션을 `create` 메서드에 두 번째 및 세 번째 인수로 전달하면 됩니다.

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => 'Some extra information.'],
]);
```

<a name="coupons"></a>
#### 쿠폰

구독을 생성할 때 쿠폰을 적용하려면 `withCoupon` 메서드를 사용할 수 있습니다.

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

또는 [Stripe 프로모션 코드](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 적용하려면 `withPromotionCode` 메서드를 사용할 수 있습니다.

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

제공된 프로모션 코드 ID는 고객이 접하는 프로모션 코드가 아니라 프로모션 코드에 할당된 Stripe API ID여야 합니다. 특정 고객 대상 프로모션 코드를 기반으로 프로모션 코드 ID를 찾아야 하는 경우 `findPromotionCode` 메서드를 사용할 수 있습니다.

```php
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

위의 예에서 반환된 `$promotionCode` 개체는 `Laravel\Cashier\PromotionCode`의 인스턴스입니다. 이 클래스는 기본 `Stripe\PromotionCode` 객체를 장식합니다. `coupon` 메서드를 호출하여 프로모션 코드와 관련된 쿠폰을 검색할 수 있습니다.

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

쿠폰 인스턴스를 사용하면 할인 금액과 쿠폰이 고정 할인을 나타내는지 또는 백분율 기반 할인을 나타내는지 여부를 확인할 수 있습니다.

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

현재 고객 또는 구독에 적용되는 할인을 검색할 수도 있습니다.

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

반환된 `Laravel\Cashier\Discount` 인스턴스는 기본 `Stripe\Discount` 개체 인스턴스를 장식합니다. `coupon` 메서드를 호출하여 이 할인과 관련된 쿠폰을 검색할 수 있습니다.

```php
$coupon = $subscription->discount()->coupon();
```

고객이나 구독에 새로운 쿠폰이나 프로모션 코드를 적용하려면 `applyCoupon` 또는 `applyPromotionCode` 메서드를 통해 적용할 수 있습니다.

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

고객용 프로모션 코드가 아닌 프로모션 코드에 할당된 Stripe API ID를 사용해야 한다는 점을 기억하세요. 특정 시점에 하나의 쿠폰 또는 프로모션 코드만 고객 또는 구독에 적용될 수 있습니다.

이 주제에 대한 자세한 내용은 [쿠폰](https://stripe.com/docs/billing/subscriptions/coupons) 및 [프로모션 코드](https://stripe.com/docs/billing/subscriptions/coupons/codes)에 관한 Stripe 문서를 참조하세요.

<a name="adding-subscriptions"></a>
#### 구독 추가

이미 기본 결제 수단을 갖고 있는 고객에게 구독을 추가하려면 구독 빌더에서 `add` 메서드를 호출하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe 대시보드에서 구독 생성

Stripe 대시보드 자체에서 구독을 생성할 수도 있습니다. 이렇게 하면 Cashier는 새로 추가된 구독을 동기화하고 `default` 유형을 할당합니다. 대시보드 생성 구독에 할당된 구독 유형을 사용자 지정하려면 [웹후크 이벤트 핸들러 정의](#defining-webhook-event-handlers)를 참조하세요.

또한 Stripe 대시보드를 통해 한 가지 유형의 구독만 생성할 수 있습니다. 애플리케이션이 서로 다른 유형을 사용하는 여러 구독을 제공하는 경우 Stripe 대시보드를 통해 한 가지 유형의 구독만 추가할 수 있습니다.

마지막으로, 항상 애플리케이션에서 제공하는 구독 유형당 하나의 활성 구독만 추가해야 합니다. 고객이 두 개의 `default` 구독을 가지고 있는 경우 두 구독 모두 애플리케이션의 데이터베이스와 동기화되더라도 가장 최근에 추가된 구독만 Cashier에서 사용됩니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

고객이 애플리케이션을 구독하면 다양하고 편리한 메서드를 사용하여 구독 상태를 쉽게 확인할 수 있습니다. 먼저, 구독이 현재 평가판 기간 내에 있더라도 고객에게 활성 구독이 있는 경우 `subscribed` 메서드는 `true`를 반환합니다. `subscribed` 메서드는 구독 유형을 첫 번째 인수로 승인합니다.

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
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // This user is not a paying customer...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

사용자가 아직 평가판 기간 내에 있는지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이 메서드는 사용자에게 아직 평가판 기간에 있다는 경고를 표시해야 하는지 결정하는 데 유용할 수 있습니다.

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

`subscribedToProduct` 메서드는 주어진 Stripe 제품의 식별자를 기반으로 사용자가 특정 제품에 가입했는지 여부를 결정하는 데 사용될 수 있습니다. Stripe에서 제품은 가격 모음입니다. 이 예에서는 사용자의 `default` 구독이 애플리케이션의 "프리미엄" 제품에 적극적으로 구독되어 있는지 확인합니다. 지정된 Stripe 제품 식별자는 Stripe 대시보드에 있는 제품 식별자 중 하나와 일치해야 합니다.

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

`subscribedToProduct` 메서드에 배열을 전달하면 사용자의 `default` 구독이 애플리케이션의 "기본" 또는 "프리미엄" 제품에 적극적으로 구독되어 있는지 확인할 수 있습니다.

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

`subscribedToPrice` 메서드는 고객의 구독이 주어진 가격 ID에 해당하는지 확인하는 데 사용될 수 있습니다.

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

`recurring` 메서드를 사용하여 사용자가 현재 구독 중이고 더 이상 평가판 기간 내에 있지 않은지 확인할 수 있습니다.

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> 사용자에게 동일한 유형의 구독이 두 개 있는 경우 가장 최근 구독이 항상 `subscription` 메서드에 의해 반환됩니다. 예를 들어, 사용자에게 `default` 유형의 구독 레코드가 두 개 있을 수 있습니다. 그러나 구독 중 하나는 오래되고 만료된 구독이고 다른 하나는 현재 활성 구독일 수 있습니다. 가장 최근 구독은 항상 반환되며 이전 구독은 기록 검토를 위해 데이터베이스에 보관됩니다.

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태

사용자가 한때 활성 구독자였으나 구독을 취소했는지 확인하려면 `canceled` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

사용자가 구독을 취소했지만 구독이 완전히 만료될 때까지 여전히 '유예 기간'에 있는지 확인할 수도 있습니다. 예를 들어 원래 3월 10일에 만료될 예정이었던 구독을 사용자가 3월 5일에 취소한 경우 사용자는 3월 10일까지 '유예 기간'을 유지하게 됩니다. 이 시간 동안 `subscribed` 메서드는 여전히 `true`를 반환합니다.

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

사용자가 구독을 취소했고 더 이상 "유예 기간"이 지나지 않았는지 확인하려면 `ended` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
#### 미완료 및 연체 상태

구독 생성 후 보조 결제 작업이 필요한 경우 구독은 `incomplete`로 표시됩니다. 구독 상태는 Cashier의 `subscriptions` 데이터베이스 테이블의 `stripe_status` 열에 저장됩니다.

마찬가지로, 가격을 교환할 때 보조 결제 작업이 필요한 경우 구독은 `past_due`로 표시됩니다. 귀하의 구독이 이러한 상태 중 하나이면 고객이 결제를 확인할 때까지 활성화되지 않습니다. 구독에 불완전한 결제가 있는지 확인하려면 청구 가능한 모델 또는 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용하여 수행할 수 있습니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

구독에 결제가 완료되지 않은 경우 `latestPayment` 식별자를 전달하여 사용자를 Cashier의 결제 확인 페이지로 안내해야 합니다. 구독 인스턴스에서 사용할 수 있는 `latestPayment` 메서드를 사용하여 이 식별자를 검색할 수 있습니다.

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

`past_due` 또는 `incomplete` 상태에 있을 때 구독이 계속 활성 상태로 간주되도록 하려면 Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 및 `keepIncompleteSubscriptionsActive` 메서드를 사용할 수 있습니다. 일반적으로 이러한 메서드는 `App\Providers\AppServiceProvider`의 `register` 메서드에서 호출되어야 합니다.

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
> 구독이 `incomplete` 상태인 경우 결제가 확인될 때까지 변경할 수 없습니다. 따라서 구독이 `incomplete` 상태에 있을 때 `swap` 및 `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 범위

대부분의 구독 상태는 쿼리 범위로도 사용할 수 있으므로 특정 상태에 있는 구독에 대해 데이터베이스를 쉽게 쿼리할 수 있습니다.

```php
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 범위의 전체 목록은 아래에서 확인할 수 있습니다.

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
### 가격 변경

고객이 애플리케이션을 구독한 후 가끔 새 구독 가격으로 변경하고 싶을 수도 있습니다. 고객을 새 가격으로 교환하려면 Stripe 가격 식별자를 `swap` 메서드에 전달하세요. 가격을 교환할 때 사용자는 이전에 구독을 취소한 경우 구독을 다시 활성화하기를 원한다고 가정합니다. 지정된 가격 식별자는 Stripe 대시보드에서 사용할 수 있는 Stripe 가격 식별자와 일치해야 합니다.

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

고객이 평가판을 사용 중인 경우 평가판 기간이 유지됩니다. 또한 구독에 대한 "수량"이 존재하는 경우 해당 수량도 유지됩니다.

가격을 교환하고 고객이 현재 진행 중인 평가판 기간을 취소하려면 `skipTrial` 메서드를 호출하면 됩니다.

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

가격을 교환하고 다음 청구 주기를 기다리지 않고 즉시 고객에게 청구하려면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 비례 배분

기본적으로 Stripe는 가격을 교환할 때 요금을 비례 배분합니다. `noProrate` 메서드를 사용하면 요금을 비례배분하지 않고 구독 가격을 업데이트할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

구독 비례배분에 대한 자세한 내용은 [Stripe 문서](https://stripe.com/docs/billing/subscriptions/prorations)를 참조하세요.

> [!WARNING]
> `swapAndInvoice` 메서드 이전에 `noProrate` 메서드를 실행하면 비례 배분에 영향을 주지 않습니다. 청구서는 항상 발행됩니다.

<a name="subscription-quantity"></a>
### 구독 수량

때때로 구독은 "수량"의 ​​영향을 받습니다. 예를 들어 프로젝트 관리 애플리케이션은 프로젝트당 월 10달러를 청구할 수 있습니다. `incrementQuantity` 및 `decrementQuantity` 메서드를 사용하여 구독 수량을 쉽게 늘리거나 줄일 수 있습니다.

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

또는 `updateQuantity` 메서드를 사용하여 특정 수량을 설정할 수도 있습니다.

```php
$user->subscription('default')->updateQuantity(10);
```

`noProrate` 메서드를 사용하면 요금을 비례배분하지 않고 구독 수량을 업데이트할 수 있습니다.

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

구독 수량에 대한 자세한 내용은 [Stripe 문서](https://stripe.com/docs/subscriptions/quantities)를 참조하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 제품이 포함된 구독 수량

구독이 [여러 제품에 대한 구독](#subscriptions-with-multiple-products)인 경우 수량을 늘리거나 줄이려는 가격의 ID를 증가/감소 메서드의 두 번째 인수로 전달해야 합니다.

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 제품이 포함된 구독

[여러 제품이 포함된 구독](https://stripe.com/docs/billing/subscriptions/multiple-products)을 사용하면 단일 구독에 여러 결제 제품을 할당할 수 있습니다. 예를 들어, 기본 구독 가격이 월 10달러이지만 추가 월 15달러에 실시간 채팅 추가 기능 제품을 제공하는 고객 서비스 "헬프데스크" 애플리케이션을 구축한다고 가정해 보겠습니다. 여러 제품이 포함된 구독에 대한 정보는 Cashier의 `subscription_items` 데이터베이스 테이블에 저장됩니다.

가격 배열을 `newSubscription` 메서드의 두 번째 인수로 전달하여 특정 구독에 대해 여러 제품을 지정할 수 있습니다.

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

위의 예에서 고객은 `default` 구독에 두 가지 가격을 첨부하게 됩니다. 두 가격 모두 해당 청구 간격에 따라 청구됩니다. 필요한 경우 `quantity` 메서드를 사용하여 각 가격에 대한 특정 수량을 표시할 수 있습니다.

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

기존 구독에 다른 가격을 추가하려면 구독의 `addPrice` 메서드를 호출하면 됩니다.

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

위의 예에서는 새 가격을 추가하고 고객에게 다음 청구 주기에 해당 가격이 청구됩니다. 고객에게 즉시 비용을 청구하려면 `addPriceAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

특정 수량의 가격을 추가하려면 해당 수량을 `addPrice` 또는 `addPriceAndInvoice` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

`removePrice` 메서드를 사용하여 구독에서 가격을 제거할 수 있습니다.

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> 구독의 마지막 가격은 제거할 수 없습니다. 대신 구독을 취소하면 됩니다.

<a name="swapping-prices"></a>
#### 가격 교환

여러 제품이 포함된 구독에 첨부된 가격을 변경할 수도 있습니다. 예를 들어, 고객이 `price_chat` 추가 제품이 포함된 `price_basic` 구독을 가지고 있고 고객을 `price_basic`에서 `price_pro` 가격으로 업그레이드하려고 한다고 가정해 보겠습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

위의 예를 실행하면 `price_basic`가 있는 기본 구독 항목이 삭제되고 `price_chat`가 있는 구독 항목이 유지됩니다. 또한 `price_pro`에 대한 새 구독 항목이 생성됩니다.

키/값 쌍 배열을 `swap` 메서드에 전달하여 구독 항목 옵션을 지정할 수도 있습니다. 예를 들어 구독 가격 수량을 지정해야 할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

구독의 단일 가격을 교환하려면 구독 항목 자체에 `swap` 메서드를 사용하면 됩니다. 이 접근 방식은 구독의 다른 가격에 대한 기존 메타데이터를 모두 보존하려는 경우 특히 유용합니다.

```php
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>
#### 비례배분

기본적으로 Stripe는 여러 제품이 포함된 구독에서 가격을 추가하거나 제거할 때 요금을 비례 배분합니다. 비례배분 없이 가격을 조정하려면 `noProrate` 메서드를 가격 작업에 연결해야 합니다.

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 수량

개별 구독 가격의 수량을 업데이트하려면 가격 ID를 메서드에 추가 인수로 전달하여 [기존 수량 메서드](#subscription-quantity)를 사용하여 업데이트할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 구독에 여러 가격이 있는 경우 `Subscription` 모델의 `stripe_price` 및 `quantity` 속성은 `null`가 됩니다. 개별 가격 속성에 액세스하려면 `Subscription` 모델에서 사용 가능한 `items` 관계를 사용해야 합니다.

<a name="subscription-items"></a>
#### 구독 항목

구독 가격이 여러 개인 경우 데이터베이스의 `subscription_items` 테이블에 여러 구독 "항목"이 저장됩니다. 구독의 `items` 관계를 통해 이러한 항목에 액세스할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

`findItemOrFail` 메서드를 사용하여 특정 가격을 검색할 수도 있습니다.

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### 다중 구독

Stripe를 사용하면 고객이 동시에 여러 구독을 가질 수 있습니다. 예를 들어 수영 구독과 역도 구독을 제공하는 체육관을 운영할 수 있으며 각 구독마다 가격이 다를 수 있습니다. 물론 고객은 둘 중 하나 또는 두 가지 요금제 모두에 가입할 수 있어야 합니다.

애플리케이션이 구독을 생성할 때 `newSubscription` 메서드에 구독 유형을 제공할 수 있습니다. 유형은 사용자가 시작하는 구독 유형을 나타내는 문자열일 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

이 예에서는 고객을 위해 월간 수영 구독을 시작했습니다. 그러나 나중에 연간 구독으로 전환할 수도 있습니다. 고객의 구독을 조정할 때 `swimming` 구독의 가격을 간단히 교환할 수 있습니다.

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

물론 구독을 완전히 취소할 수도 있습니다.

```php
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
### 사용량 기반 청구

[사용량 기반 청구](https://stripe.com/docs/billing/subscriptions/metered-billing)를 사용하면 청구 주기 동안 제품 사용량을 기준으로 고객에게 요금을 청구할 수 있습니다. 예를 들어, 매월 보내는 문자 메시지나 이메일 수를 기준으로 고객에게 요금을 청구할 수 있습니다.

사용량 청구 사용을 시작하려면 먼저 Stripe 대시보드에서 [사용량 기반 청구 모델](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) 및 [미터](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter)를 사용하여 새 제품을 생성해야 합니다. 측정기를 생성한 후 사용량을 보고하고 검색하는 데 필요한 연결된 이벤트 이름과 측정기 ID를 저장합니다. 그런 다음 `meteredPrice` 메서드를 사용하여 측정 가격 ID를 고객 구독에 추가합니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

[Stripe Checkout](#checkout)을 통해 종량제 구독을 시작할 수도 있습니다.

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
#### 보고 사용량

고객이 애플리케이션을 사용할 때 정확한 요금이 청구될 수 있도록 사용량을 Stripe에 보고하게 됩니다. 측정된 이벤트의 사용량을 보고하려면 `Billable` 모델에서 `reportMeterEvent` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

기본적으로 "사용 수량" 1이 청구 기간에 추가됩니다. 또는 특정 양의 "사용량"을 전달하여 청구 기간 동안 고객의 사용량에 추가할 수 있습니다.

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

미터에 대한 고객의 이벤트 요약을 검색하려면 `Billable` 인스턴스의 `meterEventSummaries` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

미터 이벤트 요약에 대한 자세한 내용은 Stripe의 [미터 이벤트 요약 개체 문서](https://docs.stripe.com/api/billing/meter-event_summary/object)를 참조하세요.

[모든 미터를 나열](https://docs.stripe.com/api/billing/meter/list)하려면 `Billable` 인스턴스의 `meters` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>
### 구독세

> [!WARNING]
> 세율을 수동으로 계산하는 대신 [Stripe 세금을 사용하여 자동으로 세금을 계산](#tax-configuration)할 수 있습니다.

사용자가 구독에 대해 지불하는 세율을 지정하려면 청구 가능한 모델에 `taxRates` 메서드를 구현하고 Stripe 세율 ID가 포함된 배열을 반환해야 합니다. [Stripe 대시보드](https://dashboard.stripe.com/test/tax-rates)에서 다음 세율을 정의할 수 있습니다.

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

`taxRates` 메서드를 사용하면 고객별로 세율을 적용할 수 있으며, 이는 여러 국가 및 세율에 걸쳐 있는 사용자 기반에 도움이 될 수 있습니다.

여러 제품이 포함된 구독을 제공하는 경우 청구 가능한 모델에 `priceTaxRates` 메서드를 구현하여 각 가격에 대해 서로 다른 세율을 정의할 수 있습니다.

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
> `taxRates` 메서드는 구독 요금에만 적용됩니다. Cashier를 사용하여 "일회성" 요금을 부과하는 경우 해당 시점에 세율을 수동으로 지정해야 합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화

`taxRates` 메서드에서 반환된 하드 코딩된 세율 ID를 변경하는 경우 사용자의 기존 구독에 대한 세금 설정은 동일하게 유지됩니다. 새로운 `taxRates` 값으로 기존 구독의 세금 값을 업데이트하려면 사용자의 구독 인스턴스에서 `syncTaxRates` 메서드를 호출해야 합니다.

```php
$user->subscription('default')->syncTaxRates();
```

또한 여러 제품의 구독에 대한 항목 세율도 동기화됩니다. 애플리케이션이 여러 제품에 대한 구독을 제공하는 경우 청구 가능한 모델이 [위에서 설명한] `priceTaxRates` 메서드(#subscription-taxes)를 구현하는지 확인해야 합니다.

<a name="tax-exemption"></a>
#### 면세

Cashier는 또한 고객이 면세 대상인지 확인하기 위해 `isNotTaxExempt`, `isTaxExempt` 및 `reverseChargeApplies` 메서드를 제공합니다. 이러한 메서드는 Stripe API를 호출하여 고객의 면세 상태를 확인합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]
> 이러한 메서드는 모든 `Laravel\Cashier\Invoice` 개체에서도 사용할 수 있습니다. 그러나 `Invoice` 객체에서 호출되면 메서드는 송장이 생성될 당시의 면제 상태를 결정합니다.

<a name="subscription-anchor-date"></a>
### 구독 앵커 날짜

기본적으로 청구 주기 기준은 구독이 생성된 날짜이거나 평가판 기간이 사용된 경우 평가판이 종료되는 날짜입니다. 청구 기준일을 수정하려면 `anchorBillingCycleOn` 메서드를 사용하세요.

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

구독 청구 주기 관리에 대한 자세한 내용은 [Stripe 청구 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참조하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 사용자 구독에서 `cancel` 메서드를 호출하세요.

```php
$user->subscription('default')->cancel();
```

구독이 취소되면 Cashier는 `subscriptions` 데이터베이스 테이블에 `ends_at` 열을 자동으로 설정합니다. 이 열은 `subscribed` 메서드가 `false` 반환을 시작해야 하는 시기를 아는 데 사용됩니다.

예를 들어, 고객이 3월 1일에 구독을 취소했지만 구독이 3월 5일까지 종료될 예정이 아닌 경우 `subscribed` 메서드는 3월 5일까지 `true`를 계속 반환합니다. 이는 일반적으로 사용자가 청구 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있도록 허용되기 때문에 수행됩니다.

`onGracePeriod` 메서드를 사용하여 사용자가 구독을 취소했지만 여전히 "유예 기간"에 있는지 확인할 수 있습니다.

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

구독을 즉시 취소하려면 사용자 구독에서 `cancelNow` 메서드를 호출하세요.

```php
$user->subscription('default')->cancelNow();
```

구독을 즉시 취소하고 청구되지 않은 남은 측정 사용량 또는 새/보류 중인 비례 할당 청구 항목에 대해 청구하려면 사용자의 구독에서 `cancelNowAndInvoice` 메서드를 호출하세요.

```php
$user->subscription('default')->cancelNowAndInvoice();
```

특정 시점에 구독을 취소하도록 선택할 수도 있습니다.

```php
$user->subscription('default')->cancelAt(
    now()->plus(days: 10)
);
```

마지막으로, 연결된 사용자 모델을 삭제하기 전에 항상 사용자 구독을 취소해야 합니다.

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
### 구독 재개

고객이 구독을 취소했고 이를 재개하려는 경우 구독에서 `resume` 메서드를 호출할 수 있습니다. 구독을 재개하려면 고객이 '유예 기간' 내에 있어야 합니다.

```php
$user->subscription('default')->resume();
```

고객이 구독을 취소한 다음 구독이 완전히 만료되기 전에 해당 구독을 재개하는 경우 고객에게 즉시 요금이 청구되지 않습니다. 대신 구독이 다시 활성화되고 원래 청구 주기에 따라 비용이 청구됩니다.

<a name="subscription-trials"></a>
## 구독 평가판 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단을 먼저 선택하세요.

결제 수단 정보를 미리 수집하면서 고객에게 평가판 기간을 제공하려면 구독을 생성할 때 `trialDays` 메서드를 사용해야 합니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```

이 메서드는 데이터베이스 내의 구독 기록에 평가 기간 종료 날짜를 설정하고 이 날짜 이후까지 고객에게 청구를 시작하지 않도록 Stripe에 지시합니다. `trialDays` 메서드를 사용하는 경우 Cashier는 Stripe의 가격에 대해 구성된 기본 평가판 기간을 덮어씁니다.

> [!WARNING]
> 평가판 종료 날짜 이전에 고객의 구독을 취소하지 않으면 평가판이 만료되는 즉시 요금이 청구되므로 사용자에게 평가판 종료 날짜를 알려야 합니다.

`trialUntil` 메서드를 사용하면 평가판 기간 종료 시기를 지정하는 `DateTime` 인스턴스를 제공할 수 있습니다.

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->plus(days: 10))
    ->create($paymentMethod);
```

사용자 인스턴스의 `onTrial` 메서드 또는 구독 인스턴스의 `onTrial` 메서드를 사용하여 사용자가 평가판 기간 내에 있는지 확인할 수 있습니다. 아래 두 예는 동일합니다.

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

`endTrial` 메서드를 사용하여 구독 평가판을 즉시 종료할 수 있습니다.

```php
$user->subscription('default')->endTrial();
```

기존 평가판이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe / Cashier에서 평가판 일 정의

Stripe 대시보드에서 가격이 수신되는 평가판 일수를 정의하거나 항상 Cashier를 사용하여 명시적으로 통과하도록 선택할 수 있습니다. Stripe에서 가격의 평가판 날짜를 정의하기로 선택한 경우 과거에 구독이 있었던 고객의 새 구독을 포함하여 새 구독은 `skipTrial()` 메서드를 명시적으로 호출하지 않는 한 항상 평가판 기간을 받게 된다는 점을 알아야 합니다.

<a name="without-payment-method-up-front"></a>
### 결제 수단 없음

사용자의 결제 수단 정보를 미리 수집하지 않고 평가판 기간을 제공하려는 경우 사용자 기록의 `trial_ends_at` 열을 원하는 평가판 종료 날짜로 설정하면 됩니다. 이는 일반적으로 사용자 등록 시 수행됩니다:

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->plus(days: 10),
]);
```

> [!WARNING]
> 청구 가능한 모델 클래스 정의 내에서 `trial_ends_at` 속성에 대해 [날짜 캐스트](/docs/13.x/eloquent-mutators#date-casting)를 추가해야 합니다.

Cashier는 이러한 유형의 평가판을 "일반 평가판"이라고 부릅니다. 기존 구독에 연결되어 있지 않기 때문입니다. 청구 가능한 모델 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 값을 지나지 않은 경우 `true`를 반환합니다.

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

사용자를 위한 실제 구독을 생성할 준비가 되면 평소처럼 `newSubscription` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

사용자의 평가판 종료 날짜를 검색하려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 평가판을 사용 중인 경우 Carbon 날짜 인스턴스를 반환하고 그렇지 않은 경우 `null`를 반환합니다. 기본 구독이 아닌 특정 구독에 대한 평가판 종료 날짜를 확인하려는 경우 선택적 구독 유형 매개변수를 전달할 수도 있습니다.

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

사용자가 "일반" 평가판 기간 내에 있고 아직 실제 구독을 생성하지 않았는지 구체적으로 알고 싶은 경우 `onGenericTrial` 메서드를 사용할 수도 있습니다.

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>
### 평가판 연장

`extendTrial` 메서드를 사용하면 구독이 생성된 후 구독의 평가판 기간을 연장할 수 있습니다. 평가판이 이미 만료되었고 고객에게 이미 구독 요금이 청구된 경우에도 연장된 평가판을 제공할 수 있습니다. 평가판 기간 내에 소요된 시간은 고객의 다음 청구서에서 공제됩니다.

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
## Stripe 웹훅 처리 (Handling Stripe Webhooks)

> [!NOTE]
> [Stripe CLI](https://stripe.com/docs/stripe-cli)를 사용하여 로컬 개발 중에 웹훅을 테스트할 수 있습니다.

Stripe는 웹후크를 통해 다양한 이벤트를 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier의 웹훅 ​​컨트롤러를 가리키는 라우트는 Cashier 서비스 프로바이더에 의해 자동으로 등록됩니다. 이 컨트롤러는 들어오는 모든 웹훅 요청을 처리합니다.

기본적으로 Cashier 웹후크 컨트롤러는 요금 실패(Stripe 설정에 정의됨)가 너무 많은 구독 취소, 고객 업데이트, 고객 삭제, 구독 업데이트 및 결제 수단 변경을 자동으로 처리합니다. 그러나 곧 알게 되겠지만 이 컨트롤러를 확장하여 원하는 Stripe 웹훅 이벤트를 처리할 수 있습니다.

애플리케이션이 Stripe 웹훅을 처리할 수 있도록 하려면 Stripe 제어판에서 웹훅 URL를 구성해야 합니다. 기본적으로 Cashier의 웹훅 ​​컨트롤러는 `/stripe/webhook` URL 경로에 응답합니다. Stripe 제어판에서 활성화해야 하는 모든 웹후크의 전체 목록은 다음과 같습니다.

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

편의를 위해 Cashier에는 `cashier:webhook` Artisan 명령이 포함되어 있습니다. 이 명령은 Cashier에 필요한 모든 이벤트를 수신하는 Stripe에 웹후크를 생성합니다.

```shell
php artisan cashier:webhook
```

기본적으로 생성된 웹훅은 `APP_URL` 환경 변수로 정의된 URL와 Cashier에 포함된 `cashier.webhook` 라우트를 가리킵니다. 다른 URL를 사용하려는 경우 명령을 호출할 때 `--url` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

생성된 웹훅은 귀하의 Cashier 버전과 호환되는 Stripe API 버전을 사용합니다. 다른 Stripe 버전을 사용하려면 `--api-version` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

웹훅이 생성되면 즉시 활성화됩니다. 웹훅을 생성하고 싶지만 준비가 될 때까지 비활성화한 경우 명령을 호출할 때 `--disabled` 옵션을 제공할 수 있습니다.

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Cashier에 포함된 [웹훅 서명 확인](#verifying-webhook-signatures) 미들웨어를 사용하여 들어오는 Stripe 웹훅 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅 및 CSRF 보호

Stripe 웹훅은 Laravel의 [CSRF 보호](/docs/13.x/csrf)를 우회해야 하므로 Laravel가 수신 Stripe 웹훅에 대한 CSRF 토큰의 유효성을 검사하려고 시도하지 않도록 해야 합니다. 이를 달성하려면 애플리케이션의 `bootstrap/app.php` 파일의 CSRF 보호에서 `stripe/*`를 제외해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 청구 실패 및 기타 일반적인 Stripe 웹훅 이벤트에 대한 구독 취소를 자동으로 처리합니다. 그러나 처리하고 싶은 추가 웹훅 이벤트가 있는 경우 Cashier의 디스패치인 다음 이벤트를 청취하여 처리할 수 있습니다.

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

두 이벤트 모두 Stripe 웹훅의 전체 페이로드를 포함합니다. 예를 들어, `invoice.payment_succeeded` 웹훅을 처리하려는 경우 이벤트를 처리할 [리스너](/docs/13.x/events#defining-listeners)를 등록할 수 있습니다.

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
### 웹훅 서명 확인

웹훅을 보호하려면 [Stripe의 웹훅 ​​서명](https://stripe.com/docs/webhooks/signatures)을 사용할 수 있습니다. 편의를 위해 Cashier에는 들어오는 Stripe 웹훅 요청이 유효한지 확인하는 미들웨어가 자동으로 포함됩니다.

웹훅 확인을 활성화하려면 `STRIPE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 설정되어 있는지 확인하세요. 웹훅 `secret`는 Stripe 계정 대시보드에서 검색할 수 있습니다.

<a name="single-charges"></a>
## 단일 요금 (Single Charges)

<a name="simple-charge"></a>
### 간편충전

고객에게 일회성 비용을 청구하려면 청구 가능한 모델 인스턴스에서 `charge` 메서드를 사용할 수 있습니다. `charge` 메서드에 대한 두 번째 인수로 [결제 수단 식별자를 제공](#payment-methods-for-single-charges)해야 합니다.

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

`charge` 메서드는 배열을 세 번째 인수로 허용하므로 기본 Stripe 요금 생성에 원하는 옵션을 전달할 수 있습니다. 요금을 생성할 때 사용할 수 있는 옵션에 대한 자세한 내용은 [Stripe 문서](https://stripe.com/docs/api/charges/create)에서 확인할 수 있습니다.

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

기본 고객이나 사용자 없이 `charge` 메서드를 사용할 수도 있습니다. 이를 수행하려면 애플리케이션의 청구 가능한 모델의 새 인스턴스에서 `charge` 메서드를 호출하십시오.

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

청구에 실패하면 `charge` 메서드에서 예외가 발생합니다. 요금이 성공적으로 청구되면 `Laravel\Cashier\Payment` 인스턴스가 메서드에서 반환됩니다.

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]
> `charge` 메서드는 애플리케이션에서 사용되는 통화의 가장 낮은 분모로 결제 금액을 허용합니다. 예를 들어, 고객이 미국 달러로 지불하는 경우 금액은 페니로 지정되어야 합니다.

<a name="charge-with-invoice"></a>
### 송장으로 청구

때로는 일회성 비용을 청구하고 고객에게 PDF 송장을 제공해야 할 수도 있습니다. `invoicePrice` 메서드를 사용하면 바로 이러한 작업을 수행할 수 있습니다. 예를 들어 고객에게 새 셔츠 5벌에 대한 송장을 발행해 보겠습니다.

```php
$user->invoicePrice('price_tshirt', 5);
```

청구서는 사용자의 기본 결제 수단으로 즉시 청구됩니다. `invoicePrice` 메서드는 세 번째 인수로 배열을 허용합니다. 이 배열에는 송장 항목에 대한 청구 옵션이 포함되어 있습니다. 이 메서드에서 허용하는 네 번째 인수는 송장 자체에 대한 청구 옵션을 포함해야 하는 배열이기도 합니다.

```php
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

`invoicePrice`와 마찬가지로 `tabPrice` 메서드를 사용하여 여러 품목(송장당 최대 250개 품목)에 대해 일회성 요금을 생성할 수 있습니다. 이를 고객의 "탭"에 추가한 다음 고객에게 송장을 발행합니다. 예를 들어 고객에게 셔츠 5개와 머그잔 2개에 대한 송장을 보낼 수 있습니다.

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

또는 `invoiceFor` 메서드를 사용하여 고객의 기본 결제 수단에 대해 "일회성" 청구를 할 수도 있습니다.

```php
$user->invoiceFor('One Time Fee', 500);
```

`invoiceFor` 메서드를 사용할 수 있지만 사전 정의된 가격으로 `invoicePrice` 및 `tabPrice` 메서드를 사용하는 것이 좋습니다. 이렇게 하면 Stripe 대시보드 내에서 제품별 판매와 관련된 더 나은 분석 및 데이터에 액세스할 수 있습니다.

> [!WARNING]
> `invoice`, `invoicePrice` 및 `invoiceFor` 메서드는 실패한 청구 시도를 다시 시도하는 Stripe 송장을 생성합니다. 청구서에서 실패한 청구를 다시 시도하지 않으려면 첫 번째 청구 실패 후 Stripe API를 사용하여 청구서를 마감해야 합니다.

<a name="creating-payment-intents"></a>
### 지불 의도 생성

청구 가능한 모델 인스턴스에서 `pay` 메서드를 호출하여 새로운 Stripe 결제 의도를 생성할 수 있습니다. 이 메서드를 호출하면 `Laravel\Cashier\Payment` 인스턴스에 래핑된 결제 인텐트가 생성됩니다.

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

결제 의도를 생성한 후 사용자가 브라우저에서 결제를 완료할 수 있도록 클라이언트 비밀번호를 애플리케이션의 프론트엔드에 반환할 수 있습니다. Stripe 결제 의도를 사용하여 전체 결제 흐름을 구축하는 방법에 대해 자세히 알아보려면 [Stripe 문서](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참조하세요.

`pay` 메서드를 사용하는 경우 고객은 Stripe 대시보드 내에서 활성화된 기본 결제 수단을 사용할 수 있습니다. 또는 일부 특정 결제 수단만 사용하도록 허용하려는 경우 `payWith` 메서드를 사용할 수 있습니다.

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
> `pay` 및 `payWith` 메서드는 애플리케이션에서 사용되는 통화의 가장 낮은 분모로 결제 금액을 허용합니다. 예를 들어, 고객이 미국 달러로 지불하는 경우 금액은 페니로 지정되어야 합니다.

<a name="refunding-charges"></a>
### 환불 수수료

Stripe 요금을 환불해야 하는 경우 `refund` 메서드를 사용할 수 있습니다. 이 메서드는 Stripe [결제 의도 ID](#payment-methods-for-single-charges)를 첫 번째 인수로 허용합니다.

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 송장 (Invoices)

<a name="retrieving-invoices"></a>
### 송장 검색

`invoices` 메서드를 사용하면 청구 가능한 모델의 송장 배열을 쉽게 검색할 수 있습니다. `invoices` 메서드는 `Laravel\Cashier\Invoice` 인스턴스 컬렉션을 반환합니다.

```php
$invoices = $user->invoices();
```

결과에 보류 중인 송장을 포함하려면 `invoicesIncludingPending` 메서드를 사용할 수 있습니다.

```php
$invoices = $user->invoicesIncludingPending();
```

`findInvoice` 메서드를 사용하여 ID별로 특정 송장을 검색할 수 있습니다.

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### 송장 정보 표시

고객의 송장을 나열할 때 송장의 메서드를 사용하여 관련 송장 정보를 표시할 수 있습니다. 예를 들어, 사용자가 쉽게 다운로드할 수 있도록 모든 송장을 테이블에 나열할 수 있습니다.

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
### 다가오는 송장

고객에 대한 향후 송장을 검색하려면 `upcomingInvoice` 메서드를 사용할 수 있습니다.

```php
$invoice = $user->upcomingInvoice();
```

마찬가지로, 고객이 여러 구독을 갖고 있는 경우 특정 구독에 대해 예정된 송장을 검색할 수도 있습니다.

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### 구독 송장 미리보기

`previewInvoice` 메서드를 사용하면 가격을 변경하기 전에 송장을 미리 볼 수 있습니다. 이를 통해 특정 가격이 변경될 때 고객의 송장이 어떻게 표시되는지 결정할 수 있습니다.

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

여러 개의 새로운 가격이 포함된 송장을 미리 보려면 `previewInvoice` 메서드에 일련의 가격을 전달할 수 있습니다.

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### 송장 PDF 생성

송장 PDF를 생성하기 전에 Composer를 사용하여 Cashier의 기본 송장 렌더러인 Dompdf 라이브러리를 설치해야 합니다.

```shell
composer require dompdf/dompdf
```

라우트 또는 컨트롤러 내에서 `downloadInvoice` 메서드를 사용하여 특정 송장의 PDF 다운로드를 생성할 수 있습니다. 이 메서드는 송장을 다운로드하는 데 필요한 적절한 HTTP 응답을 자동으로 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

기본적으로 송장의 모든 데이터는 Stripe에 저장된 고객 및 송장 데이터에서 파생됩니다. 파일 이름은 `app.name` 구성 값을 기반으로 합니다. 그러나 배열을 `downloadInvoice` 메서드의 두 번째 인수로 제공하여 이 데이터 중 일부를 사용자 지정할 수 있습니다. 이 배열을 사용하면 회사 및 제품 세부 정보와 같은 정보를 사용자 지정할 수 있습니다.

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

`downloadInvoice` 메서드는 세 번째 인수를 통해 사용자 지정 파일 이름도 허용합니다. 이 파일 이름에는 자동으로 `.pdf` 접미사가 붙습니다.

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### 맞춤형 송장 렌더러

Cashier를 사용하면 맞춤형 송장 렌더러를 사용할 수도 있습니다. 기본적으로 Cashier는 [dompdf](https://github.com/dompdf/dompdf) PHP 라이브러리를 활용하여 Cashier의 송장을 생성하는 `DompdfInvoiceRenderer` 구현을 사용합니다. 그러나 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현하여 원하는 렌더러를 사용할 수 있습니다. 예를 들어, 타사 PDF 렌더링 서비스에 대한 API 호출을 사용하여 송장 PDF를 렌더링할 수 있습니다.

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

송장 렌더러 계약을 구현한 후에는 애플리케이션의 `config/cashier.php` 구성 파일에서 `cashier.invoices.renderer` 구성 값을 업데이트해야 합니다. 이 구성 값은 사용자 지정 렌더러 구현의 클래스 이름으로 설정되어야 합니다.

<a name="checkout"></a>
## 점검 (Checkout)

Cashier Stripe는 [Stripe 체크아웃](https://stripe.com/payments/checkout)도 지원합니다. Stripe Checkout은 사전 구축된 호스팅 결제 페이지를 제공함으로써 결제를 허용하는 사용자 지정 페이지를 구현하는 수고를 덜어줍니다.

다음 문서에는 Cashier로 Stripe Checkout을 사용하여 시작하는 방법에 대한 정보가 포함되어 있습니다. Stripe Checkout에 대해 자세히 알아보려면 [Stripe의 Checkout 관련 문서](https://stripe.com/docs/payments/checkout) 검토도 고려해야 합니다.

<a name="product-checkouts"></a>
### 제품 결제

청구 가능한 모델에서 `checkout` 메서드를 사용하여 Stripe 대시보드 내에서 생성된 기존 제품에 대한 체크아웃을 수행할 수 있습니다. `checkout` 메서드는 새로운 Stripe Checkout 세션을 시작합니다. 기본적으로 Stripe 가격 ID를 전달해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

필요한 경우 제품 수량을 지정할 수도 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

고객이 이 라우트를 방문하면 Stripe의 결제 페이지로 리디렉션됩니다. 기본적으로 사용자가 구매를 성공적으로 완료하거나 취소하면 `home` 라우트 위치로 리디렉션되지만 `success_url` 및 `cancel_url` 옵션을 사용하여 사용자 지정 콜백 URL을 지정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

`success_url` 체크아웃 옵션을 정의할 때 URL를 호출할 때 체크아웃 세션 ID를 쿼리 문자열 매개변수로 추가하도록 Stripe에 지시할 수 있습니다. 이렇게 하려면 리터럴 문자열 `{CHECKOUT_SESSION_ID}`를 `success_url` 쿼리 문자열에 추가하세요. Stripe는 이 자리 표시자를 실제 결제 세션 ID로 대체합니다.

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
#### 프로모션 코드

기본적으로 Stripe Checkout에서는 [사용자가 사용할 수 있는 프로모션 코드](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 허용하지 않습니다. 다행히 결제 페이지에서 이를 활성화하는 쉬운 방법이 있습니다. 그렇게 하려면 `allowPromotionCodes` 메서드를 호출하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### 단일 청구 결제

Stripe 대시보드에서 생성되지 않은 임시 제품에 대해 단순 청구를 수행할 수도 있습니다. 이렇게 하려면 청구 가능한 모델에서 `checkoutCharge` 메서드를 사용하고 청구 가능한 금액, 제품 이름 및 선택적 수량을 전달할 수 있습니다. 고객이 이 라우트를 방문하면 Stripe의 결제 페이지로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` 메서드를 사용하면 Stripe는 항상 Stripe 대시보드에 새로운 제품과 가격을 생성합니다. 따라서 Stripe 대시보드에서 제품을 미리 생성하고 대신 `checkout` 메서드를 사용하는 것이 좋습니다.

<a name="subscription-checkouts"></a>
### 구독 결제

> [!WARNING]
> 구독을 위해 Stripe Checkout을 사용하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 활성화해야 합니다. 이 웹훅은 데이터베이스에 구독 기록을 생성하고 모든 관련 구독 항목을 저장합니다.

Stripe Checkout을 사용하여 구독을 시작할 수도 있습니다. Cashier의 구독 빌더 메서드로 구독을 정의한 후 `checkout ` 메서드를 호출할 수 있습니다. 고객이 이 라우트를 방문하면 Stripe의 결제 페이지로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

제품 결제와 마찬가지로 성공 및 취소 URL을 맞춤 설정할 수 있습니다.

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

물론 구독 결제를 위해 프로모션 코드를 활성화할 수도 있습니다.

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
> 안타깝게도 Stripe Checkout은 구독을 시작할 때 모든 구독 청구 옵션을 지원하지 않습니다. 구독 빌더에서 `anchorBillingCycleOn` 메서드를 사용하거나 비례 배분 방식을 설정하거나 결제 방식을 설정하면 Stripe Checkout 세션 중에는 아무런 영향을 미치지 않습니다. 사용 가능한 매개변수를 검토하려면 [Stripe 체크아웃 세션 API 문서](https://stripe.com/docs/api/checkout/sessions/create)를 참조하세요.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe 체크아웃 및 평가판 기간

물론, Stripe Checkout을 사용하여 완료할 구독을 구축할 때 시험 기간을 정의할 수 있습니다.

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

그러나 평가판 기간은 Stripe Checkout에서 지원하는 최소 평가판 시간인 48시간 이상이어야 합니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독 및 웹훅

Stripe 및 Cashier는 웹후크를 통해 구독 상태를 업데이트하므로 고객이 결제 정보를 입력한 후 애플리케이션으로 돌아올 때 구독이 아직 활성화되지 않았을 가능성이 있다는 점을 기억하세요. 이 시나리오를 처리하기 위해 사용자에게 결제 또는 구독이 보류 중임을 알리는 메시지를 표시할 수 있습니다.

<a name="collecting-tax-ids"></a>
### 세금 ID 수집

Checkout에서는 고객의 세금 ID 수집도 지원합니다. 결제 세션에서 이를 활성화하려면 세션을 생성할 때 `collectTaxIds` 메서드를 호출하십시오.

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

이 메서드가 호출되면 고객이 회사로서 구매하는지 여부를 표시할 수 있는 새 확인란을 사용할 수 있습니다. 그렇다면 세금 ID 번호를 제공할 기회가 주어집니다.

> [!WARNING]
> 애플리케이션의 서비스 프로바이더에서 [자동 세금 징수](#tax-configuration)를 이미 구성한 경우 이 기능이 자동으로 활성화되며 `collectTaxIds` 메서드를 호출할 필요가 없습니다.

<a name="guest-checkouts"></a>
### 게스트 체크아웃

`Checkout::guest` 메서드를 사용하면 "계정"이 없는 애플리케이션 게스트에 대한 체크아웃 세션을 시작할 수 있습니다.

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

기존 사용자를 위한 체크아웃 세션을 생성할 때와 마찬가지로 `Laravel\Cashier\CheckoutBuilder` 인스턴스에서 사용 가능한 추가 메서드를 활용하여 손님 체크아웃 세션을 사용자 지정할 수 있습니다.

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

게스트 체크아웃이 완료된 후 Stripe는 디스패치를 `checkout.session.completed` 웹훅 이벤트로 설정할 수 있으므로 실제로 이 이벤트를 애플리케이션에 보내려면 [Stripe 웹훅을 구성](https://dashboard.stripe.com/webhooks)해야 합니다. Stripe 대시보드 내에서 웹훅이 활성화되면 [Cashier로 웹훅을 처리](#handling-stripe-webhooks)할 수 있습니다. 웹훅 페이로드에 포함된 개체는 고객의 주문을 이행하기 위해 검사할 수 있는 [체크아웃 개체](https://stripe.com/docs/api/checkout/sessions/object)입니다.

<a name="handling-failed-payments"></a>
## 결제 실패 처리 (Handling Failed Payments)

때로는 구독 또는 단일 청구에 대한 결제가 실패할 수 있습니다. 이런 일이 발생하면 Cashier는 이러한 일이 발생했음을 알리는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이 예외를 포착한 후 진행 방법에 대한 두 가지 옵션이 있습니다.

먼저 고객을 Cashier에 포함된 전용 결제 확인 페이지로 리디렉션할 수 있습니다. 이 페이지에는 이미 Cashier의 서비스 프로바이더를 통해 등록된 라우트라는 연결 항목이 있습니다. 따라서 `IncompletePayment` 예외를 포착하고 사용자를 결제 확인 페이지로 리디렉션할 수 있습니다.

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

결제 확인 페이지에서 고객은 신용 카드 정보를 다시 입력하고 "3D Secure" 확인과 같이 Stripe에서 요구하는 추가 작업을 수행하라는 메시지를 받게 됩니다. 결제를 확인한 후 사용자는 위에 지정된 `redirect` 매개변수에서 제공하는 URL로 리디렉션됩니다. 리디렉션 시 `message`(문자열) 및 `success`(정수) 쿼리 문자열 변수가 URL에 추가됩니다. 결제 페이지는 현재 다음과 같은 결제 수단 유형을 지원합니다.

<div class="content-list" markdown="1">

- 신용카드
- 알리페이
- 반콘택트
- BECS 자동이체
- EPS
- 지로페이
- 이상적인
- SEPA 자동이체

</div>

또는 Stripe가 결제 확인을 처리하도록 허용할 수도 있습니다. 이 경우 결제 확인 페이지로 리디렉션하는 대신 Stripe 대시보드에서 [Stripe의 자동 청구 이메일을 설정](https://dashboard.stripe.com/account/billing/automatic)할 수 있습니다. 그러나 `IncompletePayment` 예외가 발생하는 경우 사용자에게 추가 결제 확인 지침이 포함된 이메일을 받게 될 것임을 알려야 합니다.

`Billable` 트레이트를 사용하는 모델의 `charge`, `invoiceFor` 및 `invoice` 메서드에 대해 지불 예외가 발생할 수 있습니다. 구독과 상호 작용할 때 `SubscriptionBuilder`의 `create` 메서드와 `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice` 및 `swapAndInvoice` 메서드에서 불완전한 결제 예외가 발생할 수 있습니다.

기존 구독에 불완전한 결제가 있는지 확인하려면 청구 가능한 모델 또는 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용하여 수행할 수 있습니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

예외 인스턴스에서 `payment` 속성을 검사하여 불완전한 결제의 특정 상태를 파생할 수 있습니다.

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
### 결제 확인

일부 결제 수단에는 결제를 확인하기 위해 추가 데이터가 필요합니다. 예를 들어, SEPA 결제 수단에는 결제 프로세스 중에 추가 "명령" 데이터가 필요합니다. `withPaymentConfirmationOptions` 메서드를 사용하여 이 데이터를 Cashier에 제공할 수 있습니다.

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

[Stripe API 문서](https://stripe.com/docs/api/payment_intents/confirm)를 참조하여 결제 확인 시 허용되는 모든 옵션을 검토할 수 있습니다.

<a name="strong-customer-authentication"></a>
## 강력한 고객 인증 (Strong Customer Authentication)

귀하의 회사 또는 고객 중 한 명이 유럽에 본사를 두고 있는 경우 EU의 SCA(강력한 고객 인증) 규정을 준수해야 합니다. 이 규정은 결제 사기를 방지하기 위해 유럽 연합에서 2019년 9월에 제정한 것입니다. 다행히 Stripe 및 Cashier는 SCA 호환 애플리케이션을 구축할 준비가 되어 있습니다.

> [!WARNING]
> 시작하기 전에 [Stripe의 PSD2 및 SCA 가이드](https://stripe.com/guides/strong-customer-authentication)와 [새 SCA API에 대한 문서](https://stripe.com/docs/strong-customer-authentication)를 검토하세요.

<a name="payments-requiring-additional-confirmation"></a>
### 추가 확인이 필요한 결제

SCA 규정에 따라 결제를 확인하고 처리하기 위해 추가 확인이 필요한 경우가 많습니다. 이런 일이 발생하면 Cashier는 추가 확인이 필요함을 알리는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시킵니다. 이러한 예외를 처리하는 방법에 대한 자세한 내용은 [실패한 결제 처리](#handling-failed-payments) 문서에서 확인할 수 있습니다.

Stripe 또는 Cashier가 제공하는 결제 확인 화면은 특정 은행이나 카드 발급사의 결제 흐름에 맞게 맞춤화될 수 있으며 추가 카드 확인, 임시 소액 청구, 별도의 장치 인증 또는 기타 형태의 확인이 포함될 수 있습니다.

<a name="incomplete-and-past-due-state"></a>
#### 미완료 및 연체 상태

결제에 추가 확인이 필요한 경우 구독은 `stripe_status` 데이터베이스 열에 표시된 대로 `incomplete` 또는 `past_due` 상태로 유지됩니다. Cashier는 결제 확인이 완료되고 웹후크를 통해 Stripe가 애플리케이션 완료 알림을 보내는 즉시 고객의 구독을 자동으로 활성화합니다.

`incomplete` 및 `past_due` 상태에 대한 자세한 내용은 [이러한 상태에 대한 추가 문서](#incomplete-and-past-due-status)를 참조하세요.

<a name="off-session-payment-notifications"></a>
### 세션 외 결제 알림

SCA 규정에 따라 고객은 구독이 활성화된 동안에도 때때로 결제 세부 정보를 확인해야 하므로 Cashier는 세션 외 결제 확인이 필요할 때 고객에게 알림을 보낼 수 있습니다. 예를 들어, 구독이 갱신될 때 이런 일이 발생할 수 있습니다. Cashier의 결제 알림은 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수를 알림 클래스로 설정하여 활성화할 수 있습니다. 기본적으로 이 알림은 비활성화되어 있습니다. 물론 Cashier에는 이 목적으로 사용할 수 있는 알림 클래스가 포함되어 있지만 원하는 경우 고유한 알림 클래스를 자유롭게 제공할 수 있습니다.

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

세션 외 결제 확인 알림이 전달되도록 하려면 애플리케이션에 [Stripe 웹훅이 구성](#handling-stripe-webhooks)되고 `invoice.payment_action_required` 웹훅이 Stripe 대시보드에서 활성화되어 있는지 확인하세요. 또한 `Billable` 모델은 Laravel의 `Illuminate\Notifications\Notifiable` 트레이트도 사용해야 합니다.

> [!WARNING]
> 고객이 추가 확인이 필요한 수동 결제를 하는 경우에도 알림이 전송됩니다. 불행하게도 Stripe에서는 결제가 수동으로 이루어졌는지 또는 "세션 외"로 이루어졌는지 알 수 있는 방법이 없습니다. 그러나 고객이 이미 결제를 확인한 후 결제 페이지를 방문하면 '결제 성공' 메시지만 표시됩니다. 고객이 실수로 동일한 결제를 두 번 확인하여 실수로 두 번째 요금이 청구되는 일은 허용되지 않습니다.

<a name="stripe-sdk"></a>
## Stripe SDK (Stripe SDK)

Cashier 개체 중 다수는 Stripe SDK 개체를 둘러싼 래퍼입니다. Stripe 개체와 직접 상호 작용하려면 `asStripe` 메서드를 사용하여 편리하게 검색할 수 있습니다.

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

`updateStripeSubscription` 메서드를 사용하여 Stripe 구독을 직접 업데이트할 수도 있습니다.

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

`Stripe\StripeClient` 클라이언트를 직접 사용하려는 경우 `Cashier` 클래스에서 `stripe` 메서드를 호출할 수 있습니다. 예를 들어 이 메서드를 사용하여 `StripeClient` 인스턴스에 액세스하고 Stripe 계정에서 가격 목록을 검색할 수 있습니다.

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## 테스트 (Testing)

Cashier를 사용하는 애플리케이션을 테스트할 때 실제 HTTP 요청을 Stripe API로 모의할 수 있습니다. 그러나 이를 위해서는 Cashier 자체 동작을 부분적으로 다시 구현해야 합니다. 따라서 테스트가 실제 Stripe API에 도달하도록 허용하는 것이 좋습니다. 속도는 느리지만 애플리케이션이 예상대로 작동하고 있다는 확신을 더 많이 제공하며 느린 테스트는 자체 Pest / PHPUnit 테스트 그룹 내에 배치될 수 있습니다.

테스트할 때 Cashier 자체에는 이미 훌륭한 테스트 모음이 있다는 점을 기억하십시오. 따라서 모든 기본 Cashier 동작이 아니라 자신의 애플리케이션의 구독 및 결제 흐름을 테스트하는 데에만 집중해야 합니다.

시작하려면 Stripe 비밀의 **테스트** 버전을 `phpunit.xml` 파일에 추가하세요.

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

이제 테스트하는 동안 Cashier와 상호 작용할 때마다 실제 API 요청을 Stripe 테스트 환경으로 보냅니다. 편의를 위해 테스트에 사용할 수 있는 구독/가격으로 Stripe 테스트 계정을 미리 채워야 합니다.

> [!NOTE]
> 신용 카드 거부 및 실패와 같은 다양한 청구 시나리오를 테스트하려면 Stripe에서 제공하는 광범위한 [테스트 카드 번호 및 토큰](https://stripe.com/docs/testing)을 사용할 수 있습니다.
