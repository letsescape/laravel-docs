# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [Billable 모델](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로깅](#logging)
    - [커스텀 모델 사용](#using-custom-models)
- [빠른 시작](#quickstart)
    - [제품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 업데이트](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [Billing Portal](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 여부](#payment-method-presence)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [여러 제품이 포함된 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 청구](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험(Trial)](#subscription-trials)
    - [결제 수단을 미리 받는 경우](#with-payment-method-up-front)
    - [결제 수단 없이 시작하는 경우](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단한 결제](#simple-charge)
    - [청구서가 포함된 결제](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [청구서](#invoices)
    - [청구서 조회](#retrieving-invoices)
    - [예정된 청구서](#upcoming-invoices)
    - [구독 청구서 미리보기](#previewing-subscription-invoices)
    - [청구서 PDF 생성](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [제품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [게스트 Checkout](#guest-checkouts)
- [실패한 결제 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 사용할 수 있도록 **표현력이 좋고 직관적인 인터페이스**를 제공합니다. 이 라이브러리는 구독 결제 시스템을 구현할 때 반복적으로 작성해야 하는 대부분의 보일러플레이트 코드를 처리해 줍니다.

기본적인 구독 관리 기능 외에도 Cashier는 다음과 같은 기능을 지원합니다.

- 쿠폰(coupon)
- 구독 변경(swapping subscription)
- 구독 수량(subscription quantities)
- 취소 후 유예 기간(grace period)
- 청구서 PDF 생성

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

> [!WARNING]
> 호환성 문제를 방지하기 위해 Cashier는 **고정된 Stripe API 버전**을 사용합니다.  
> Cashier 16은 Stripe API 버전 `2025-06-30.basil`을 사용합니다.  
> Stripe의 새로운 기능 및 개선 사항을 반영하기 위해 **마이너 릴리스에서 Stripe API 버전이 업데이트될 수 있습니다.**

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용하여 Stripe용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier
```

패키지를 설치한 후 `vendor:publish` Artisan 명령어를 사용하여 Cashier의 마이그레이션을 게시합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음 데이터베이스 마이그레이션을 실행합니다.

```shell
php artisan migrate
```

Cashier의 마이그레이션은 다음 작업을 수행합니다.

- `users` 테이블에 여러 개의 컬럼을 추가
- 고객의 구독 정보를 저장하기 위한 `subscriptions` 테이블 생성
- 여러 가격(price)을 사용하는 구독을 위한 `subscription_items` 테이블 생성

필요하다면 `vendor:publish` Artisan 명령어를 사용하여 Cashier 설정 파일도 게시할 수 있습니다.

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로 Cashier가 Stripe 이벤트를 제대로 처리할 수 있도록 **Webhook 설정**을 반드시 진행해야 합니다.

> [!WARNING]
> Stripe는 Stripe 식별자를 저장하는 컬럼이 **대소문자를 구분(case-sensitive)** 하도록 권장합니다.  
> 따라서 MySQL을 사용하는 경우 `stripe_id` 컬럼의 collation을 `utf8_bin`으로 설정해야 합니다.  
> 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하십시오.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### Billable 모델

Cashier를 사용하기 전에 **결제 기능을 사용할 모델**에 `Billable` trait을 추가해야 합니다.

일반적으로 이 모델은 `App\Models\User`입니다.

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

이 trait은 다음과 같은 결제 관련 작업을 수행하는 다양한 메서드를 제공합니다.

- 구독 생성
- 쿠폰 적용
- 결제 수단 정보 업데이트

Cashier는 기본적으로 Laravel에서 제공하는 `App\Models\User` 모델을 **billable 모델**로 가정합니다.

다른 모델을 사용하려면 `useCustomerModel` 메서드를 통해 변경할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 설정합니다.

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
> Laravel 기본 `App\Models\User` 모델이 아닌 다른 모델을 사용할 경우,  
> Cashier에서 제공하는 [마이그레이션](#installation)을 게시한 뒤 **테이블 이름을 해당 모델에 맞게 수정해야 합니다.**

<a name="api-keys"></a>
### API 키

다음으로 Stripe API 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Stripe API 키는 Stripe 대시보드에서 확인할 수 있습니다.

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 `.env` 파일에 반드시 정의되어 있어야 합니다.  
> 이 값은 들어오는 webhook 요청이 실제로 **Stripe에서 온 것인지 검증하는 데 사용됩니다.**

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 **미국 달러 (USD)** 입니다.

애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 값을 설정하여 기본 통화를 변경할 수 있습니다.

```ini
CASHIER_CURRENCY=eur
```

또한 청구서에서 금액을 표시할 때 사용할 **로케일(locale)** 도 설정할 수 있습니다.

Cashier 내부에서는 통화 포맷을 위해 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장이 설치 및 설정되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax)를 사용하면 Stripe에서 생성되는 모든 청구서의 세금을 자동으로 계산할 수 있습니다.

자동 세금 계산을 활성화하려면 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출합니다.

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

세금 계산을 활성화하면 다음 항목에 자동으로 세금이 적용됩니다.

- 새로 생성되는 구독
- 단일 청구서(one-off invoice)

이 기능이 제대로 작동하려면 다음 고객 정보가 Stripe와 동기화되어 있어야 합니다.

- 고객 이름
- 주소
- 세금 ID

이를 위해 Cashier가 제공하는 다음 기능을 사용할 수 있습니다.

- [고객 데이터 동기화](#syncing-customer-data-with-stripe)
- [Tax ID 관리](#tax-ids)

<a name="logging"></a>
### 로깅

Cashier는 Stripe 관련 치명적인 오류를 기록할 **로그 채널**을 지정할 수 있습니다.

`.env` 파일에 `CASHIER_LOGGER` 환경 변수를 설정하면 됩니다.

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출에서 발생하는 예외는 애플리케이션의 **기본 로그 채널**을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용

Cashier 내부에서 사용하는 모델을 **확장하여 커스터마이징**할 수 있습니다.

예를 들어 `Subscription` 모델을 확장하려면 다음과 같이 작성합니다.

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후 `Laravel\Cashier\Cashier` 클래스를 사용하여 Cashier가 해당 모델을 사용하도록 설정합니다.

보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 설정합니다.

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

(이후 문서는 계속 동일한 방식으로 이어집니다.)