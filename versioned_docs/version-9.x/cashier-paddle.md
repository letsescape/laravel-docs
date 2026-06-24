<!-- # Laravel Cashier (Paddle) -->
# Laravel Cashier (Paddle)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
    - [Database Migrations](#database-migrations)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Paddle JS](#paddle-js)
    - [Currency Configuration](#currency-configuration)
    - [Overriding Default Models](#overriding-default-models)
- [Core Concepts](#core-concepts)
    - [Pay Links](#pay-links)
    - [Inline Checkout](#inline-checkout)
    - [User Identification](#user-identification)
- [Prices](#prices)
- [Customers](#customers)
    - [Customer Defaults](#customer-defaults)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Subscription Single Charges](#subscription-single-charges)
    - [Updating Payment Information](#updating-payment-information)
    - [Changing Plans](#changing-plans)
    - [Subscription Quantity](#subscription-quantity)
    - [Subscription Modifiers](#subscription-modifiers)
    - [Multiple Subscriptions](#multiple-subscriptions)
    - [Pausing Subscriptions](#pausing-subscriptions)
    - [Cancelling Subscriptions](#cancelling-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Payment Method Up Front](#with-payment-method-up-front)
    - [Without Payment Method Up Front](#without-payment-method-up-front)
- [Handling Paddle Webhooks](#handling-paddle-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
    - [Simple Charge](#simple-charge)
    - [Charging Products](#charging-products)
    - [Refunding Orders](#refunding-orders)
- [Receipts](#receipts)
    - [Past & Upcoming Payments](#past-and-upcoming-payments)
- [Handling Failed Payments](#handling-failed-payments)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) provides an expressive, fluent interface to [Paddle's](https://paddle.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading. In addition to basic subscription management, Cashier can handle: coupons, swapping subscription, subscription "quantities", cancellation grace periods, and more. -->
[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle's](https://paddle.com)의 구독 청구 서비스를 쉽고 유연하게 사용할 수 있도록 인터페이스를 제공합니다. 이 패키지는 번거로운 구독 청구 관련 코드를 대부분 대신 처리해줍니다. 기본적인 구독 관리 외에도 Cashier는 쿠폰 관리, 구독 변경, 구독 "수량", 구독 취소 유예 기간 등 다양한 기능을 지원합니다.

<!-- While working with Cashier we recommend you also review Paddle's [user guides](https://developer.paddle.com/guides) and [API documentation](https://developer.paddle.com/api-reference). -->
Cashier를 사용하면서, Paddle의 [user guides](https://developer.paddle.com/guides)와 [API documentation](https://developer.paddle.com/api-reference)도 함께 참고하시길 권장합니다.

<a name="upgrading-cashier"></a>
<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md). -->
Cashier의 새 버전으로 업그레이드할 때는 반드시 [the upgrade guide](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 확인하십시오.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Paddle using the Composer package manager: -->
먼저, Composer 패키지 매니저를 사용해 Paddle용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier-paddle
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 올바르게 처리하려면 반드시 [set up Cashier's webhook handling](#handling-paddle-webhooks)을 설정해야 한다는 점을 기억하세요.

<a name="paddle-sandbox"></a>
<!-- ### Paddle Sandbox -->
### Paddle Sandbox

<!-- During local and staging development, you should [register a Paddle Sandbox account](https://developer.paddle.com/getting-started/sandbox). This account will give you a sandboxed environment to test and develop your applications without making actual payments. You may use Paddle's [test card numbers](https://developer.paddle.com/getting-started/sandbox#test-cards) to simulate various payment scenarios. -->
로컬 또는 스테이징 환경에서 개발을 진행할 때는, [register a Paddle Sandbox account](https://developer.paddle.com/getting-started/sandbox)을 등록해야 합니다. 이 계정은 실제 결제 없이 애플리케이션을 테스트하고 개발할 수 있는 샌드박스 환경을 제공합니다. 다양한 결제 시나리오를 시뮬레이션하려면 Paddle의 [test card numbers](https://developer.paddle.com/getting-started/sandbox#test-cards)를 사용할 수 있습니다.

<!-- When using the Paddle Sandbox environment, you should set the `PADDLE_SANDBOX` environment variable to `true` within your application's `.env` file: -->
Paddle 샌드박스 환경을 사용할 때는, 애플리케이션의 `.env` 파일에 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다.

```ini
PADDLE_SANDBOX=true
```

<!-- After you have finished developing your application you may [apply for a Paddle vendor account](https://paddle.com). Before your application is placed into production, Paddle will need to approve your application's domain. -->
애플리케이션 개발이 끝나면 [apply for a Paddle vendor account](https://paddle.com)을 신청할 수 있습니다. 애플리케이션을 실제 서비스 환경에 배포하기 전에, Paddle에서 애플리케이션의 도메인을 반드시 승인해주어야 합니다.

<a name="database-migrations"></a>
<!-- ### Database Migrations -->
### Database Migrations

<!-- The Cashier service provider registers its own database migration directory, so remember to migrate your database after installing the package. The Cashier migrations will create a new `customers` table. In addition, a new `subscriptions` table will be created to store all of your customer's subscriptions. Finally, a new `receipts` table will be created to store all of your application's receipt information: -->
Cashier 서비스 프로바이더는 자체 데이터베이스 마이그레이션 디렉터리를 등록합니다. 따라서 패키지 설치 후 반드시 데이터베이스 마이그레이션을 실행해야 합니다. Cashier 마이그레이션을 실행하면 새로운 `customers` 테이블이 생성됩니다. 또한, 고객의 모든 구독 정보를 저장할 새로운 `subscriptions` 테이블과, 애플리케이션의 모든 영수증 정보를 저장할 `receipts` 테이블도 함께 생성됩니다.

```shell
php artisan migrate
```

<!-- If you need to overwrite the migrations that are included with Cashier, you can publish them using the `vendor:publish` Artisan command: -->
Cashier에 기본 포함된 마이그레이션 파일을 직접 수정하고 싶다면, `vendor:publish` Artisan 명령어를 사용해 파일을 퍼블리시할 수 있습니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- If you would like to prevent Cashier's migrations from running entirely, you may use the `ignoreMigrations` provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
Cashier의 마이그레이션 자체를 실행하지 않으려는 경우, Cashier에서 제공하는 `ignoreMigrations` 메서드를 사용할 수 있습니다. 보통, 이 메서드는 `AppServiceProvider`의 `register` 메서드에서 호출해야 합니다.

```
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
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="billable-model"></a>
<!-- ### Billable Model -->
### Billable Model

<!-- Before using Cashier, you must add the `Billable` trait to your user model definition. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons and updating payment method information: -->
Cashier를 사용하려면 먼저, 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 정보 업데이트 등 자주 사용하는 청구 관련 작업을 간단하게 처리할 수 있도록 여러 메서드를 제공합니다.

```
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- If you have billable entities that are not users, you may also add the trait to those classes: -->
만약 사용자가 아닌 청구 가능한 엔터티가 있다면, 해당 클래스에도 이 트레이트를 추가할 수 있습니다.

```
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
<!-- ### API Keys -->
### API Keys

<!-- Next, you should configure your Paddle keys in your application's `.env` file. You can retrieve your Paddle API keys from the Paddle control panel: -->
다음으로, 애플리케이션의 `.env` 파일에 Paddle API 키를 설정해야 합니다. Paddle 사이트의 컨트롤 패널에서 관련 API 키들을 가져올 수 있습니다.

```ini
PADDLE_VENDOR_ID=your-paddle-vendor-id
PADDLE_VENDOR_AUTH_CODE=your-paddle-vendor-auth-code
PADDLE_PUBLIC_KEY="your-paddle-public-key"
PADDLE_SANDBOX=true
```

<!-- The `PADDLE_SANDBOX` environment variable should be set to `true` when you are using [Paddle's Sandbox environment](#paddle-sandbox). The `PADDLE_SANDBOX` variable should be set to `false` if you are deploying your application to production and are using Paddle's live vendor environment. -->
`PADDLE_SANDBOX` 환경 변수는 [Paddle's Sandbox environment](#paddle-sandbox)을 사용할 때 `true`로 설정해야 합니다. 애플리케이션을 프로덕션에 배포하고 Paddle의 라이브 벤더 환경을 사용할 때는 `PADDLE_SANDBOX` 변수를 `false`로 설정해야 합니다.

<a name="paddle-js"></a>
<!-- ### Paddle JS -->
### Paddle JS

<!-- Paddle relies on its own JavaScript library to initiate the Paddle checkout widget. You can load the JavaScript library by placing the `@paddleJS` Blade directive right before your application layout's closing `</head>` tag: -->
Paddle은 자신의 결제 위젯을 초기화하는 별도의 자바스크립트 라이브러리를 사용합니다. 이 라이브러리를 불러오려면, 애플리케이션 레이아웃의 `</head>` 태그 바로 앞에 `@paddleJS` Blade 디렉티브를 추가하면 됩니다.

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by defining a `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
Cashier에서 기본 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정해 기본 통화를 변경할 수 있습니다.

```ini
CASHIER_CURRENCY=EUR
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
Cashier의 통화 외에도, 청구서에 표시되는 금액의 지역화(로케일)를 지정할 수 있습니다. 내부적으로 Cashier는 [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php)를 이용해 통화 로케일을 적용합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 반드시 설치 및 설정되어 있어야 합니다.

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
Cashier 내부적으로 사용하는 모델을 자유롭게 확장하여 직접 정의할 수 있습니다. 예를 들어, Cashier의 기본 모델을 상속받아 자신만의 모델을 구현할 수 있습니다.

```
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Paddle\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
모델을 정의한 후에는, `Laravel\Paddle\Cashier` 클래스를 이용해 Cashier가 새로운 모델을 사용하도록 지정해야 합니다. 보통, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이를 설정합니다.

```
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
```

<a name="core-concepts"></a>
<!-- ## Core Concepts -->
## Core Concepts

<a name="pay-links"></a>
<!-- ### Pay Links -->
### Pay Links

<!-- Paddle lacks an extensive CRUD API to perform subscription state changes. Therefore, most interactions with Paddle are done through its [checkout widget](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout). Before we can display the checkout widget, we must generate a "pay link" using Cashier. A "pay link" will inform the checkout widget of the billing operation we wish to perform: -->
Paddle은 구독 상태 변경을 위한 완전한 CRUD API를 제공하지 않기 때문에, 대부분의 Paddle과의 상호작용은 [checkout widget](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout)을 통해 이루어집니다. 결제 위젯을 표시하기 전에, Cashier를 사용해 반드시 "결제 링크(pay link)"를 먼저 생성해야 합니다. 이 링크는 결제 위젯에 어떤 청구 작업을 수행할 것인지 알려줍니다.

```
use App\Models\User;
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $premium = 34567)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- Cashier includes a `paddle-button` [Blade component](/docs/9.x/blade#components). We may pass the pay link URL to this component as a "prop". When this button is clicked, Paddle's checkout widget will be displayed: -->
Cashier에는 `paddle-button` [Blade component](/docs/9.x/blade#components)가 포함되어 있습니다. 결제 링크 URL을 prop(속성)으로 이 컴포넌트에 전달할 수 있습니다. 이 버튼을 누르면 Paddle의 결제 위젯이 표시됩니다.

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- By default, this will display a button with the standard Paddle styling. You can remove all Paddle styling by adding the `data-theme="none"` attribute to the component: -->
기본적으로 이 버튼은 Paddle의 기본 스타일로 표시됩니다. Paddle의 스타일을 모두 제거하려면, 컴포넌트에 `data-theme="none"` 속성을 추가하면 됩니다.

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="none">
    Subscribe
</x-paddle-button>
```

<!-- The Paddle checkout widget is asynchronous. Once the user creates or updates a subscription within the widget, Paddle will send your application webhooks so that you may properly update the subscription state in our own database. Therefore, it's important that you properly [set up webhooks](#handling-paddle-webhooks) to accommodate for state changes from Paddle. -->
Paddle 결제 위젯은 비동기 방식으로 동작합니다. 사용자가 위젯에서 구독을 생성하거나 변경하면, Paddle은 웹훅을 통해 애플리케이션에 해당 정보를 전달하므로, 반드시 데이터베이스의 구독 상태도 함께 업데이트해야 합니다. 이처럼 결제 및 구독 상태 변경을 정확하게 반영하려면, 반드시 [set up webhooks](#handling-paddle-webhooks)이 잘 설정되어 있어야 합니다.

<!-- For more information on pay links, you may review [the Paddle API documentation on pay link generation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink). -->
결제 링크에 대해 더 자세한 정보가 필요하다면 [the Paddle API documentation on pay link generation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요.

> [!WARNING]
> 구독 상태가 변경되면, 해당 웹훅을 받기까지 보통은 짧은 지연 시간이 있지만, 사용자가 결제를 완료했더라도 구독이 즉시 활성화되지 않을 수 있음을 애플리케이션에서 반드시 고려해야 합니다.

<a name="manually-rendering-pay-links"></a>
<!-- #### Manually Rendering Pay Links -->
#### Manually Rendering Pay Links

<!-- You may also manually render a pay link without using Laravel's built-in Blade components. To get started, generate the pay link URL as demonstrated in previous examples: -->
Blade 컴포넌트를 사용하지 않고 결제 링크를 직접 렌더링할 수도 있습니다. 결제 링크 URL은 앞선 예시처럼 생성할 수 있습니다.

```
$payLink = $request->user()->newSubscription('default', $premium = 34567)
    ->returnTo(route('home'))
    ->create();
```

<!-- Next, simply attach the pay link URL to an `a` element in your HTML: -->
그 다음, 단순히 해당 결제 링크 URL을 HTML의 `a` 태그에 연결하면 됩니다.

```
<a href="#!" class="ml-4 paddle_button" data-override="{{ $payLink }}">
    Paddle Checkout
</a>
```

<a name="payments-requiring-additional-confirmation"></a>
<!-- #### Payments Requiring Additional Confirmation -->
#### Payments Requiring Additional Confirmation

<!-- Sometimes additional verification is required in order to confirm and process a payment. When this happens, Paddle will present a payment confirmation screen. Payment confirmation screens presented by Paddle or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
가끔 결제를 완료하려면 추가 인증이 필요한 경우가 있습니다. 이럴 때는 Paddle이 결제 확인 화면을 제공합니다. 이러한 확인 화면은 Paddle이나 Cashier에서 카드사 또는 은행의 인증 절차에 맞게 맞춤으로 보여줄 수 있으며, 카드 추가 확인, 소액 임시 청구, 별도의 기기 인증 등 다양한 방식이 사용될 수 있습니다.

<a name="inline-checkout"></a>
<!-- ### Inline Checkout -->
### Inline Checkout

<!-- If you don't want to make use of Paddle's "overlay" style checkout widget, Paddle also provides the option to display the widget inline. While this approach does not allow you to adjust any of the checkout's HTML fields, it allows you to embed the widget within your application. -->
Paddle의 오버레이 스타일 결제 위젯을 사용하고 싶지 않은 경우, Paddle은 결제 위젯을 페이지 내에 인라인으로 표시하는 기능도 제공합니다. 이 방식은 결제 HTML 필드를 따로 커스터마이즈할 수는 없지만, 결제 위젯을 애플리케이션 내에 직접 임베드할 수 있습니다.

<!-- To make it easy for you to get started with inline checkout, Cashier includes a `paddle-checkout` Blade component. To get started, you should [generate a pay link](#pay-links) and pass the pay link to the component's `override` attribute: -->
Cashier에서는 인라인 결제 시작이 쉽도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. [generate a pay link](#pay-links)를 생성한 후, 해당 링크를 컴포넌트의 `override` 속성에 전달하면 됩니다.

```blade
<x-paddle-checkout :override="$payLink" class="w-full" />
```

<!-- To adjust the height of the inline checkout component, you may pass the `height` attribute to the Blade component: -->
인라인 결제 컴포넌트의 높이를 조절하려면 `height` 속성을 활용할 수 있습니다.

```blade
<x-paddle-checkout :override="$payLink" class="w-full" height="500" />
```

<a name="inline-checkout-without-pay-links"></a>
<!-- #### Inline Checkout Without Pay Links -->
#### Inline Checkout Without Pay Links

<!-- Alternatively, you may customize the widget with custom options instead of using a pay link: -->
또는, 결제 링크를 사용하지 않고도 몇 가지 옵션을 직접 전달하여 결제 위젯을 커스터마이즈할 수 있습니다.

```blade
@php
$options = [
    'product' => $productId,
    'title' => 'Product Title',
];
@endphp

<x-paddle-checkout :options="$options" class="w-full" />
```

<!-- Please consult Paddle's [guide on Inline Checkout](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout) as well as their [parameter reference](https://developer.paddle.com/reference/paddle-js/parameters) for further details on the inline checkout's available options. -->
인라인 결제에서 사용할 수 있는 다양한 옵션은 Paddle의 [guide on Inline Checkout](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout) 및 [parameter reference](https://developer.paddle.com/reference/paddle-js/parameters)를 참고하시기 바랍니다.

> [!WARNING]
> 커스텀 옵션으로 `passthrough` 옵션을 사용하고 싶다면, 반드시 key/value 배열 형태로 전달해야 합니다. Cashier가 자동으로 해당 배열을 JSON 문자열로 변환해줍니다. 단, `customer_id` passthrough 옵션은 Cashier 내부적으로 사용되므로 별도로 지정하실 필요가 없습니다.

<a name="manually-rendering-an-inline-checkout"></a>
<!-- #### Manually Rendering An Inline Checkout -->
#### Manually Rendering An Inline Checkout

<!-- You may also manually render an inline checkout without using Laravel's built-in Blade components. To get started, generate the pay link URL [as demonstrated in previous examples](#pay-links). -->
Laravel의 Blade 컴포넌트를 사용하지 않고 인라인 결제를 직접 렌더링할 수도 있습니다. 먼저, [as demonstrated in previous examples](#pay-links)처럼 결제 링크 URL을 생성합니다.

<!-- Next, you may use Paddle.js to initialize the checkout. To keep this example simple, we will demonstrate this using [Alpine.js](https://github.com/alpinejs/alpine); however, you are free to translate this example to your own frontend stack: -->
그 다음, Paddle.js를 이용해 결제 창을 초기화하면 됩니다. 이 예제에서는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하지만, 여러분이 사용하는 다른 프론트엔드 프레임워크로 자유롭게 변경할 수 있습니다.

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
<!-- ### User Identification -->
### User Identification

<!-- In contrast to Stripe, Paddle users are unique across all of Paddle, not unique per Paddle account. Because of this, Paddle's API's do not currently provide a method to update a user's details such as their email address. When generating pay links, Paddle identifies users using the `customer_email` parameter. When creating a subscription, Paddle will try to match the user provided email to an existing Paddle user. -->
Stripe와는 달리, Paddle의 사용자 계정은 Paddle 전체에서 고유하게 관리됩니다(즉, Paddle 계정별로 구분되는 것이 아님). 이러한 이유로, 현재 Paddle API에서는 사용자의 이메일 주소 같은 세부 정보를 업데이트하는 기능이 제공되지 않습니다. 결제 링크를 생성할 때에는 Paddle이 `customer_email` 파라미터로 사용자를 식별합니다. 구독을 생성할 때, Paddle은 입력된 이메일 주소와 동일한 이메일을 가진 기존 사용자가 있다면 해당 사용자와 연결을 시도합니다.

<!-- In light of this behavior, there are some important things to keep in mind when using Cashier and Paddle. First, you should be aware that even though subscriptions in Cashier are tied to the same application user, **they could be tied to different users within Paddle's internal systems**. Secondly, each subscription has its own connected payment method information and could also have different email addresses within Paddle's internal systems (depending on which email was assigned to the user when the subscription was created). -->
이러한 동작 방식 때문에 Cashier와 Paddle을 사용할 때 꼭 주의해야 할 점이 있습니다. 우선, Cashier에서는 하나의 애플리케이션 사용자와 구독이 연결되어 있더라도, **Paddle의 내부 시스템에서는 서로 다른 사용자에 연결될 수 있습니다.** 또한, 각 구독별로 개별적인 결제 정보, 이메일 주소를 별도로 관리할 수 있으며(구독 생성 시에 어떤 이메일을 할당받았는지에 따라 다름) 서로 다를 수도 있습니다.

<!-- Therefore, when displaying subscriptions you should always inform the user which email address or payment method information is connected to the subscription on a per-subscription basis. Retrieving this information can be done with the following methods provided by the `Laravel\Paddle\Subscription` model: -->
따라서, 구독 정보를 보여줄 때마다 반드시 각 구독이 Paddle 시스템 내에서 어떤 이메일/결제 정보와 연결되어 있는지 사용자에게 알려주는 것이 좋습니다. 이러한 정보는 `Laravel\Paddle\Subscription` 모델의 다음과 같은 메서드로 확인할 수 있습니다.

```
$subscription = $user->subscription('default');

$subscription->paddleEmail();
$subscription->paymentMethod();
$subscription->cardBrand();
$subscription->cardLastFour();
$subscription->cardExpirationDate();
```

<!-- There is currently no way to modify a user's email address through the Paddle API. When a user wants to update their email address within Paddle, the only way for them to do so is to contact Paddle customer support. When communicating with Paddle, they need to provide the `paddleEmail` value of the subscription to assist Paddle in updating the correct user. -->
현재로서는 Paddle API를 통해 사용자의 이메일 주소를 직접 수정할 수 있는 기능이 없습니다. 사용자가 Paddle 내 이메일을 변경하고 싶은 경우, Paddle 고객 지원에 직접 연락해야 하며, 이 때 구독의 `paddleEmail` 값을 제공해야 정확한 사용자 정보 수정에 도움이 됩니다.

<a name="prices"></a>
<!-- ## Prices -->
## Prices

<!-- Paddle allows you to customize prices per currency, essentially allowing you to configure different prices for different countries. Cashier Paddle allows you to retrieve all of the prices for a given product using the `productPrices` method. This method accepts the product IDs of the products you wish to retrieve prices for: -->
Paddle은 각 통화별로 가격을 개별적으로 지정할 수 있으므로, 국가별로 서로 다른 가격을 설정할 수 있습니다. Cashier Paddle을 사용하면, `productPrices` 메서드를 통해 한 번에 여러 상품의 가격 정보를 받아올 수 있습니다. 이 메서드는 가격 정보를 조회할 상품의 ID 배열을 인수로 받습니다.

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456]);
```

<!-- The currency will be determined based on the IP address of the request; however, you may optionally provide a specific country to retrieve prices for: -->
통화 종류는 일반적으로 요청자의 IP 주소로 자동 결정되지만, 명시적으로 특정 국가의 가격을 조회하고 싶다면 두 번째 파라미터로 국가 정보를 전달할 수 있습니다.

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], ['customer_country' => 'BE']);
```

<!-- After retrieving the prices you may display them however you wish: -->
가격 정보를 가져온 뒤에는 원하는 방식으로 화면에 표시할 수 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

<!-- You may also display the net price (excludes tax) and display the tax amount separately: -->
세금 제외 금액(순액)을 표시하거나, 세금액을 별도로 표시할 수도 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->net() }} (+ {{ $price->price()->tax() }} tax)</li>
    @endforeach
</ul>
```

<!-- If you retrieved prices for subscription plans you can display their initial and recurring price separately: -->
구독 요금제에 대한 가격 정보를 가져왔다면, 최초 결제 금액과 반복 결제 금액을 따로 표시할 수도 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - Initial: {{ $price->initialPrice()->gross() }} - Recurring: {{ $price->recurringPrice()->gross() }}</li>
    @endforeach
</ul>
```

<!-- For more information, [check Paddle's API documentation on prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices). -->
더 자세한 정보는 [check Paddle's API documentation on prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)를 참고하십시오.

<a name="prices-customers"></a>
<!-- #### Customers -->
#### Customers

<!-- If a user is already a customer and you would like to display the prices that apply to that customer, you may do so by retrieving the prices directly from the customer instance: -->
이미 가입한 사용자가 있다면, 해당 고객에게 적용되는 가격을 그 고객 인스턴스에서 직접 조회할 수 있습니다.

```
use App\Models\User;

$prices = User::find(1)->productPrices([123, 456]);
```

<!-- Internally, Cashier will use the user's [`paddleCountry` method](#customer-defaults) to retrieve the prices in their currency. So, for example, a user living in the United States will see prices in USD while a user in Belgium will see prices in EUR. If no matching currency can be found the default currency of the product will be used. You can customize all prices of a product or subscription plan in the Paddle control panel. -->
내부적으로 Cashier는 사용자의 [`paddleCountry` method](#customer-defaults)를 활용해 해당 국가의 통화로 가격을 받아옵니다. 예를 들어, 미국 거주자일 경우 USD, 벨기에 거주자일 경우 EUR로 가격이 표시됩니다. 만약 일치하는 통화를 찾지 못하면 상품의 기본 통화를 사용합니다. 모든 상품이나 구독 요금제의 가격은 Paddle 컨트롤 패널에서 자유롭게 변경할 수 있습니다.

<a name="prices-coupons"></a>
<!-- #### Coupons -->
#### Coupons

<!-- You may also choose to display prices after a coupon reduction. When calling the `productPrices` method, coupons may be passed as a comma delimited string: -->
쿠폰 할인이 적용된 가격을 함께 표시할 수도 있습니다. `productPrices` 메서드를 호출할 때, 쿠폰을 콤마로 구분된 문자열로 전달하면 됩니다.

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], [
    'coupons' => 'SUMMERSALE,20PERCENTOFF'
]);
```

<!-- Then, display the calculated prices using the `price` method: -->
이렇게 조회한 가격은 `price` 메서드로 사용할 수 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

<!-- You may display the original listed prices (without coupon discounts) using the `listPrice` method: -->
쿠폰 할인이 적용되지 않은 원래 가격이 필요하다면 `listPrice` 메서드를 사용하면 됩니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->listPrice()->gross() }}</li>
    @endforeach
</ul>
```

> [!WARNING]
> 가격 조회 API를 사용할 때, Paddle은 쿠폰 적용을 일회성 결제 상품에만 허용하며 구독 요금제에는 적용할 수 없습니다.

<a name="customers"></a>
<!-- ## Customers -->
## Customers

<a name="customer-defaults"></a>
<!-- ### Customer Defaults -->
### Customer Defaults

<!-- Cashier allows you to define some useful defaults for your customers when creating pay links. Setting these defaults allow you to pre-fill a customer's email address, country, and postal code so that they can immediately move on to the payment portion of the checkout widget. You can set these defaults by overriding the following methods on your billable model: -->
Cashier를 이용하면 결제 링크 생성 시 고객을 위한 유용한 기본값을 미리 지정할 수 있습니다. 기본값을 미리 지정해두면, 고객의 이메일, 국가, 우편번호를 자동으로 입력란에 채워주어, 결제 과정을 더 빠르게 진행할 수 있습니다. 이러한 기본값은 청구 가능 모델에서 아래와 같이 메서드를 오버라이드 하는 방식으로 지정할 수 있습니다.

```
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
```

<!-- These defaults will be used for every action in Cashier that generates a [pay link](#pay-links). -->
이 기본값은 Cashier에서 [pay link](#pay-links)를 생성하는 모든 작업에 사용됩니다.

<a name="subscriptions"></a>
<!-- ## Subscriptions -->
## Subscriptions

<a name="creating-subscriptions"></a>
<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model from your database, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription pay link: -->
구독을 생성하려면 먼저 데이터베이스에서 청구 가능 모델 인스턴스를 가져와야 합니다. 일반적으로 이 모델은 `App\Models\User`의 인스턴스입니다. 모델 인스턴스를 가져온 다음, `newSubscription` 메서드를 사용해 해당 모델의 구독 결제 링크를 생성할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $premium = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- The first argument passed to the `newSubscription` method should be the internal name of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription name is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument given to the `newSubscription` method is the specific plan the user is subscribing to. This value should correspond to the plan's identifier in Paddle. The `returnTo` method accepts a URL that your user will be redirected to after they successfully complete the checkout. -->
`newSubscription`의 첫 번째 인자는 구독의 내부 이름입니다. 만약 애플리케이션에서 하나의 구독만 제공한다면, 이 값을 `default` 또는 `primary` 등으로 지정할 수 있습니다. 이 구독 이름은 사용자에게 보이는 값이 아니라 애플리케이션 내부적으로만 사용되며, 띄어쓰기를 포함하지 않아야 하며 구독 생성 후에는 절대로 변경하면 안 됩니다. `newSubscription` 메서드의 두 번째 인자는 사용자가 가입할 요금제의 ID(상품 ID)로, Paddle에서 정의된 요금제 식별자와 일치해야 합니다. `returnTo` 메서드에는 사용자가 결제를 성공적으로 마친 후 리다이렉트될 URL을 지정합니다.

<!-- The `create` method will create a pay link which you can use to generate a payment button. The payment button can be generated using the `paddle-button` [Blade component](/docs/9.x/blade#components) that is included with Cashier Paddle: -->
`create` 메서드는 결제 버튼을 생성할 수 있는 결제 링크를 반환합니다. 결제 버튼은 Cashier Paddle에 포함된 `paddle-button` [Blade component](/docs/9.x/blade#components)를 사용해 만들 수 있습니다.

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- After the user has finished their checkout, a `subscription_created` webhook will be dispatched from Paddle. Cashier will receive this webhook and setup the subscription for your customer. In order to make sure all webhooks are properly received and handled by your application, ensure you have properly [setup webhook handling](#handling-paddle-webhooks). -->
결제가 완료되면 Paddle에서 `subscription_created` 웹훅이 발송됩니다. Cashier가 이 웹훅을 수신해 고객의 구독을 정상적으로 설정하게 됩니다. 모든 웹훅이 정확히 수신되고 처리되도록 하려면, 반드시 [setup webhook handling](#handling-paddle-webhooks)이 올바로 이루어져야 합니다.

<a name="additional-details"></a>
<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional customer or subscription details, you may do so by passing them as an array of key / value pairs to the `create` method. To learn more about the additional fields supported by Paddle, check out Paddle's documentation on [generating pay links](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink): -->
구독 생성 시, 고객이나 구독에 대한 기타 세부 정보를 지정하고 싶다면, `create` 메서드에 key/value 배열 형태로 전달할 수 있습니다. Paddle에서 지원하는 입력 필드에 대한 자세한 내용은 [generating pay links](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요.

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->create([
        'vat_number' => $vatNumber,
    ]);
```

<a name="subscriptions-coupons"></a>

<!-- #### Coupons -->
#### Coupons

<!-- If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method: -->
구독을 생성할 때 쿠폰을 적용하고 싶다면, `withCoupon` 메서드를 사용할 수 있습니다.

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withCoupon('code')
    ->create();
```

<a name="metadata"></a>
<!-- #### Metadata -->
#### Metadata

<!-- You can also pass an array of metadata using the `withMetadata` method: -->
`withMetadata` 메서드를 사용해 메타데이터 배열을 함께 전달할 수도 있습니다.

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withMetadata(['key' => 'value'])
    ->create();
```

> [!WARNING]
> 메타데이터를 제공할 때 `subscription_name`을 메타데이터 키로 사용하지 마십시오. 이 키는 Cashier 내부적으로 예약되어 있습니다.

<a name="checking-subscription-status"></a>
<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a user is subscribed to your application, you may check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the user has an active subscription, even if the subscription is currently within its trial period: -->
사용자가 애플리케이션에 구독한 이후에는 다양한 편리한 메서드로 해당 사용자의 구독 상태를 확인할 수 있습니다. 먼저, `subscribed` 메서드는 사용자가 활성 구독을 보유 중이면, 무료 체험(Trial) 기간이어도 `true`를 반환합니다.

```
if ($user->subscribed('default')) {
    //
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/9.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` 메서드는 [route middleware](/docs/9.x/middleware)로 사용하기에 적합하므로, 사용자의 구독 상태에 따라 라우트 및 컨트롤러 접근을 제한할 수 있습니다.

```
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
```

<!-- If you would like to determine if a user is still within their trial period, you may use the `onTrial` method. This method can be useful for determining if you should display a warning to the user that they are still on their trial period: -->
사용자가 여전히 체험(Trial) 기간 내에 있는지 확인하고 싶다면, `onTrial` 메서드를 사용할 수 있습니다. 이 메서드를 활용하면 사용자가 아직 체험 기간임을 알리는 안내 메시지를 표시하는 등 다양한 처리가 가능합니다.

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- The `subscribedToPlan` method may be used to determine if the user is subscribed to a given plan based on a given Paddle plan ID. In this example, we will determine if the user's `default` subscription is actively subscribed to the monthly plan: -->
`subscribedToPlan` 메서드는 특정 Paddle 플랜 ID를 기준으로 사용자가 해당 플랜에 구독되어 있는지 확인할 때 사용할 수 있습니다. 예를 들어, 아래는 사용자의 `default` 구독이 월간 플랜에 활성 구독되어 있는지 확인하는 예시입니다.

```
if ($user->subscribedToPlan($monthly = 12345, 'default')) {
    //
}
```

<!-- By passing an array to the `subscribedToPlan` method, you may determine if the user's `default` subscription is actively subscribed to the monthly or the yearly plan: -->
`subscribedToPlan` 메서드에 배열을 전달하면, 사용자의 `default` 구독이 월간 또는 연간 플랜 중 하나라도 활성으로 구독 중인지 확인할 수 있습니다.

```
if ($user->subscribedToPlan([$monthly = 12345, $yearly = 54321], 'default')) {
    //
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
`recurring` 메서드를 사용하면 사용자가 현재 구독 중이며 체험 기간이 이미 종료되었는지 확인할 수 있습니다.

```
if ($user->subscription('default')->recurring()) {
    //
}
```

<a name="cancelled-subscription-status"></a>
<!-- #### Cancelled Subscription Status -->
#### Cancelled Subscription Status

<!-- To determine if the user was once an active subscriber but has cancelled their subscription, you may use the `cancelled` method: -->
사용자가 한때 활성 구독자였지만 현재 구독을 취소했는지 확인하려면 `cancelled` 메서드를 사용하면 됩니다.

```
if ($user->subscription('default')->cancelled()) {
    //
}
```

<!-- You may also determine if a user has cancelled their subscription, but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
또한 사용자가 구독을 취소했지만, 아직 구독이 완전히 만료되지 않아 "유예 기간(grace period)"에 있는지도 확인할 수 있습니다. 예를 들어, 사용자가 3월 5일에 구독을 취소했지만 원래 만료일이 3월 10일이라면, 3월 10일까지는 유예 기간이 됩니다. 이 기간 동안 `subscribed` 메서드는 계속해서 `true`를 반환합니다.

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- To determine if the user has cancelled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
구독을 취소했고, 더 이상 "유예 기간"도 남아있지 않은 상태인지는 `ended` 메서드로 확인할 수 있습니다.

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="past-due-status"></a>
<!-- #### Past Due Status -->
#### Past Due Status

<!-- If a payment fails for a subscription, it will be marked as `past_due`. When your subscription is in this state it will not be active until the customer has updated their payment information. You may determine if a subscription is past due using the `pastDue` method on the subscription instance: -->
구독 결제가 실패하면 해당 구독은 `past_due` 상태로 표시됩니다. 이 상태에서는 고객이 결제 정보를 업데이트하기 전까지 구독이 활성화되지 않습니다. 구독 인스턴스의 `pastDue` 메서드를 사용해 연체 상태인지 확인할 수 있습니다.

```
if ($user->subscription('default')->pastDue()) {
    //
}
```

<!-- When a subscription is past due, you should instruct the user to [update their payment information](#updating-payment-information). You may configure how past due subscriptions are handled in your [Paddle subscription settings](https://vendors.paddle.com/subscription-settings). -->
구독이 연체 상태일 때, 사용자에게 [update their payment information](#updating-payment-information)를 안내해야 합니다. 연체 구독 처리 방식은 [Paddle subscription settings](https://vendors.paddle.com/subscription-settings)에서 직접 구성할 수도 있습니다.

<!-- If you would like subscriptions to still be considered active when they are `past_due`, you may use the `keepPastDueSubscriptionsActive` method provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
연체(`past_due`) 상태의 구독도 여전히 활성으로 간주하고 싶다면, Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 `AppServiceProvider`의 `register` 메서드에서 호출하면 됩니다.

```
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
```

> [!WARNING]
> 구독이 `past_due` 상태인 동안에는 결제 정보가 갱신되기 전까지 구독을 변경할 수 없습니다. 따라서 구독이 `past_due` 상태일 때 `swap` 및 `updateQuantity` 메서드를 사용하면 예외가 발생합니다.

<a name="subscription-scopes"></a>
<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
대부분의 구독 상태는 쿼리 스코프로도 제공되므로, 데이터베이스에서 특정 상태의 구독을 쉽게 조회할 수 있습니다.

```
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the cancelled subscriptions for a user...
$subscriptions = $user->subscriptions()->cancelled()->get();
```

<!-- A complete list of available scopes is available below: -->
사용 가능한 모든 스코프는 다음과 같습니다.

```
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
```

<a name="subscription-single-charges"></a>
<!-- ### Subscription Single Charges -->
### Subscription Single Charges

<!-- Subscription single charges allow you to charge subscribers with a one-time charge on top of their subscriptions: -->
구독 단일 청구 기능을 사용하면 기존 구독에 일회성 요금을 추가로 청구할 수 있습니다.

```
$response = $user->subscription('default')->charge(12.99, 'Support Add-on');
```

<!-- In contrast to [single charges](#single-charges), this method will immediately charge the customer's stored payment method for the subscription. The charge amount should always be defined in the currency of the subscription. -->
[single charges](#single-charges)와 달리, 이 방식은 구독에 저장된 결제 수단으로 즉시 요금을 청구합니다. 청구 금액은 구독과 동일한 통화 단위로 지정해야 합니다.

<a name="updating-payment-information"></a>
<!-- ### Updating Payment Information -->
### Updating Payment Information

<!-- Paddle always saves a payment method per subscription. If you want to update the default payment method for a subscription, you should first generate a subscription "update URL" using the `updateUrl` method on the subscription model: -->
Paddle은 구독마다 결제 수단을 개별로 저장합니다. 특정 구독의 기본 결제 수단을 변경하려면, 먼저 구독 모델의 `updateUrl` 메서드를 사용해 '구독 업데이트 URL'을 생성해야 합니다.

```
use App\Models\User;

$user = User::find(1);

$updateUrl = $user->subscription('default')->updateUrl();
```

<!-- Then, you may use the generated URL in combination with Cashier's provided `paddle-button` Blade component to allow the user to initiate the Paddle widget and update their payment information: -->
생성된 URL은 Cashier에서 제공하는 `paddle-button` Blade 컴포넌트와 결합해 사용자가 Paddle 위젯을 통해 결제 정보를 직접 수정할 수 있도록 할 수 있습니다.

```html
<x-paddle-button :url="$updateUrl" class="px-8 py-4">
    Update Card
</x-paddle-button>
```

<!-- When a user has finished updating their information, a `subscription_updated` webhook will be dispatched by Paddle and the subscription details will be updated in your application's database. -->
사용자가 정보를 모두 수정하면 Paddle에서 `subscription_updated` 웹훅이 전송되며, 구독 정보가 애플리케이션 데이터베이스에 반영됩니다.

<a name="changing-plans"></a>
<!-- ### Changing Plans -->
### Changing Plans

<!-- After a user has subscribed to your application, they may occasionally want to change to a new subscription plan. To update the subscription plan for a user, you should pass the Paddle plan's identifier to the subscription's `swap` method: -->
사용자가 구독을 시작한 후, 새로운 구독 플랜으로 변경하고 싶을 수 있습니다. 사용자 구독의 플랜을 업데이트하려면, 구독 모델의 `swap` 메서드에 변경할 Paddle 플랜 ID를 전달하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap($premium = 34567);
```

<!-- If you would like to swap plans and immediately invoice the user instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
플랜을 변경하며 바로 청구서를 발행하고 싶다면, 즉시 청구가 발생하도록 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice($premium = 34567);
```

> [!WARNING]
> 체험 기간이 활성화되어 있는 경우에는 플랜을 변경할 수 없습니다. 해당 제약 조건에 대한 상세 내용은 [Paddle documentation](https://developer.paddle.com/api-reference/subscription-api/users/updateuser#usage-notes)를 참고해 주세요.

<a name="prorations"></a>
<!-- #### Prorations -->
#### Prorations

<!-- By default, Paddle prorates charges when swapping between plans. The `noProrate` method may be used to update the subscriptions without prorating the charges: -->
기본적으로 Paddle은 플랜 변경 시 비용을 비례 배분해 계산합니다. 만약 비례 계산 없이 구독을 업데이트하려면 `noProrate` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->noProrate()->swap($premium = 34567);
```

<a name="subscription-quantity"></a>
<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. To easily increment or decrement your subscription's quantity, use the `incrementQuantity` and `decrementQuantity` methods: -->
경우에 따라 구독 요금이 "수량"에 따라 달라질 수 있습니다. 예를 들어, 프로젝트 관리 앱에서 프로젝트당 매월 $10씩 청구하는 경우가 이에 해당합니다. 구독의 수량을 간편하게 증가/감소시키려면 `incrementQuantity`와 `decrementQuantity` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription('default')->decrementQuantity(5);
```

<!-- Alternatively, you may set a specific quantity using the `updateQuantity` method: -->
또는 `updateQuantity` 메서드로 특정 수량을 지정할 수도 있습니다.

```
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
`noProrate` 메서드를 사용해 비례 계산 없이 구독 수량을 업데이트할 수도 있습니다.

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<a name="subscription-modifiers"></a>
<!-- ### Subscription Modifiers -->
### Subscription Modifiers

<!-- Subscription modifiers allow you to implement [metered billing](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers) or extend subscriptions with add-ons. -->
구독 모디파이어를 이용하면 [metered billing](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers)나, 구독에 추가 요소(Add-on)를 더할 수 있습니다.

<!-- For example, you might want to offer a "Premium Support" add-on with your standard subscription. You can create this modifier like so: -->
예를 들어, 표준 구독에 "프리미엄 지원(Premium Support)" 추가 기능을 제공하고 싶다면 아래와 같이 모디파이어를 생성할 수 있습니다.

```
$modifier = $user->subscription('default')->newModifier(12.99)->create();
```

<!-- The example above will add a $12.99 add-on to the subscription. By default, this charge will recur on every interval you have configured for the subscription. If you would like, you can add a readable description to the modifier using the modifier's `description` method: -->
위 예시는 구독에 $12.99짜리 추가 기능을 더하는 예입니다. 기본적으로 이 금액은 구독에 설정된 청구 주기마다 반복해서 청구됩니다. 필요하다면 `description` 메서드로 모디파이어에 설명을 추가할 수도 있습니다.

```
$modifier = $user->subscription('default')->newModifier(12.99)
    ->description('Premium Support')
    ->create();
```

<!-- To illustrate how to implement metered billing using modifiers, imagine your application charges per SMS message sent by the user. First, you should create a $0 plan in your Paddle dashboard. Once the user has been subscribed to this plan, you can add modifiers representing each individual charge to the subscription: -->
계량형 청구를 모디파이어로 구현하는 또 다른 예로, 사용자가 보낸 SMS 한 건당 요금을 청구하는 애플리케이션을 생각해봅시다. Paddle 대시보드에 $0 플랜을 생성하고, 사용자가 이 플랜에 구독한 뒤 각 요금마다 별도의 모디파이어를 추가하는 방식입니다.

```
$modifier = $user->subscription('default')->newModifier(0.99)
    ->description('New text message')
    ->oneTime()
    ->create();
```

<!-- As you can see, we invoked the `oneTime` method when creating this modifier. This method will ensure the modifier is only charged once and does not recur every billing interval. -->
여기서는 `oneTime` 메서드를 사용했습니다. 이 메서드는 해당 모디파이어가 한 번만 청구되고, 이후 반복 청구되지 않도록 합니다.

<a name="retrieving-modifiers"></a>
<!-- #### Retrieving Modifiers -->
#### Retrieving Modifiers

<!-- You may retrieve a list of all modifiers for a subscription via the `modifiers` method: -->
구독에 적용된 모든 모디파이어 목록은 `modifiers` 메서드로 조회할 수 있습니다.

```
$modifiers = $user->subscription('default')->modifiers();

foreach ($modifiers as $modifier) {
    $modifier->amount(); // $0.99
    $modifier->description; // New text message.
}
```

<a name="deleting-modifiers"></a>
<!-- #### Deleting Modifiers -->
#### Deleting Modifiers

<!-- Modifiers may be deleted by invoking the `delete` method on a `Laravel\Paddle\Modifier` instance: -->
`Laravel\Paddle\Modifier` 인스턴스에서 `delete` 메서드를 호출하면 해당 모디파이어를 삭제할 수 있습니다.

```
$modifier->delete();
```

<a name="multiple-subscriptions"></a>
<!-- ### Multiple Subscriptions -->
### Multiple Subscriptions

<!-- Paddle allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans. -->
Paddle은 고객이 동시에 여러 개의 구독을 가질 수 있도록 허용합니다. 예를 들어, 헬스클럽 운영자가 수영장 구독과 헬스장 구독을 각각 별도 가격으로 운영할 수 있습니다. 물론 고객은 두 플랜 중 하나만, 혹은 모두 구독할 수도 있습니다.

<!-- When your application creates subscriptions, you may provide the name of the subscription to the `newSubscription` method. The name may be any string that represents the type of subscription the user is initiating: -->
응용 프로그램에서 구독 생성 시, `newSubscription` 메서드에 구독명을 직접 지정해줄 수 있습니다. 이 이름은 사용자가 시작하려는 구독 종류를 나타내는 임의의 문자열이어도 무방합니다.

```
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()
        ->newSubscription('swimming', $swimmingMonthly = 12345)
        ->create($request->paymentMethodId);

    // ...
});
```

<!-- In this example, we initiated a monthly swimming subscription for the customer. However, they may want to swap to a yearly subscription at a later time. When adjusting the customer's subscription, we can simply swap the price on the `swimming` subscription: -->
위 예시에서는 사용자를 위해 월간 수영 구독을 생성했습니다. 사용자가 나중에 연간 구독으로 전환하고 싶다면, 해당 사용자의 `swimming` 구독에서 요금만 바꿔주면 됩니다.

```
$user->subscription('swimming')->swap($swimmingYearly = 34567);
```

<!-- Of course, you may also cancel the subscription entirely: -->
물론 해당 구독을 아예 취소할 수도 있습니다.

```
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
<!-- ### Pausing Subscriptions -->
### Pausing Subscriptions

<!-- To pause a subscription, call the `pause` method on the user's subscription: -->
구독을 일시적으로 멈추고 싶을 때는 사용자 구독의 `pause` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->pause();
```

<!-- When a subscription is paused, Cashier will automatically set the `paused_from` column in your database. This column is used to know when the `paused` method should begin returning `true`. For example, if a customer pauses a subscription on March 1st, but the subscription was not scheduled to recur until March 5th, the `paused` method will continue to return `false` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
구독이 일시정지되면, Cashier는 데이터베이스의 `paused_from` 컬럼을 자동으로 설정합니다. 이 컬럼은 언제부터 `paused` 메서드가 `true`를 반환해야 할지 판단하는 기준 시점으로 사용됩니다. 예를 들어, 3월 1일에 사용자가 구독 일시정지를 요청했으나 실제 청구 주기가 3월 5일이었다면, `paused` 메서드는 3월 5일까지 `false`를 반환합니다. 대부분의 경우 사용자는 결제 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있기 때문입니다.

<!-- You may determine if a user has paused their subscription but are still on their "grace period" using the `onPausedGracePeriod` method: -->
일시정지됐지만 아직 "유예 기간(grace period)"에 있는지 여부는 `onPausedGracePeriod` 메서드로 확인할 수 있습니다.

```
if ($user->subscription('default')->onPausedGracePeriod()) {
    //
}
```

<!-- To resume a paused a subscription, you may call the `unpause` method on the user's subscription: -->
일시정지된 구독을 다시 활성화(재개)하고 싶다면, `unpause` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->unpause();
```

> [!WARNING]
> 구독이 일시정지된 상태에서는 어떤 변경도 할 수 없습니다. 다른 플랜으로 변경하거나 수량을 업데이트하려면, 먼저 구독을 재개해야 합니다.

<a name="cancelling-subscriptions"></a>
<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
구독을 취소하려면, 사용자 구독의 `cancel` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->cancel();
```

<!-- When a subscription is cancelled, Cashier will automatically set the `ends_at` column in your database. This column is used to know when the `subscribed` method should begin returning `false`. For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
구독이 취소되면, Cashier는 데이터베이스의 `ends_at` 컬럼을 자동으로 갱신합니다. 이 컬럼은 언제부터 `subscribed` 메서드가 `false`를 반환해야 할지 판단하는 데 사용됩니다. 예를 들어, 고객이 3월 1일에 구독을 취소했지만, 실제로 3월 5일에 종료될 예정이었다면, 3월 5일까지는 `subscribed`가 계속 `true`를 반환합니다. 대부분의 경우, 사용자는 결제 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있기 때문입니다.

<!-- You may determine if a user has cancelled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
또한 사용자가 구독을 취소했으나 아직 "유예 기간"에 있는지 `onGracePeriod` 메서드로 확인할 수 있습니다.

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- If you wish to cancel a subscription immediately, you may call the `cancelNow` method on the user's subscription: -->
바로 구독을 즉시 취소하고 싶다면, `cancelNow` 메서드를 사용할 수 있습니다.

```
$user->subscription('default')->cancelNow();
```

> [!WARNING]
> Paddle 구독은 일단 취소하면 다시 재개(resume)할 수 없습니다. 고객이 구독을 재개하고자 할 경우, 반드시 새 구독 생성이 필요합니다.

<a name="subscription-trials"></a>
<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>
<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

> [!WARNING]
> 체험 기간 적용 시 결제 수단을 미리 등록받는 경우, Paddle은 플랜 변경이나 수량 업데이트 등 구독의 모든 변경 작업을 막습니다. 체험 중 플랜을 바꾸고 싶다면 해당 구독을 취소한 뒤 새로 생성해야 합니다.

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscription pay links: -->
체험(Trial) 기간을 제공하면서도 결제 수단을 미리 수집하고자 한다면, 구독 결제 링크 생성 시 `trialDays` 메서드를 활용하세요.

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $monthly = 12345)
                ->returnTo(route('home'))
                ->trialDays(10)
                ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- This method will set the trial period ending date on the subscription record within your application's database, as well as instruct Paddle to not begin billing the customer until after this date. -->
이 방식은 구독 레코드에 체험 종료일을 저장하며, Paddle도 체험 종료일까지는 고객에게 청구하지 않습니다.

> [!WARNING]
> 체험이 끝나기 전에 사용자가 구독을 취소하지 않으면, 체험 종료 즉시 자동으로 과금이 진행됩니다. 반드시 체험 종료일을 사용자에게 미리 안내해 주세요.

<!-- You may determine if the user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
사용자가 체험 기간 내에 있는지 여부는 사용자 인스턴스의 `onTrial` 메서드 또는 구독 인스턴스의 `onTrial` 메서드로 모두 확인할 수 있습니다. 두 방법은 동일한 효과를 가집니다.

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods: -->
기존 체험 기간이 만료됐는지 확인하고 싶을 때는 `hasExpiredTrial` 메서드를 사용합니다.

```
if ($user->hasExpiredTrial('default')) {
    //
}

if ($user->subscription('default')->hasExpiredTrial()) {
    //
}
```

<a name="defining-trial-days-in-paddle-cashier"></a>
<!-- #### Defining Trial Days In Paddle / Cashier -->
#### Defining Trial Days In Paddle / Cashier

<!-- You may choose to define how many trial days your plan's receive in the Paddle dashboard or always pass them explicitly using Cashier. If you choose to define your plan's trial days in Paddle you should be aware that new subscriptions, including new subscriptions for a customer that had a subscription in the past, will always receive a trial period unless you explicitly call the `trialDays(0)` method. -->
플랜별 체험 기간은 Paddle 대시보드에서 설정하거나, Cashier에서 구독 생성 시 항상 명시적으로 지정할 수 있습니다. Paddle 대시보드에 체험 기간을 설정했다면, 신규 구독(이전에 구독한 고객의 신규 구독 포함)에는 항상 체험 기간이 적용됩니다. 체험 없이 바로 구독을 시작하고 싶다면, 반드시 `trialDays(0)` 메서드를 명시적으로 호출해야 합니다.

<a name="without-payment-method-up-front"></a>
<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the customer record attached to your user to your desired trial ending date. This is typically done during user registration: -->
사용자에게 결제 수단을 미리 요구하지 않고도 체험 기간을 제공하고 싶다면, 사용자 레코드에 연결된 고객(Customer) 레코드의 `trial_ends_at` 컬럼을 원하는 체험 종료일로 설정하면 됩니다. 이는 보통 사용자 등록 시 처리합니다.

```
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

<!-- Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the `User` instance will return `true` if the current date is not past the value of `trial_ends_at`: -->
이 방식을 Cashier에서는 "일반 체험(generic trial)"이라 부릅니다. 별도의 구독에 연결된 체험이 아니라서 그렇습니다. `User` 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 값을 지나지 않았다면 `true`를 반환합니다.

```
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
사용자의 실제 구독 생성을 준비가 끝났다면, 기존과 동일하게 `newSubscription` 메서드를 사용해 구독을 생성할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription name parameter if you would like to get the trial ending date for a specific subscription other than the default one: -->
사용자의 체험 종료일을 조회하려면 `trialEndsAt` 메서드를 사용하세요. 사용자가 체험 중이라면 Carbon 날짜 인스턴스를 반환하고, 아니라면 `null`을 반환합니다. 기본 구독 이외의 특정 구독에 대해 체험 종료일을 알고 싶다면, 해당 구독명을 인자로 전달할 수도 있습니다.

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not created an actual subscription yet: -->
"일반 체험(generic trial)" 상태, 즉 실제 구독 없이 고객에만 체험이 설정되어 있는지 알고 싶다면 `onGenericTrial` 메서드를 사용할 수 있습니다.

```
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

> [!WARNING]
> 한 번 생성된 Paddle 구독의 체험 기간은 연장하거나 수정할 수 없습니다.

<a name="handling-paddle-webhooks"></a>
<!-- ## Handling Paddle Webhooks -->
## Handling Paddle Webhooks

<!-- Paddle can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Paddle은 다양한 이벤트가 발생할 때 웹훅을 통해 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier 서비스 제공자가 Cashier의 웹훅 컨트롤러를 가리키는 라우트를 등록합니다. 이 컨트롤러가 모든 웹훅 요청을 처리합니다.

<!-- By default, this controller will automatically handle cancelling subscriptions that have too many failed charges ([as defined by your Paddle dunning settings](https://vendors.paddle.com/recover-settings#dunning-form-id)), subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Paddle webhook event you like. -->
기본적으로 이 컨트롤러는 결제 실패(지나치게 많이 실패한 경우 - [as defined by your Paddle dunning settings](https://vendors.paddle.com/recover-settings#dunning-form-id) 기준), 구독 갱신, 결제 정보 변경 등의 이벤트를 자동으로 처리합니다. 물론 여러분이 원하는 어떤 Paddle 웹훅 이벤트든 컨트롤러를 확장해서 직접 처리할 수도 있습니다.

<!-- To ensure your application can handle Paddle webhooks, be sure to [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/alerts-webhooks). By default, Cashier's webhook controller responds to the `/paddle/webhook` URL path. The full list of all webhooks you should enable in the Paddle control panel are: -->
애플리케이션이 Paddle 웹훅을 올바르게 처리하려면, 반드시 [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/alerts-webhooks)해야 합니다. Cashier의 기본 웹훅 컨트롤러는 `/paddle/webhook` 경로를 사용합니다. Paddle 관리 패널에서 활성화해야 하는 모든 웹훅 목록은 아래와 같습니다.

<!--
- Subscription Created
- Subscription Updated
- Subscription Cancelled
- Payment Succeeded
- Subscription Payment Succeeded
-->
- Subscription Created
- Subscription Updated
- Subscription Cancelled
- Payment Succeeded
- Subscription Payment Succeeded

> [!WARNING]
> 웹훅 요청이 Cashier에 포함된 [webhook signature verification](/docs/9.x/cashier-paddle#verifying-webhook-signatures) 미들웨어로 보호되고 있는지 반드시 확인하세요.

<a name="webhooks-csrf-protection"></a>

<!-- #### Webhooks & CSRF Protection -->
#### Webhooks & CSRF Protection

<!-- Since Paddle webhooks need to bypass Laravel's [CSRF protection](/docs/9.x/csrf), be sure to list the URI as an exception in your `App\Http\Middleware\VerifyCsrfToken` middleware or list the route outside of the `web` middleware group: -->
Paddle 웹훅은 Laravel의 [CSRF protection](/docs/9.x/csrf)를 우회해야 하므로, `App\Http\Middleware\VerifyCsrfToken` 미들웨어에서 해당 URI를 예외 목록에 등록하거나 해당 라우트를 `web` 미들웨어 그룹 외부에서 정의해야 합니다.

```
protected $except = [
    'paddle/*',
];
```

<a name="webhooks-local-development"></a>
<!-- #### Webhooks & Local Development -->
#### Webhooks & Local Development

<!-- For Paddle to be able to send your application webhooks during local development, you will need to expose your application via a site sharing service such as [Ngrok](https://ngrok.com/) or [Expose](https://expose.dev/docs/introduction). If you are developing your application locally using [Laravel Sail](/docs/9.x/sail), you may use Sail's [site sharing command](/docs/9.x/sail#sharing-your-site). -->
Paddle이 로컬 개발 환경에서 애플리케이션으로 웹훅을 전송할 수 있도록 하려면 [Ngrok](https://ngrok.com/) 또는 [Expose](https://expose.dev/docs/introduction)와 같은 사이트 공유 서비스를 통해 애플리케이션을 외부에 노출해야 합니다. [Laravel Sail](/docs/9.x/sail)을 이용해 로컬에서 개발 중이라면, Sail의 [site sharing command](/docs/9.x/sail#sharing-your-site)를 사용할 수도 있습니다.

<a name="defining-webhook-event-handlers"></a>
<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancellation on failed charges and other common Paddle webhooks. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier는 결제 실패 시 구독 취소 등과 같은 일반적인 Paddle 웹훅을 자동으로 처리합니다. 그러나 추가적으로 처리하고 싶은 웹훅 이벤트가 있다면, Cashier에서 발생시키는 아래 이벤트를 리스닝하여 직접 처리할 수 있습니다.

<!--
- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`
-->
- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

<!-- Both events contain the full payload of the Paddle webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/9.x/events#defining-listeners) that will handle the event: -->
이 이벤트들은 모두 Paddle 웹훅의 전체 페이로드를 포함합니다. 예를 들어, `invoice.payment_succeeded` 웹훅을 처리하고 싶다면, 아래와 같이 [listener](/docs/9.x/events#defining-listeners)를 등록할 수 있습니다.

```
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
```

<!-- Once your listener has been defined, you may register it within your application's `EventServiceProvider`: -->
리스너를 정의한 후에는, 애플리케이션의 `EventServiceProvider`에 등록해야 합니다.

```
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
```

<!-- Cashier also emit events dedicated to the type of the received webhook. In addition to the full payload from Paddle, they also contain the relevant models that were used to process the webhook such as the billable model, the subscription, or the receipt: -->
Cashier는 수신된 웹훅의 종류에 따라 전용 이벤트도 발생시킵니다. 이들 이벤트에는 Paddle에서 받은 전체 페이로드뿐 아니라, 웹훅 처리 시 사용된 관련 모델(청구 모델, 구독, 영수증 등)도 함께 전달됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`
-->
- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`

<!-- </div> -->
</div>

<!-- You can also override the default, built-in webhook route by defining the `CASHIER_WEBHOOK` environment variable in your application's `.env` file. This value should be the full URL to your webhook route and needs to match the URL set in your Paddle control panel: -->
기본 내장 웹훅 라우트를 오버라이드하고 싶다면, 애플리케이션의 `.env` 파일에서 `CASHIER_WEBHOOK` 환경 변수를 정의하면 됩니다. 이 값은 반드시 전체 웹훅 라우트 URL이어야 하며, Paddle 관리 패널에 등록된 URL과 일치해야 합니다.

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
<!-- ### Verifying Webhook Signatures -->
### Verifying Webhook Signatures

<!-- To secure your webhooks, you may use [Paddle's webhook signatures](https://developer.paddle.com/webhook-reference/verifying-webhooks). For convenience, Cashier automatically includes a middleware which validates that the incoming Paddle webhook request is valid. -->
웹훅을 보호하기 위해 [Paddle's webhook signatures](https://developer.paddle.com/webhook-reference/verifying-webhooks)을 활용할 수 있습니다. Cashier는 Paddle에서 수신한 웹훅 요청이 유효한지 자동으로 검증해 주는 미들웨어를 포함하고 있습니다.

<!-- To enable webhook verification, ensure that the `PADDLE_PUBLIC_KEY` environment variable is defined in your application's `.env` file. The public key may be retrieved from your Paddle account dashboard. -->
웹훅 검증을 활성화하려면, 애플리케이션의 `.env` 파일에 `PADDLE_PUBLIC_KEY` 환경 변수를 반드시 정의해야 합니다. 공개 키는 Paddle 계정 대시보드에서 가져올 수 있습니다.

<a name="single-charges"></a>
<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>
<!-- ### Simple Charge -->
### Simple Charge

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance to generate a pay link for the charge. The `charge` method accepts the charge amount (float) as its first argument and a charge description as its second argument: -->
고객에게 단회성 결제를 진행하고 싶다면, 청구 가능한 모델 인스턴스에서 `charge` 메서드를 사용하여 결제용 페이 링크(pay link)를 만들 수 있습니다. `charge` 메서드의 첫 번째 인수로는 결제 금액(float), 두 번째 인수로는 결제 설명을 입력합니다.

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $user->charge(12.99, 'Action Figure')
    ]);
});
```

<!-- After generating the pay link, you may use Cashier's provided `paddle-button` Blade component to allow the user to initiate the Paddle widget and complete the charge: -->
페이 링크를 생성한 후에는 Cashier에서 제공하는 `paddle-button` Blade 컴포넌트를 사용하여 사용자가 Paddle 위젯을 실행하고 결제를 마칠 수 있도록 할 수 있습니다.

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

<!-- The `charge` method accepts an array as its third argument, allowing you to pass any options you wish to the underlying Paddle pay link creation. Please consult [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) to learn more about the options available to you when creating charges: -->
`charge` 메서드는 세 번째 인수로 배열을 받아, Paddle에게 결제 링크 생성 시 원하는 다양한 옵션을 전달할 수 있습니다. 사용할 수 있는 옵션에 관한 자세한 내용은 [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요.

```
$payLink = $user->charge(12.99, 'Action Figure', [
    'custom_option' => $value,
]);
```

<!-- Charges happen in the currency specified in the `cashier.currency` configuration option. By default, this is set to USD. You may override the default currency by defining the `CASHIER_CURRENCY` environment variable in your application's `.env` file: -->
결제는 `cashier.currency` 설정 옵션에 명시된 통화 단위로 이루어집니다. 기본 값은 USD입니다. 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정하여 기본 통화 단위를 변경할 수 있습니다.

```ini
CASHIER_CURRENCY=EUR
```

<!-- You can also [override prices per currency](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink#price-overrides) using Paddle's dynamic pricing matching system. To do so, pass an array of prices instead of a fixed amount: -->
또한, Paddle의 동적 가격 매칭 시스템을 이용해 [override prices per currency](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink#price-overrides)할 수도 있습니다. 이 경우 고정 금액 대신 통화별 가격 배열을 전달합니다.

```
$payLink = $user->charge([
    'USD:19.99',
    'EUR:15.99',
], 'Action Figure');
```

<a name="charging-products"></a>
<!-- ### Charging Products -->
### Charging Products

<!-- If you would like to make a one-time charge against a specific product configured within Paddle, you may use the `chargeProduct` method on a billable model instance to generate a pay link: -->
Paddle에 미리 등록된 특정 상품에 대해 단회성 결제를 진행하고 싶다면, 청구 가능한 모델 인스턴스의 `chargeProduct` 메서드를 사용해 페이 링크를 생성할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $request->user()->chargeProduct($productId = 123)
    ]);
});
```

<!-- Then, you may provide the pay link to the `paddle-button` component to allow the user to initialize the Paddle widget: -->
이후, `paddle-button` 컴포넌트에 해당 페이 링크를 넘겨 사용자가 Paddle 위젯을 실행할 수 있도록 하면 됩니다.

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

<!-- The `chargeProduct` method accepts an array as its second argument, allowing you to pass any options you wish to the underlying Paddle pay link creation. Please consult [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) regarding the options that are available to you when creating charges: -->
`chargeProduct` 메서드 역시 두 번째 인수로 배열을 받을 수 있어, Paddle 결제 링크 생성 시 다양한 옵션을 전달할 수 있습니다. 옵션 관련 사항은 [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요.

```
$payLink = $user->chargeProduct($productId, [
    'custom_option' => $value,
]);
```

<a name="refunding-orders"></a>
<!-- ### Refunding Orders -->
### Refunding Orders

<!-- If you need to refund a Paddle order, you may use the `refund` method. This method accepts the Paddle order ID as its first argument. You may retrieve the receipts for a given billable model using the `receipts` method: -->
Paddle 주문을 환불할 필요가 있다면, `refund` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 Paddle 주문 ID를 받습니다. 청구 가능한 모델에 대한 영수증은 `receipts` 메서드로 조회할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$receipt = $user->receipts()->first();

$refundRequestId = $user->refund($receipt->order_id);
```

<!-- You may optionally specify a specific amount to refund as well as a reason for the refund: -->
환불 금액이나 환불 사유를 별도로 지정할 수도 있습니다.

```
$receipt = $user->receipts()->first();

$refundRequestId = $user->refund(
    $receipt->order_id, 5.00, 'Unused product time'
);
```

> [!NOTE]
> Paddle 지원팀에 문의 시 `$refundRequestId`를 환불 참조값으로 사용할 수 있습니다.

<a name="receipts"></a>
<!-- ## Receipts -->
## Receipts

<!-- You may easily retrieve an array of a billable model's receipts via the `receipts` property: -->
청구 가능한 모델의 영수증 배열은 `receipts` 프로퍼티를 통해 쉽게 조회할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$receipts = $user->receipts;
```

<!-- When listing the receipts for the customer, you may use the receipt instance's methods to display the relevant receipt information. For example, you may wish to list every receipt in a table, allowing the user to easily download any of the receipts: -->
고객의 영수증을 나열할 때는 각 영수증 인스턴스의 메서드를 이용해 표시할 정보를 불러올 수 있습니다. 예를 들어, 모든 영수증을 표로 나열하고 사용자가 원하는 영수증을 바로 다운로드할 수 있도록 할 수 있습니다.

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
<!-- ### Past & Upcoming Payments -->
### Past & Upcoming Payments

<!-- You may use the `lastPayment` and `nextPayment` methods to retrieve and display a customer's past or upcoming payments for recurring subscriptions: -->
`lastPayment`와 `nextPayment` 메서드를 사용하여 반복 구독에 대한 고객의 과거 및 예정 결제 내역을 조회하고 표시할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription('default');

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

<!-- Both of these methods will return an instance of `Laravel\Paddle\Payment`; however, `nextPayment` will return `null` when the billing cycle has ended (such as when a subscription has been cancelled): -->
이 두 메서드는 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 단, 구독이 해지되어 결제 주기가 끝난 경우 `nextPayment`는 `null`을 반환합니다.

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="handling-failed-payments"></a>
<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Subscription payments fail for various reasons, such as expired cards or a card having insufficient funds. When this happens, we recommend that you let Paddle handle payment failures for you. Specifically, you may [setup Paddle's automatic billing emails](https://vendors.paddle.com/subscription-settings) in your Paddle dashboard. -->
구독 결제는 카드 만료, 한도 초과 등 다양한 원인으로 실패할 수 있습니다. 이런 경우에는 Paddle에서 결제 실패 처리를 담당하도록 하는 것이 좋습니다. Paddle 대시보드에서 [setup Paddle's automatic billing emails](https://vendors.paddle.com/subscription-settings) 설정을 통해 처리할 수 있습니다.

<!-- Alternatively, you can perform more precise customization by [listening](/docs/9.x/events) for the `subscription_payment_failed` Paddle event via the `WebhookReceived` event dispatched by Cashier. You should also ensure the "Subscription Payment Failed" option is enabled in the Webhook settings of your Paddle dashboard: -->
그리고, 더 세밀한 제어가 필요하다면 Cashier에서 디스패치하는 `WebhookReceived` 이벤트를 [listening](/docs/9.x/events)하여 `subscription_payment_failed` Paddle 이벤트를 직접 처리할 수도 있습니다. Paddle 대시보드의 Webhook 설정에서 "Subscription Payment Failed" 옵션이 활성화되어 있는지도 확인하세요.

```
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
```

<!-- Once your listener has been defined, you should register it within your application's `EventServiceProvider`: -->
리스너를 정의한 뒤에는, 애플리케이션의 `EventServiceProvider`에 반드시 등록해야 합니다.

```
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
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- While testing, you should manually test your billing flow to make sure your integration works as expected. -->
빌링(Billing) 플로우의 예상 동작을 확인하려면 실제로 수동 테스트를 하는 것이 좋습니다.

<!-- For automated tests, including those executed within a CI environment, you may use [Laravel's HTTP Client](/docs/9.x/http-client#testing) to fake HTTP calls made to Paddle. Although this does not test the actual responses from Paddle, it does provide a way to test your application without actually calling Paddle's API. -->
CI 환경 등 자동화된 테스트에서는 [Laravel's HTTP Client](/docs/9.x/http-client#testing)를 이용해 Paddle로 보내는 HTTP 요청을 페이크로 처리할 수 있습니다. 이 방식은 실제 Paddle의 응답을 테스트하지는 않지만, Paddle API를 호출하지 않고 애플리케이션 동작을 검증하는 데 유용하게 활용할 수 있습니다.