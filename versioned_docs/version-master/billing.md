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
    - [Tax ID](#tax-ids)
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
    - [여러 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 수단을 먼저 등록하는 경우](#with-payment-method-up-front)
    - [결제 수단 없이 체험 시작](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단한 결제](#simple-charge)
    - [인보이스와 함께 결제](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [제품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [Tax ID 수집](#collecting-tax-ids)
    - [게스트 Checkout](#guest-checkouts)
- [실패한 결제 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [Off-session 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 보다 직관적이고 유연하게 사용할 수 있도록 해주는 인터페이스를 제공합니다. 구독 결제 시스템을 직접 구현할 때 발생하는 반복적인 보일러플레이트 코드를 대부분 처리해 줍니다.

기본적인 구독 관리 기능뿐만 아니라 다음과 같은 기능도 제공합니다.

- 쿠폰 처리
- 구독 요금 변경
- 구독 수량 관리
- 취소 후 유예 기간(grace period)
- 인보이스 PDF 생성

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

새로운 Cashier 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md)를 확인해야 합니다.

> [!WARNING]
> 변경 사항으로 인한 문제를 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 16은 Stripe API 버전 `2025-06-30.basil`을 사용합니다. 새로운 Stripe 기능과 개선 사항을 활용하기 위해 마이너 릴리스에서 Stripe API 버전이 업데이트될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용하여 Stripe용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier
```

패키지 설치 후 `vendor:publish` Artisan 명령어를 사용하여 Cashier의 마이그레이션을 퍼블리시합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음 데이터베이스 마이그레이션을 실행합니다.

```shell
php artisan migrate
```

Cashier의 마이그레이션은 다음 작업을 수행합니다.

- `users` 테이블에 여러 컬럼 추가
- 고객 구독 정보를 저장하는 `subscriptions` 테이블 생성
- 여러 가격을 가진 구독을 위한 `subscription_items` 테이블 생성

원한다면 Cashier 설정 파일도 퍼블리시할 수 있습니다.

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로 Stripe 이벤트를 정상적으로 처리하기 위해 반드시 [Cashier Webhook 설정](#handling-stripe-webhooks)을 해야 합니다.

> [!WARNING]
> Stripe는 Stripe 식별자를 저장하는 컬럼이 **대소문자를 구분(case-sensitive)** 하도록 설정할 것을 권장합니다. 따라서 MySQL을 사용하는 경우 `stripe_id` 컬럼의 collation을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하십시오.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### Billable 모델

Cashier를 사용하기 전에 과금 대상 모델(billable model)에 `Billable` trait을 추가해야 합니다. 일반적으로 이 모델은 `App\Models\User`입니다.

이 trait은 다음과 같은 과금 관련 작업을 수행할 수 있는 다양한 메서드를 제공합니다.

- 구독 생성
- 쿠폰 적용
- 결제 수단 정보 업데이트

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 `App\Models\User` 모델을 billable 모델로 가정합니다. 다른 모델을 사용하려면 `useCustomerModel` 메서드를 사용해 변경할 수 있습니다.

이 메서드는 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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
> Laravel에서 기본 제공하는 `App\Models\User` 모델이 아닌 다른 모델을 사용하는 경우, [Cashier 마이그레이션](#installation)을 퍼블리시한 뒤 테이블 이름을 해당 모델에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로 애플리케이션의 `.env` 파일에 Stripe API 키를 설정해야 합니다. API 키는 Stripe 대시보드에서 확인할 수 있습니다.

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수는 반드시 `.env` 파일에 설정해야 합니다. 이 값은 들어오는 webhook 요청이 실제 Stripe에서 보낸 것인지 확인하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 설정합니다.

```ini
CASHIER_CURRENCY=eur
```

또한 인보이스에서 금액을 표시할 때 사용할 로케일(locale)도 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용하여 통화 형식을 설정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장이 설치되어 있어야 합니다.