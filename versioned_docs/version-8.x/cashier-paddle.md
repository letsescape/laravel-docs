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
[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle's](https://paddle.com)의 구독 과금 서비스를 직관적이고 쉽게 사용할 수 있는 인터페이스로 제공합니다. 번거로운 구독 과금 관련 반복 코드를 거의 모두 알아서 처리합니다. 기본적인 구독 관리 외에도, Cashier는 쿠폰, 구독 플랜 변경, 구독 "수량(Quantity)", 구독 취소 유예 기간 등 다양한 기능도 제공합니다.

<!-- While working with Cashier we recommend you also review Paddle's [user guides](https://developer.paddle.com/guides) and [API documentation](https://developer.paddle.com/api-reference/intro). -->
Cashier를 사용할 때에는 Paddle의 [user guides](https://developer.paddle.com/guides)와 [API documentation](https://developer.paddle.com/api-reference/intro)도 함께 참고하시기를 권장합니다.

<a name="upgrading-cashier"></a>
<!-- ## Upgrading Cashier -->
## Upgrading Cashier

<!-- When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md). -->
Cashier의 새로운 버전으로 업그레이드할 때는 [the upgrade guide](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 반드시 꼼꼼히 확인해야 합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install the Cashier package for Paddle using the Composer package manager: -->
먼저, Composer 패키지 관리자를 사용하여 Paddle용 Cashier 패키지를 설치합니다.

```
composer require laravel/cashier-paddle
```

> [!NOTE]
> Cashier가 모든 Paddle 이벤트를 제대로 처리할 수 있도록, 반드시 [set up Cashier's webhook handling](#handling-paddle-webhooks)를 설정해두어야 합니다.

<a name="paddle-sandbox"></a>
<!-- ### Paddle Sandbox -->
### Paddle Sandbox

<!-- During local and staging development, you should [register a Paddle Sandbox account](https://developer.paddle.com/getting-started/sandbox). This account will give you a sandboxed environment to test and develop your applications without making actual payments. You may use Paddle's [test card numbers](https://developer.paddle.com/getting-started/sandbox#test-cards) to simulate various payment scenarios. -->
로컬 혹은 스테이징 개발 단계에서는 반드시 [register a Paddle Sandbox account](https://developer.paddle.com/getting-started/sandbox)을 등록하세요. 이 계정을 사용하면 실제 결제가 발생하지 않는 샌드박스 환경에서 안전하게 애플리케이션을 테스트하고 개발할 수 있습니다. 다양한 결제 상황을 시뮬레이션하려면 Paddle의 [test card numbers](https://developer.paddle.com/getting-started/sandbox#test-cards)를 사용할 수 있습니다.

<!-- When using the Paddle Sandbox environment, you should set the `PADDLE_SANDBOX` environment variable to `true` within your application's `.env` file: -->
Paddle 샌드박스 환경을 사용 중이라면, 애플리케이션의 `.env` 파일에서 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다.

<!-- PADDLE_SANDBOX=true -->
PADDLE_SANDBOX=true

<!-- After you have finished developing your application you may [apply for a Paddle vendor account](https://paddle.com). -->
애플리케이션 개발을 마쳤다면 [apply for a Paddle vendor account](https://paddle.com)을 신청할 수 있습니다.

<a name="database-migrations"></a>
<!-- ### Database Migrations -->
### Database Migrations

<!-- The Cashier service provider registers its own database migration directory, so remember to migrate your database after installing the package. The Cashier migrations will create a new `customers` table. In addition, a new `subscriptions` table will be created to store all of your customer's subscriptions. Finally, a new `receipts` table will be created to store all of your application's receipt information: -->
Cashier 서비스 프로바이더는 자체 마이그레이션 디렉터리를 등록합니다. 패키지 설치 후 반드시 데이터베이스 마이그레이션을 실행하세요. Cashier가 제공하는 마이그레이션은 새로운 `customers` 테이블을 생성합니다. 또한, 모든 고객의 구독 정보를 저장하는 `subscriptions` 테이블, 애플리케이션의 영수증 정보를 관리하는 `receipts` 테이블도 함께 생성됩니다.

```
php artisan migrate
```

<!-- If you need to overwrite the migrations that are included with Cashier, you can publish them using the `vendor:publish` Artisan command: -->
Cashier에서 제공하는 기본 마이그레이션 파일을 덮어써야 한다면, `vendor:publish` Artisan 명령어로 마이그레이션 파일을 퍼블리시할 수 있습니다.

```
php artisan vendor:publish --tag="cashier-migrations"
```

<!-- If you would like to prevent Cashier's migrations from running entirely, you may use the `ignoreMigrations` provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
반대로, Cashier가 제공하는 마이그레이션을 아예 실행하지 않을 수도 있습니다. 이 경우, Cashier에서 제공하는 `ignoreMigrations` 메서드를 사용할 수 있습니다. 일반적으로, 이 메서드는 `AppServiceProvider`의 `register` 메서드에서 호출합니다.

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
Cashier를 사용하기 전에 반드시 사용자(User) 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트를 추가하면 구독 생성, 쿠폰 적용, 결제 수단 정보 갱신 등 다양한 과금 관련 작업을 쉽게 수행할 수 있습니다.

```
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

<!-- If you have billable entities that are not users, you may also add the trait to those classes: -->
사용자가 아닌 다른 엔터티(예: 팀 등)도 과금 대상으로 만들고 싶다면, 해당 클래스에 이 트레이트를 추가하면 됩니다.

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
다음으로, Paddle 키 정보를 애플리케이션의 `.env` 파일에 설정해야 합니다. Paddle API 키는 Paddle 관리 콘솔에서 확인할 수 있습니다.

```
PADDLE_VENDOR_ID=your-paddle-vendor-id
PADDLE_VENDOR_AUTH_CODE=your-paddle-vendor-auth-code
PADDLE_PUBLIC_KEY="your-paddle-public-key"
PADDLE_SANDBOX=true
```

<!-- The `PADDLE_SANDBOX` environment variable should be set to `true` when you are using [Paddle's Sandbox environment](#paddle-sandbox). The `PADDLE_SANDBOX` variable should be set to `false` if you are deploying your application to production and are using Paddle's live vendor environment. -->
`PADDLE_SANDBOX` 환경 변수는 [Paddle's Sandbox environment](#paddle-sandbox) 사용 시 `true`로 설정해야 합니다. 운영 환경(프로덕션)에서 Paddle의 실제 벤더 환경을 사용할 때에는 `PADDLE_SANDBOX` 값을 `false`로 변경해야 합니다.

<a name="paddle-js"></a>
<!-- ### Paddle JS -->
### Paddle JS

<!-- Paddle relies on its own JavaScript library to initiate the Paddle checkout widget. You can load the JavaScript library by placing the `@paddleJS` Blade directive right before your application layout's closing `</head>` tag: -->
Paddle의 결제 위젯을 띄우려면 전용 자바스크립트 라이브러리를 로드해야 합니다. 이 라이브러리는 애플리케이션 레이아웃의 `</head>` 태그 바로 앞에 `@paddleJS` Blade 디렉티브를 삽입하면 자동으로 로드할 수 있습니다.

```
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
<!-- ### Currency Configuration -->
### Currency Configuration

<!-- The default Cashier currency is United States Dollars (USD). You can change the default currency by defining a `CASHIER_CURRENCY` environment variable within your application's `.env` file: -->
Cashier는 기본적으로 미국 달러(USD)를 통화로 사용합니다. 다른 통화를 기본값으로 사용하려면, `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 추가하세요.

```
CASHIER_CURRENCY=EUR
```

<!-- In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale: -->
통화 외에도, 청구서에 표시될 금액의 로캘(언어 및 지역)을 설정할 수도 있습니다. 내부적으로 Cashier는 [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php)를 통해 금액 로캘을 지정합니다.

```
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!NOTE]
> `en`(영어) 외의 로캘을 사용하려면, 서버에 `ext-intl` PHP 확장 모듈이 설치 및 구성되어 있어야 합니다.

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model: -->
Cashier 내부에서 사용하는 모델을 직접 확장하여 원하는 방식(필드 추가 등)으로 정의할 수 있습니다. Cashier 모델을 상속받아 새 모델을 만든 후, Cashier에 이를 사용하도록 지정만 하면 됩니다.

```
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

<!-- After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Paddle\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
모델을 정의했다면, `Laravel\Paddle\Cashier` 클래스의 메서드로 커스텀 모델을 Cashier에 등록하세요. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 지정합니다.

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
Paddle은 구독 상태를 변경하는 전용 CRUD API가 충분하지 않습니다. 그래서 대부분의 Paddle과의 상호작용은 [checkout widget](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout)을 통해 이루어집니다. 결제 위젯을 띄우려면 먼저 Cashier를 사용해 "페이 링크(pay link)"를 발급받아야 합니다. 이 페이 링크는 어떤 과금 작업을 할지 결제 위젯에 알려주는 역할을 합니다.

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

<!-- Cashier includes a `paddle-button` [Blade component](/docs/8.x/blade#components). We may pass the pay link URL to this component as a "prop". When this button is clicked, Paddle's checkout widget will be displayed: -->
Cashier에는 `paddle-button` [Blade component](/docs/8.x/blade#components)가 준비되어 있습니다. 이 컴포넌트의 prop으로 페이 링크 URL을 전달하면, 버튼 클릭 시 Paddle 결제 위젯이 자동으로 나타납니다.

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- By default, this will display a button with the standard Paddle styling. You can remove all Paddle styling by adding the `data-theme="none"` attribute to the component: -->
기본적으로 이 버튼에는 표준 Paddle 스타일이 적용됩니다. 모든 Paddle 스타일을 제거하고 싶다면, 컴포넌트에 `data-theme="none"` 속성을 추가하면 됩니다.

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="none">
    Subscribe
</x-paddle-button>
```

<!-- The Paddle checkout widget is asynchronous. Once the user creates or updates a subscription within the widget, Paddle will send your application webhooks so that you may properly update the subscription state in our own database. Therefore, it's important that you properly [set up webhooks](#handling-paddle-webhooks) to accommodate for state changes from Paddle. -->
Paddle 결제 위젯은 비동기적으로 동작합니다. 사용자가 위젯에서 구독을 생성하거나 수정하면, Paddle은 웹훅(Webhook)을 여러분의 애플리케이션으로 전송하여 데이터베이스에 올바르게 구독 상태를 반영할 수 있도록 도와줍니다. 따라서 Paddle에서의 상태 변경을 반영하려면 반드시 [set up webhooks](#handling-paddle-webhooks)를 올바르게 설정해 두어야 합니다.

<!-- For more information on pay links, you may review [the Paddle API documentation on pay link generation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink). -->
페이 링크에 대한 더 자세한 정보는 [the Paddle API documentation on pay link generation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)에서 확인하실 수 있습니다.

> [!NOTE]
> 구독 상태 변경 이후 해당 웹훅을 수신하기까지는 일반적으로 딜레이가 거의 없지만, 결제가 끝난 즉시 구독 정보가 바로 반영되지 않을 수도 있음을 염두에 두어야 합니다.

<a name="manually-rendering-pay-links"></a>
<!-- #### Manually Rendering Pay Links -->
#### Manually Rendering Pay Links

<!-- You may also manually render a pay link without using Laravel's built-in Blade components. To get started, generate the pay link URL as demonstrated in previous examples: -->
Laravel의 기본 제공 Blade 컴포넌트를 사용하지 않아도, 페이 링크를 직접 HTML에 연결할 수 있습니다. 먼저, 이전 예시처럼 페이 링크 URL을 생성합니다.

```
$payLink = $request->user()->newSubscription('default', $premium = 34567)
    ->returnTo(route('home'))
    ->create();
```

<!-- Next, simply attach the pay link URL to an `a` element in your HTML: -->
그런 다음, 생성된 페이 링크 URL을 HTML의 `a` 요소에 단순히 연결하여 사용할 수 있습니다.

```
<a href="#!" class="ml-4 paddle_button" data-override="{{ $payLink }}">
    Paddle Checkout
</a>
```

<a name="payments-requiring-additional-confirmation"></a>
<!-- #### Payments Requiring Additional Confirmation -->
#### Payments Requiring Additional Confirmation

<!-- Sometimes additional verification is required in order to confirm and process a payment. When this happens, Paddle will present a payment confirmation screen. Payment confirmation screens presented by Paddle or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification. -->
일부 결제의 경우, 추가적인 확인 절차가 필요할 수 있습니다. 이럴 때 Paddle은 별도의 결제 확인 화면을 보여줍니다. Paddle이 보여주는 결제 확인 화면은, 결제 은행 또는 카드사에 따라 추가 카드 인증, 임시 소액 청구, 별도 디바이스 인증 등 여러 종류가 있을 수 있습니다.

<a name="inline-checkout"></a>
<!-- ### Inline Checkout -->
### Inline Checkout

<!-- If you don't want to make use of Paddle's "overlay" style checkout widget, Paddle also provides the option to display the widget inline. While this approach does not allow you to adjust any of the checkout's HTML fields, it allows you to embed the widget within your application. -->
Paddle의 "오버레이" 스타일 결제 위젯 대신, 위젯을 인라인으로 페이지 내에 직접 표시할 수도 있습니다. 이 방식은 결제 위젯의 HTML 필드를 커스터마이즈할 수는 없지만, 애플리케이션 내부에 바로 임베드해서 사용할 수 있습니다.

<!-- To make it easy for you to get started with inline checkout, Cashier includes a `paddle-checkout` Blade component. To get started, you should [generate a pay link](#pay-links) and pass the pay link to the component's `override` attribute: -->
Cashier는 인라인 결제를 쉽게 구현할 수 있는 `paddle-checkout` Blade 컴포넌트를 지원합니다. [generate a pay link](#pay-links)한 뒤, 이 컴포넌트의 `override` 속성에 페이 링크를 전달하세요.

```html
<x-paddle-checkout :override="$payLink" class="w-full" />
```

<!-- To adjust the height of the inline checkout component, you may pass the `height` attribute to the Blade component: -->
인라인 결제 컴포넌트의 높이를 조정하려면 `height` 속성을 추가하면 됩니다.

```
<x-paddle-checkout :override="$payLink" class="w-full" height="500" />
```

<a name="inline-checkout-without-pay-links"></a>
<!-- #### Inline Checkout Without Pay Links -->
#### Inline Checkout Without Pay Links

<!-- Alternatively, you may customize the widget with custom options instead of using a pay link: -->
페이 링크를 사용하지 않고, 사용자 정의 옵션을 지정하여 위젯을 커스터마이즈할 수도 있습니다.

```
$options = [
    'product' => $productId,
    'title' => 'Product Title',
];

<x-paddle-checkout :options="$options" class="w-full" />
```

<!-- Please consult Paddle's [guide on Inline Checkout](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout) as well as their [parameter reference](https://developer.paddle.com/reference/paddle-js/parameters) for further details on the inline checkout's available options. -->
인라인 결제에서 사용할 수 있는 옵션에 대한 자세한 내용은 Paddle의 [guide on Inline Checkout](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout)와 [parameter reference](https://developer.paddle.com/reference/paddle-js/parameters)를 참고하세요.

> [!NOTE]
> 직접 옵션을 지정하여 `passthrough`(임의 데이터 전달)를 사용하려면, 키/값 배열을 값으로 넘기면 됩니다. Cashier가 자동으로 배열을 JSON 문자열로 변환해줍니다. 참고로, `customer_id` passthrough 옵션은 Cashier 내부적으로 사용되므로, 별도 지정하지 않아야 합니다.

<a name="manually-rendering-an-inline-checkout"></a>
<!-- #### Manually Rendering An Inline Checkout -->
#### Manually Rendering An Inline Checkout

<!-- You may also manually render an inline checkout without using Laravel's built-in Blade components. To get started, generate the pay link URL [as demonstrated in previous examples](#pay-links). -->
Laravel의 Blade 컴포넌트를 사용하지 않고 인라인 결제를 직접 구현할 수도 있습니다. [as demonstrated in previous examples](#pay-links)하세요.

<!-- Next, you may use Paddle.js to initialize the checkout. To keep this example simple, we will demonstrate this using [Alpine.js](https://github.com/alpinejs/alpine); however, you are free to translate this example to your own frontend stack: -->
그다음, Paddle.js를 사용해서 결제 위젯을 초기화할 수 있습니다. 아래 예시는 [Alpine.js](https://github.com/alpinejs/alpine)를 이용한 것이지만, 여러분의 프론트엔드 환경에 맞게 참고해 구현 가능합니다.

```html
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
Stripe와는 다르게, Paddle의 사용자는 모든 Paddle 전체에서 고유합니다. 즉, 각 Paddle 계정별로 고유한 사용자가 존재하지 않습니다. 이런 구조 때문에, Paddle의 API는 현재 사용자의 이메일 주소 등 세부 정보를 수정할 수 없습니다. 페이 링크 생성 시 Paddle은 `customer_email` 파라미터로 사용자를 식별하며, 구독 생성 시에도 입력받은 이메일을 이미 등록된 Paddle 사용자와 매칭하려 시도합니다.

<!-- In light of this behavior, there are some important things to keep in mind when using Cashier and Paddle. First, you should be aware that even though subscriptions in Cashier are tied to the same application user, **they could be tied to different users within Paddle's internal systems**. Secondly, each subscription has its own connected payment method information and could also have different email addresses within Paddle's internal systems (depending on which email was assigned to the user when the subscription was created). -->
이런 특성 때문에 Cashier와 Paddle을 사용할 때 반드시 주의해야 할 점이 있습니다. 첫째, Cashier에서는 같은 애플리케이션 사용자와 구독이 연결되어 있어도, **내부적으로 Paddle에서는 각기 다른 사용자(이메일 등)와 매칭될 수 있습니다.** 둘째, 구독마다 개별 결제 수단이나 이메일 주소가 따로 지정될 수 있습니다(Paddle에서 구독 생성 당시의 이메일이 그대로 사용됨).

<!-- Therefore, when displaying subscriptions you should always inform the user which email address or payment method information is connected to the subscription on a per-subscription basis. Retrieving this information can be done with the following methods provided by the `Laravel\Paddle\Subscription` model: -->
따라서 구독 정보를 사용자에게 보여줄 때에는, 구독별로 어떤 이메일과 결제 정보가 연결되어 있는지를 반드시 안내해야 합니다. 아래와 같이 `Laravel\Paddle\Subscription` 모델이 제공하는 메서드로 이 정보를 확인할 수 있습니다.

```
$subscription = $user->subscription('default');

$subscription->paddleEmail();
$subscription->paymentMethod();
$subscription->cardBrand();
$subscription->cardLastFour();
$subscription->cardExpirationDate();
```

<!-- There is currently no way to modify a user's email address through the Paddle API. When a user wants to update their email address within Paddle, the only way for them to do so is to contact Paddle customer support. When communicating with Paddle, they need to provide the `paddleEmail` value of the subscription to assist Paddle in updating the correct user. -->
현재 Paddle API를 통해 사용자의 이메일 주소를 직접 변경할 방법은 없습니다. 사용자가 Paddle 내에서 이메일을 바꾸고 싶은 경우, Paddle 고객 지원팀에 직접 문의해야 합니다. 이때, 올바른 사용자를 식별하기 위해 해당 구독의 `paddleEmail` 값을 Paddle 측에 전달해야 합니다.

<a name="prices"></a>
<!-- ## Prices -->
## Prices

<!-- Paddle allows you to customize prices per currency, essentially allowing you to configure different prices for different countries. Cashier Paddle allows you to retrieve all of the prices for a given product using the `productPrices` method. This method accepts the product IDs of the products you wish to retrieve prices for: -->
Paddle은 통화별로 가격을 다르게 설정할 수 있어, 국가별로 서로 다른 가격을 지정하는 것이 가능합니다. Cashier Paddle은 `productPrices` 메서드로 특정 상품의 모든 가격 정보를 가져올 수 있습니다. 이 메서드에는 가격을 확인하고 싶은 상품 ID 배열을 전달합니다.

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456]);
```

<!-- The currency will be determined based on the IP address of the request; however, you may optionally provide a specific country to retrieve prices for: -->
통화는 요청의 IP 주소를 기준으로 결정되지만, 원한다면 가격을 조회할 특정 국가를 직접 지정할 수도 있습니다.

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], ['customer_country' => 'BE']);
```

<!-- After retrieving the prices you may display them however you wish: -->
가져온 가격 정보는 원하는 형태로 출력할 수 있습니다.

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

<!-- You may also display the net price (excludes tax) and display the tax amount separately: -->
세금이 빠진 실제 가격(순액) 및 세금 금액만 분리해서 보여줄 수도 있습니다.

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->net() }} (+ {{ $price->price()->tax() }} tax)</li>
    @endforeach
</ul>
```

<!-- If you retrieved prices for subscription plans you can display their initial and recurring price separately: -->
구독 플랜의 가격을 가져온 경우, 최초 결제료와 반복 결제료를 별도로 표시할 수 있습니다.

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - Initial: {{ $price->initialPrice()->gross() }} - Recurring: {{ $price->recurringPrice()->gross() }}</li>
    @endforeach
</ul>
```

<!-- For more information, [check Paddle's API documentation on prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices). -->
자세한 내용은 [check Paddle's API documentation on prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)를 참고하세요.

<a name="prices-customers"></a>
<!-- #### Customers -->
#### Customers

<!-- If a user is already a customer and you would like to display the prices that apply to that customer, you may do so by retrieving the prices directly from the customer instance: -->
이미 고객으로 등록된 사용자가 있고 그 고객에게 적용되는 가격을 표시하고 싶다면, 고객 인스턴스에서 직접 가격을 조회할 수 있습니다.

```
use App\Models\User;

$prices = User::find(1)->productPrices([123, 456]);
```

<!-- Internally, Cashier will use the user's [`paddleCountry` method](#customer-defaults) to retrieve the prices in their currency. So, for example, a user living in the United States will see prices in USD while a user in Belgium will see prices in EUR. If no matching currency can be found the default currency of the product will be used. You can customize all prices of a product or subscription plan in the Paddle control panel. -->
내부적으로 Cashier는 사용자의 [`paddleCountry` method](#customer-defaults)를 활용해, 해당 국가의 통화로 가격을 조회합니다. 예를 들어 미국에 사는 사용자는 USD, 벨기에 사용자는 EUR로 가격이 표시됩니다. 만약 매칭되는 통화가 없다면 상품의 기본 통화가 사용됩니다. 모든 상품 및 플랜의 가격은 Paddle 콘솔에서 자유롭게 수정할 수 있습니다.

<a name="prices-coupons"></a>
<!-- #### Coupons -->
#### Coupons

<!-- You may also choose to display prices after a coupon reduction. When calling the `productPrices` method, coupons may be passed as a comma delimited string: -->
쿠폰이 적용된 최종 가격을 미리 보여줄 수도 있습니다. `productPrices` 호출 시 쿠폰을 콤마로 구분한 문자열로 전달하세요.

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], [
    'coupons' => 'SUMMERSALE,20PERCENTOFF'
]);
```

<!-- Then, display the calculated prices using the `price` method: -->
계산된 가격은 `price` 메서드로 가져올 수 있습니다.

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

<!-- You may display the original listed prices (without coupon discounts) using the `listPrice` method: -->
쿠폰 할인 없이 원래 표시된 가격을 보이고 싶다면 `listPrice` 메서드를 사용하세요.

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->listPrice()->gross() }}</li>
    @endforeach
</ul>
```

> [!NOTE]
> 가격 API를 사용할 때 Paddle은 오직 일회성 상품에만 쿠폰 적용을 지원하며, 구독 플랜에는 쿠폰을 적용할 수 없습니다.

<a name="customers"></a>
<!-- ## Customers -->
## Customers

<a name="customer-defaults"></a>
<!-- ### Customer Defaults -->
### Customer Defaults

<!-- Cashier allows you to define some useful defaults for your customers when creating pay links. Setting these defaults allow you to pre-fill a customer's email address, country, and postal code so that they can immediately move on to the payment portion of the checkout widget. You can set these defaults by overriding the following methods on your billable model: -->
Cashier에서는 페이 링크 생성 시 고객의 이메일, 국가, 우편번호 등 여러 정보를 기본값으로 미리 입력할 수 있습니다. 이를 통해 체크아웃 위젯에서 해당 정보를 바로 입력한 채로 결제 단계로 넘어갈 수 있습니다. 청구 가능 모델에서 아래 메서드들을 오버라이드하여 이러한 기본값을 설정할 수 있습니다.

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
설정한 기본값은 Cashier에서 [pay link](#pay-links)를 생성하는 모든 작업에 적용됩니다.

<a name="subscriptions"></a>
<!-- ## Subscriptions -->
## Subscriptions

<a name="creating-subscriptions"></a>
<!-- ### Creating Subscriptions -->
### Creating Subscriptions

<!-- To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription pay link: -->
구독을 생성하려면 먼저 청구 가능 모델(일반적으로 `App\Models\User` 인스턴스)을 가져와야 합니다. 모델 인스턴스를 준비한 다음, `newSubscription` 메서드로 구독 페이 링크를 생성할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $user->newSubscription('default', $premium = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

<!-- The first argument passed to the `newSubscription` method should be the internal name of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription name is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument given to the `newSubscription` method is the specific plan the user is subscribing to. This value should correspond to the plan's identifier in Paddle. The `returnTo` method accepts a URL that your user will be redirected to after they successfully complete the checkout. -->
`newSubscription` 메서드의 첫 번째 인수는 구독의 내부 명칭입니다. 애플리케이션이 단일 구독만 제공하는 경우라면 `default` 또는 `primary`처럼 명명하면 됩니다. 이 구독 이름은 내부 애플리케이션 로직에서만 사용되므로, 사용자에게 노출하거나 변경하지 않아야 하며, 공백 없이 설정해야 합니다. `newSubscription` 메서드에 전달하는 두 번째 인수는 사용자가 가입할 구체적인 플랜(Plan)의 식별자입니다. 이 값은 Paddle에서 플랜을 구분하는 값과 일치해야 합니다. `returnTo` 메서드에는 결제가 성공적으로 완료된 뒤 사용자를 리다이렉트할 URL을 지정합니다.

<!-- The `create` method will create a pay link which you can use to generate a payment button. The payment button can be generated using the `paddle-button` [Blade component](/docs/8.x/blade#components) that is included with Cashier Paddle: -->
`create` 메서드는 실제로 사용할 수 있는 페이 링크를 생성합니다. 결제 버튼은 Cashier Paddle이 제공하는 `paddle-button` [Blade component](/docs/8.x/blade#components)를 사용해 만들 수 있습니다.

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

<!-- After the user has finished their checkout, a `subscription_created` webhook will be dispatched from Paddle. Cashier will receive this webhook and setup the subscription for your customer. In order to make sure all webhooks are properly received and handled by your application, ensure you have properly [setup webhook handling](#handling-paddle-webhooks). -->
사용자가 결제를 완료하면, Paddle에서 `subscription_created` 웹훅이 발송됩니다. Cashier가 이 웹훅을 수신하여 해당 고객의 구독을 설정해줍니다. 모든 웹훅이 제대로 수신/처리되는지 반드시 [setup webhook handling](#handling-paddle-webhooks)이 필요한 점을 유념하세요.

<a name="additional-details"></a>
<!-- #### Additional Details -->
#### Additional Details

<!-- If you would like to specify additional customer or subscription details, you may do so by passing them as an array of key / value pairs to the `create` method. To learn more about the additional fields supported by Paddle, check out Paddle's documentation on [generating pay links](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink): -->
구독 또는 고객에 대한 추가 정보를 더 지정하고 싶다면, `create` 메서드에서 키/값 배열로 함께 전달할 수 있습니다. 지원되는 필드와 자세한 내용은 [generating pay links](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요.

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
구독 생성 시 쿠폰을 함께 적용하고 싶다면, `withCoupon` 메서드를 이용하세요.

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
`withMetadata` 메서드를 사용하여 메타데이터 배열을 전달할 수도 있습니다.

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withMetadata(['key' => 'value'])
    ->create();
```

> [!NOTE]
> 메타데이터를 제공할 때는 `subscription_name`을 메타데이터 키로 사용하지 마십시오. 이 키는 Cashier 내부적으로 예약되어 있습니다.

<a name="checking-subscription-status"></a>
<!-- ### Checking Subscription Status -->
### Checking Subscription Status

<!-- Once a user is subscribed to your application, you may check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the user has an active subscription, even if the subscription is currently within its trial period: -->
사용자가 애플리케이션에 구독한 이후에는 여러 편리한 메서드를 사용하여 구독 상태를 확인할 수 있습니다. 먼저, `subscribed` 메서드는 사용자가 활성 구독 상태라면(체험 기간(trial period) 중이더라도) `true`를 반환합니다.

```
if ($user->subscribed('default')) {
    //
}
```

<!-- The `subscribed` method also makes a great candidate for a [route middleware](/docs/8.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status: -->
`subscribed` 메서드는 [route middleware](/docs/8.x/middleware)에 활용하기에도 적합합니다. 이를 통해 사용자의 구독 상태에 따라 라우트와 컨트롤러의 접근을 제한할 수 있습니다.

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
사용자가 아직 체험 기간(trial period) 중인지 확인하고 싶다면 `onTrial` 메서드를 사용할 수 있습니다. 예를 들어, 체험 기간임을 유저에게 경고 메시지로 안내할 때 활용할 수 있습니다.

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

<!-- The `subscribedToPlan` method may be used to determine if the user is subscribed to a given plan based on a given Paddle plan ID. In this example, we will determine if the user's `default` subscription is actively subscribed to the monthly plan: -->
`subscribedToPlan` 메서드는 지정한 Paddle 요금제(plan) ID를 바탕으로 사용자가 해당 요금제에 구독 중인지 여부를 확인할 때 사용할 수 있습니다. 예를 들어, 사용자의 `default` 구독이 월간 요금제에 등록되어 있는지 확인하려면 다음과 같이 할 수 있습니다.

```
if ($user->subscribedToPlan($monthly = 12345, 'default')) {
    //
}
```

<!-- By passing an array to the `subscribedToPlan` method, you may determine if the user's `default` subscription is actively subscribed to the monthly or the yearly plan: -->
`subscribedToPlan` 메서드에 배열을 전달하면 사용자의 `default` 구독이 월간 요금제나 연간 요금제 중 하나에 등록되어 있는지 확인할 수 있습니다.

```
if ($user->subscribedToPlan([$monthly = 12345, $yearly = 54321], 'default')) {
    //
}
```

<!-- The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period: -->
`recurring` 메서드는 사용자가 현재 구독 중이며, 체험 기간이 지난 상태인지를 확인할 때 사용할 수 있습니다.

```
if ($user->subscription('default')->recurring()) {
    //
}
```

<a name="cancelled-subscription-status"></a>
<!-- #### Cancelled Subscription Status -->
#### Cancelled Subscription Status

<!-- To determine if the user was once an active subscriber but has cancelled their subscription, you may use the `cancelled` method: -->
사용자가 한때 활성 구독자였으나 구독을 취소한 경우, 이를 확인하려면 `cancelled` 메서드를 사용할 수 있습니다.

```
if ($user->subscription('default')->cancelled()) {
    //
}
```

<!-- You may also determine if a user has cancelled their subscription, but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time: -->
구독 취소 후, 완전히 만료되기 전까지 "유예 기간(grace period)"이 남아 있는지도 확인할 수 있습니다. 예를 들어, 3월 5일에 구독을 취소했으나 원래 만료일이 3월 10일이었다면 3월 10일까지 유예 기간이 남은 상태입니다. 이 기간에도 `subscribed` 메서드는 여전히 `true`를 반환합니다.

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- To determine if the user has cancelled their subscription and is no longer within their "grace period", you may use the `ended` method: -->
사용자가 구독을 취소했고, 더 이상 유예 기간에 있지 않은 상태인지 확인하려면 `ended` 메서드를 사용합니다.

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="past-due-status"></a>
<!-- #### Past Due Status -->
#### Past Due Status

<!-- If a payment fails for a subscription, it will be marked as `past_due`. When your subscription is in this state it will not be active until the customer has updated their payment information. You may determine if a subscription is past due using the `pastDue` method on the subscription instance: -->
구독 결제에 실패하면 해당 구독의 상태가 `past_due`로 표시됩니다. 이 상태에서는 고객이 결제 정보를 갱신할 때까지 구독이 활성 상태가 아니게 됩니다. 구독 인스턴스의 `pastDue` 메서드를 사용하여 연체 상태인지 확인할 수 있습니다.

```
if ($user->subscription('default')->pastDue()) {
    //
}
```

<!-- When a subscription is past due, you should instruct the user to [update their payment information](#updating-payment-information). You may configure how past due subscriptions are handled in your [Paddle subscription settings](https://vendors.paddle.com/subscription-settings). -->
구독이 연체 상태라면, 사용자에게 [update their payment information](#updating-payment-information)을 안내해야 합니다. 연체 구독 처리 방식은 [Paddle subscription settings](https://vendors.paddle.com/subscription-settings)에서 구성할 수 있습니다.

<!-- If you would like subscriptions to still be considered active when they are `past_due`, you may use the `keepPastDueSubscriptionsActive` method provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`: -->
연체(`past_due`) 상태에서도 구독을 활성 상태로 간주하고 싶다면, Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 메서드를 사용할 수 있습니다. 이 메서드는 일반적으로 `AppServiceProvider`의 `register` 메서드에서 호출해야 합니다.

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

> [!NOTE]
> 구독이 `past_due` 상태일 때는 결제 정보가 갱신되기 전까지 상태를 변경할 수 없습니다. 따라서 `swap` 및 `updateQuantity` 메서드가 `past_due` 상태에서 호출되면 예외가 발생합니다.

<a name="subscription-scopes"></a>
<!-- #### Subscription Scopes -->
#### Subscription Scopes

<!-- Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state: -->
대부분의 구독 상태는 쿼리 스코프(scope)로도 제공되어, 특정 상태에 해당하는 구독을 데이터베이스에서 쉽게 조회할 수 있습니다.

```
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the cancelled subscriptions for a user...
$subscriptions = $user->subscriptions()->cancelled()->get();
```

<!-- A complete list of available scopes is available below: -->
사용 가능한 전체 스코프 목록은 다음과 같습니다.

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
구독 단일 청구 기능을 사용하면 구독자에게 구독 금액에 더해 1회성 추가 금액을 청구할 수 있습니다.

```
$response = $user->subscription('default')->charge(12.99, 'Support Add-on');
```

<!-- In contrast to [single charges](#single-charges), this method will immediately charge the customer's stored payment method for the subscription. The charge amount should always be defined in the currency of the subscription. -->
[single charges](#single-charges)와 달리, 이 메서드는 구독에 저장된 결제 수단으로 즉시 청구가 이루어집니다. 청구 금액은 반드시 구독의 통화로 지정해야 합니다.

<a name="updating-payment-information"></a>
<!-- ### Updating Payment Information -->
### Updating Payment Information

<!-- Paddle always saves a payment method per subscription. If you want to update the default payment method for a subscription, you should first generate a subscription "update URL" using the `updateUrl` method on the subscription model: -->
Paddle은 구독별로 결제 수단을 저장합니다. 구독의 기본 결제 수단을 갱신하려면 우선 구독 모델의 `updateUrl` 메서드를 사용하여 구독 "업데이트 URL"을 생성해야 합니다.

```
use App\Models\User;

$user = User::find(1);

$updateUrl = $user->subscription('default')->updateUrl();
```

<!-- Then, you may use the generated URL in combination with Cashier's provided `paddle-button` Blade component to allow the user to initiate the Paddle widget and update their payment information: -->
그런 다음, Cashier에서 제공하는 `paddle-button` Blade 컴포넌트와 함께 생성된 URL을 사용하여 사용자가 Paddle 위젯을 열고 결제 정보를 갱신할 수 있도록 할 수 있습니다.

```html
<x-paddle-button :url="$updateUrl" class="px-8 py-4">
    Update Card
</x-paddle-button>
```

<!-- When a user has finished updating their information, a `subscription_updated` webhook will be dispatched by Paddle and the subscription details will be updated in your application's database. -->
사용자가 결제 정보를 갱신하면, Paddle에서 `subscription_updated` 웹훅이 전송되며, 애플리케이션의 데이터베이스에 구독 정보가 자동으로 업데이트됩니다.

<a name="changing-plans"></a>
<!-- ### Changing Plans -->
### Changing Plans

<!-- After a user has subscribed to your application, they may occasionally want to change to a new subscription plan. To update the subscription plan for a user, you should pass the Paddle plan's identifier to the subscription's `swap` method: -->
사용자가 애플리케이션에 구독한 후, 새로운 구독 요금제로 변경하고 싶어 할 수 있습니다. 사용자의 구독 요금제를 변경하려면, 구독의 `swap` 메서드에 Paddle 요금제의 식별자를 전달하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap($premium = 34567);
```

<!-- If you would like to swap plans and immediately invoice the user instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method: -->
요금제 변경 시 다음 결제 주기까지 기다리지 않고 곧바로 사용자를 청구하려면 `swapAndInvoice` 메서드를 사용하세요.

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice($premium = 34567);
```

> [!NOTE]
> 체험(trial) 중에는 요금제 변경이 불가능합니다. 이 제한에 대한 추가 정보는 [Paddle documentation](https://developer.paddle.com/api-reference/subscription-api/users/updateuser#usage-notes)를 참고하세요.

<a name="prorations"></a>
<!-- #### Prorations -->
#### Prorations

<!-- By default, Paddle prorates charges when swapping between plans. The `noProrate` method may be used to update the subscription's without prorating the charges: -->
기본적으로, Paddle은 요금제를 변경할 때 금액을 일할 계산하여 청구합니다. 일할 계산 없이 구독 정보를 갱신하려면 `noProrate` 메서드를 사용합니다.

```
$user->subscription('default')->noProrate()->swap($premium = 34567);
```

<a name="subscription-quantity"></a>
<!-- ### Subscription Quantity -->
### Subscription Quantity

<!-- Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. To easily increment or decrement your subscription's quantity, use the `incrementQuantity` and `decrementQuantity` methods: -->
특정 상황에서는 구독이 "수량(quantity)"에 따라 사용될 수 있습니다. 예를 들어, 프로젝트 관리 애플리케이션이 프로젝트 1개당 월 $10을 부과하는 경우가 이에 해당합니다. 구독 수량을 간편하게 증가 또는 감소하려면, `incrementQuantity`와 `decrementQuantity` 메서드를 사용할 수 있습니다.

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
또는 `updateQuantity` 메서드를 사용하여 특정 수량으로 직접 설정할 수도 있습니다.

```
$user->subscription('default')->updateQuantity(10);
```

<!-- The `noProrate` method may be used to update the subscription's quantity without prorating the charges: -->
일할 계산 없이 구독 수량을 갱신하고 싶다면, `noProrate` 메서드를 함께 사용할 수 있습니다.

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<a name="subscription-modifiers"></a>
<!-- ### Subscription Modifiers -->
### Subscription Modifiers

<!-- Subscription modifiers allow you to implement [metered billing](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers) or extend subscriptions with add-ons. -->
구독 수정자(modifier)를 사용하면 [metered billing](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers)나 부가 기능(add-on)을 구독에 적용할 수 있습니다.

<!-- For example, you might want to offer a "Premium Support" add-on with your standard subscription. You can create this modifier like so: -->
예를 들어, 표준 구독에 "프리미엄 지원" 부가 기능을 제공하고 싶다면 아래와 같이 수정자를 추가할 수 있습니다.

```
$modifier = $user->subscription('default')->newModifier(12.99)->create();
```

<!-- The example above will add a $12.99 add-on to the subscription. By default, this charge will recur on every interval you have configured for the subscription. If you would like, you can add a readable description to the modifier using the modifier's `description` method: -->
위 예시에서는 구독에 $12.99의 부가 비용이 추가됩니다. 기본적으로 이 금액은 구독에서 설정한 주기마다 계속 반복 청구됩니다. 만약 수정자에 사람이 보기 쉬운 설명을 추가하고 싶다면, `description` 메서드를 사용할 수 있습니다.

```
$modifier = $user->subscription('default')->newModifier(12.99)
    ->description('Premium Support')
    ->create();
```

<!-- To illustrate how to implement metered billing using modifiers, imagine your application charges per SMS message sent by the user. First, you should create a $0 plan in your Paddle dashboard. Once the user has been subscribed to this plan, you can add modifiers representing each individual charge to the subscription: -->
수정자(modifier)를 활용해 측정형 청구를 구현하는 예시로, 사용자가 SMS 메시지를 보낼 때마다 과금을 하려면 Paddle 대시보드에서 $0 요금제를 만들고, 사용자가 이 요금제에 구독하면 각각의 청구에 해당하는 수정자를 추가하면 됩니다.

```
$modifier = $user->subscription('default')->newModifier(0.99)
    ->description('New text message')
    ->oneTime()
    ->create();
```

<!-- As you can see, we invoked the `oneTime` method when creating this modifier. This method will ensure the modifier is only charged once and does not recur every billing interval. -->
위 코드에서 `oneTime` 메서드를 호출하였으므로, 해당 수정자는 한 번만 과금되고 매 결제주기마다 반복되지 않습니다.

<a name="retrieving-modifiers"></a>
<!-- #### Retrieving Modifiers -->
#### Retrieving Modifiers

<!-- You may retrieve a list of all modifiers for a subscription via the `modifiers` method: -->
`modifiers` 메서드를 통해 해당 구독의 모든 수정자 목록을 조회할 수 있습니다.

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
`Laravel\Paddle\Modifier` 인스턴스의 `delete` 메서드를 호출하여 수정자를 삭제할 수 있습니다.

```
$modifier->delete();
```

<a name="pausing-subscriptions"></a>
<!-- ### Pausing Subscriptions -->
### Pausing Subscriptions

<!-- To pause a subscription, call the `pause` method on the user's subscription: -->
구독을 일시정지하려면 사용자의 구독에 `pause` 메서드를 호출합니다.

```
$user->subscription('default')->pause();
```

<!-- When a subscription is paused, Cashier will automatically set the `paused_from` column in your database. This column is used to know when the `paused` method should begin returning `true`. For example, if a customer pauses a subscription on March 1st, but the subscription was not scheduled to recur until March 5th, the `paused` method will continue to return `false` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
구독이 일시정지되면, Cashier가 데이터베이스의 `paused_from` 컬럼 값을 자동으로 설정합니다. 이 컬럼은 `paused` 메서드가 언제부터 `true`를 반환해야 하는지 판단하는 기준으로 사용됩니다. 예를 들어 고객이 3월 1일에 구독을 일시정지했으나, 구독의 다음 결제 주기가 3월 5일이었다면, `paused` 메서드는 3월 5일까지는 계속 `false`를 반환합니다. 이는 사용자가 일반적으로 결제 주기 종료일까지 서비스를 계속 이용하도록 허용하기 때문입니다.

<!-- You may determine if a user has paused their subscription but are still on their "grace period" using the `onPausedGracePeriod` method: -->
구독을 일시정지했지만 아직 "유예 기간"에 있는 사용자인지 여부는 `onPausedGracePeriod` 메서드로 확인할 수 있습니다.

```
if ($user->subscription('default')->onPausedGracePeriod()) {
    //
}
```

<!-- To resume a paused a subscription, you may call the `unpause` method on the user's subscription: -->
일시정지된 구독을 다시 활성화(재개)하려면, 해당 구독에 `unpause` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->unpause();
```

> [!NOTE]
> 구독이 일시정지 중에는 수정이 불가능합니다. 만약 요금제를 변경하거나 수량을 수정하고 싶다면 먼저 구독을 재개해야 합니다.

<a name="cancelling-subscriptions"></a>
<!-- ### Cancelling Subscriptions -->
### Cancelling Subscriptions

<!-- To cancel a subscription, call the `cancel` method on the user's subscription: -->
구독을 취소하려면 사용자의 구독에 `cancel` 메서드를 호출합니다.

```
$user->subscription('default')->cancel();
```

<!-- When a subscription is cancelled, Cashier will automatically set the `ends_at` column in your database. This column is used to know when the `subscribed` method should begin returning `false`. For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle. -->
구독이 취소되면 Cashier가 데이터베이스의 `ends_at` 컬럼을 자동으로 설정합니다. 이 컬럼은 `subscribed` 메서드가 언제부터 `false`를 반환해야 할지 판단하는데 사용됩니다. 예를 들어, 고객이 구독을 3월 1일에 취소했으나 실제 만료일이 3월 5일이었다면, 3월 5일까지는 계속 `subscribed` 메서드가 `true`를 반환합니다. 일반적으로 결제 주기 종료일까지 서비스를 계속 이용하도록 허용하기 때문입니다.

<!-- You may determine if a user has cancelled their subscription but are still on their "grace period" using the `onGracePeriod` method: -->
구독을 취소했으나 아직 "유예 기간"이 남은 사용자인지 확인하려면 `onGracePeriod` 메서드를 사용합니다.

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

<!-- If you wish to cancel a subscription immediately, you may call the `cancelNow` method on the user's subscription: -->
즉시 구독을 취소하고 싶을 땐, 사용자의 구독 인스턴스에서 `cancelNow` 메서드를 호출하면 됩니다.

```
$user->subscription('default')->cancelNow();
```

> [!NOTE]
> Paddle의 구독은 취소 후 재개가 불가능합니다. 고객이 구독을 다시 사용하기 원한다면, 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
<!-- ## Subscription Trials -->
## Subscription Trials

<a name="with-payment-method-up-front"></a>
<!-- ### With Payment Method Up Front -->
### With Payment Method Up Front

> [!NOTE]
> 체험 기간 중 결제 정보를 미리 수집하는 경우, Paddle은 요금제 변경(swap)이나 수량(quantity) 업데이트 등 구독의 변경을 허용하지 않습니다. 체험 중에 요금제 변경을 허용하고 싶다면, 해당 구독을 취소 후 다시 생성해야 합니다.

<!-- If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscription pay links: -->
결제 정보를 선등록받으면서 체험 기간을 제공하고 싶다면, 구독 페이링크 생성 시 `trialDays` 메서드를 사용하세요.

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
이 메서드는 구독 레코드에 체험 기간의 종료 날짜를 저장하며, Paddle에도 그 날짜까지 결제가 시작되지 않도록 지시합니다.

> [!NOTE]
> 체험 기간 종료 시 구독이 취소되지 않았다면, 체험 기간이 만료되는 즉시 결제가 이루어집니다. 따라서 체험 종료일을 사용자에게 반드시 안내해야 합니다.

<!-- You may determine if the user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent: -->
사용자가 체험 기간 중인지 확인할 때는, 사용자 인스턴스의 `onTrial` 메서드와 구독 인스턴스의 `onTrial` 메서드 둘 중 어느 것을 사용해도 됩니다. 아래 두 예시는 동등하게 동작합니다.

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

<a name="defining-trial-days-in-paddle-cashier"></a>
<!-- #### Defining Trial Days In Paddle / Cashier -->
#### Defining Trial Days In Paddle / Cashier

<!-- You may choose to define how many trial days your plan's receive in the Paddle dashboard or always pass them explicitly using Cashier. If you choose to define your plan's trial days in Paddle you should be aware that new subscriptions, including new subscriptions for a customer that had a subscription in the past, will always receive a trial period unless you explicitly call the `trialDays(0)` method. -->
요금제별 체험 일수는 Paddle 대시보드에서 설정하거나, Cashier를 통해 명시적으로 해당 값을 전달할 수 있습니다. Paddle에서 요금제별로 체험 기간을 지정한 경우, 과거에 구독 이력이 있던 고객을 포함해 새 구독마다 항상 체험 기간이 할당됨에 유의해야 합니다. 만약 체험 기간이 필요 없으면 반드시 `trialDays(0)`을 명시적으로 호출해야 합니다.

<a name="without-payment-method-up-front"></a>
<!-- ### Without Payment Method Up Front -->
### Without Payment Method Up Front

<!-- If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the customer record attached to your user to your desired trial ending date. This is typically done during user registration: -->
결제 정보를 미리 수집하지 않고 체험 기간을 제공하려면, 사용자의 고객 레코드에 연결된 `trial_ends_at` 컬럼에 원하는 체험 종료 날짜를 저장하면 됩니다. 보통 회원가입 단계에서 이 처리를 합니다.

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
이와 같은 방식의 체험 구독을 Cashier에서는 "일반(generic) 체험"이라고 부릅니다. 이는 실제 구독과 연결되지 않은 체험이기 때문입니다. `User` 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 값을 지나지 않았다면 `true`를 반환합니다.

```
if ($user->onTrial()) {
    // User is within their trial period...
}
```

<!-- Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual: -->
실제 구독을 생성할 준비가 되었다면, 평소처럼 `newSubscription` 메서드를 사용할 수 있습니다.

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
사용자의 체험 기간 종료일을 조회하려면, `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 체험 중인 사용자는 Carbon 인스턴스를 반환하고, 그렇지 않으면 `null`을 반환합니다. 기본이 아닌 다른 구독의 체험 종료일을 조회하려면 구독 이름을 인수로 전달할 수도 있습니다.

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

<!-- You may use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not created an actual subscription yet: -->
아직 실제 구독을 생성하지 않고 "일반(generic) 체험"만 진행 중인지 확인하려면 `onGenericTrial` 메서드를 사용할 수 있습니다.

```
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

> [!NOTE]
> Paddle 구독이 한 번 생성된 후에는 체험 기간을 연장하거나 수정할 수 있는 방법이 없습니다.

<a name="handling-paddle-webhooks"></a>
<!-- ## Handling Paddle Webhooks -->
## Handling Paddle Webhooks

<!-- Paddle can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is registered by the Cashier service provider. This controller will handle all incoming webhook requests. -->
Paddle은 다양한 이벤트를 웹훅을 통해 애플리케이션에 알릴 수 있습니다. 기본적으로, Cashier 서비스 프로바이더에서 Cashier의 웹훅 컨트롤러로 연결되는 라우트가 자동 등록됩니다. 이 컨트롤러는 모든 수신 웹훅 요청을 처리합니다.

<!-- By default, this controller will automatically handle cancelling subscriptions that have too many failed charges ([as defined by your Paddle subscription settings](https://vendors.paddle.com/subscription-settings)), subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Paddle webhook event you like. -->
기본적으로 이 컨트롤러는 결제 실패가 반복된 구독의 자동 취소([as defined by your Paddle subscription settings](https://vendors.paddle.com/subscription-settings)), 구독 정보 업데이트, 결제 수단 변경 등을 자동으로 처리합니다. 추가로, 원하는 모든 Paddle 웹훅 이벤트를 직접 다룰 수도 있습니다.

<!-- To ensure your application can handle Paddle webhooks, be sure to [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/alerts-webhooks). By default, Cashier's webhook controller responds to the `/paddle/webhook` URL path. The full list of all webhooks you should enable in the Paddle control panel are: -->
애플리케이션이 Paddle 웹훅을 받으려면 [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/alerts-webhooks)해야 합니다. Cashier의 웹훅 컨트롤러는 기본적으로 `/paddle/webhook` 경로를 사용합니다. Paddle 관리 패널에서 활성화해야 할 웹훅 이벤트 목록은 다음과 같습니다.

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

> [!NOTE]
> Cashier에서 제공하는 [webhook signature verification](/docs/8.x/cashier-paddle#verifying-webhook-signatures) 미들웨어로 수신 요청을 안전하게 보호해야 합니다.

<a name="webhooks-csrf-protection"></a>
<!-- #### Webhooks & CSRF Protection -->
#### Webhooks & CSRF Protection

<!-- Since Paddle webhooks need to bypass Laravel's [CSRF protection](/docs/8.x/csrf), be sure to list the URI as an exception in your `App\Http\Middleware\VerifyCsrfToken` middleware or list the route outside of the `web` middleware group: -->
Paddle 웹훅은 Laravel의 [CSRF protection](/docs/8.x/csrf)를 우회해야 하므로, 반드시 `App\Http\Middleware\VerifyCsrfToken` 미들웨어에서 이 URI를 예외 목록에 추가하거나, `web` 미들웨어 그룹 밖에서 라우트를 선언해야 합니다.

```
protected $except = [
    'paddle/*',
];
```

<a name="webhooks-local-development"></a>
<!-- #### Webhooks & Local Development -->
#### Webhooks & Local Development

<!-- For Paddle to be able to send your application webhooks during local development, you will need to expose your application via a site sharing service such as [Ngrok](https://ngrok.com/) or [Expose](https://expose.dev/docs/introduction). If you are developing your application locally using [Laravel Sail](/docs/8.x/sail), you may use Sail's [site sharing command](/docs/8.x/sail#sharing-your-site). -->
로컬 개발 단계에서 Paddle이 웹훅을 전송할 수 있도록 하려면 [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction)와 같은 사이트 공유 서비스로 애플리케이션을 외부에 노출시켜야 합니다. [Laravel Sail](/docs/8.x/sail)로 개발한다면 Sail의 [site sharing command](/docs/8.x/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
<!-- ### Defining Webhook Event Handlers -->
### Defining Webhook Event Handlers

<!-- Cashier automatically handles subscription cancellation on failed charges and other common Paddle webhooks. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier: -->
Cashier는 결제 실패 시 구독 자동 취소 등 일반적인 Paddle 웹훅을 자동으로 처리합니다. 추가적으로 더 많은 웹훅 이벤트를 처리하고 싶다면, Cashier에서 디스패치하는 다음 이벤트를 리스닝하면 됩니다.

<!--
- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`
-->
- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

<!-- Both events contain the full payload of the Paddle webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/8.x/events#defining-listeners) that will handle the event: -->
각 이벤트에는 Paddle의 전체 페이로드가 담겨 있습니다. 예를 들어, `invoice.payment_succeeded` 웹훅을 처리하려면 [listener](/docs/8.x/events#defining-listeners)를 등록하여 다음과 같이 구현할 수 있습니다.

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
이제 위에서 정의한 리스너는 애플리케이션의 `EventServiceProvider`에 다음과 같이 등록할 수 있습니다.

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
Cashier는 수신된 웹훅 타입별로 전용 이벤트도 발생시킵니다. Paddle에서 받은 전체 페이로드뿐 아니라 처리에 사용된 관련 모델(구독, 청구 가능 모델, 영수증 등)도 포함합니다.

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
또한, `.env` 파일에 `CASHIER_WEBHOOK` 환경 변수를 정의하면 기본 내장 웹훅 라우트를 원하는 값으로 변경할 수 있습니다. 반드시 Paddle 제어 패널에 설정한 웹훅 URL과 일치해야 합니다.

```bash
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>

<!-- ### Verifying Webhook Signatures -->
### Verifying Webhook Signatures

<!-- To secure your webhooks, you may use [Paddle's webhook signatures](https://developer.paddle.com/webhook-reference/verifying-webhooks). For convenience, Cashier automatically includes a middleware which validates that the incoming Paddle webhook request is valid. -->
웹훅의 보안을 위해 [Paddle's webhook signatures](https://developer.paddle.com/webhook-reference/verifying-webhooks)을 사용할 수 있습니다. 편의를 위해 Cashier는 들어오는 Paddle 웹훅 요청의 유효성을 자동으로 검증하는 미들웨어를 포함하고 있습니다.

<!-- To enable webhook verification, ensure that the `PADDLE_PUBLIC_KEY` environment variable is defined in your application's `.env` file. The public key may be retrieved from your Paddle account dashboard. -->
웹훅 검증을 활성화하려면, 애플리케이션의 `.env` 파일에 `PADDLE_PUBLIC_KEY` 환경 변수가 정의되어 있는지 확인해야 합니다. 퍼블릭 키는 Paddle 계정 대시보드에서 가져올 수 있습니다.

<a name="single-charges"></a>
<!-- ## Single Charges -->
## Single Charges

<a name="simple-charge"></a>
<!-- ### Simple Charge -->
### Simple Charge

<!-- If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance to generate a pay link for the charge. The `charge` method accepts the charge amount (float) as its first argument and a charge description as its second argument: -->
고객에게 일회성 결제를 진행하고 싶다면, billable 모델 인스턴스에서 `charge` 메서드를 사용해 결제 pay 링크를 생성할 수 있습니다. `charge` 메서드는 첫 번째 인수로 결제 금액(float), 두 번째 인수로 결제 설명을 받습니다.

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $user->charge(12.99, 'Action Figure')
    ]);
});
```

<!-- After generating the pay link, you may use Cashier's provided `paddle-button` Blade component to allow the user to initiate the Paddle widget and complete the charge: -->
pay 링크를 생성한 후, Cashier에서 제공하는 `paddle-button` Blade 컴포넌트를 통해 사용자가 Paddle 위젯을 실행하고 결제를 완료할 수 있도록 할 수 있습니다.

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

<!-- The `charge` method accepts an array as its third argument, allowing you to pass any options you wish to the underlying Paddle pay link creation. Please consult [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) to learn more about the options available to you when creating charges: -->
`charge` 메서드는 세 번째 인수로 배열을 받을 수 있으므로, pay 링크 생성 시 원하는 옵션을 전달할 수 있습니다. 사용 가능한 옵션에 대해서는 [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하시기 바랍니다.

```
$payLink = $user->charge(12.99, 'Action Figure', [
    'custom_option' => $value,
]);
```

<!-- Charges happen in the currency specified in the `cashier.currency` configuration option. By default, this is set to USD. You may override the default currency by defining the `CASHIER_CURRENCY` environment variable in your application's `.env` file: -->
결제는 `cashier.currency` 설정 옵션에 지정된 통화로 진행됩니다. 기본값은 USD(미국 달러)입니다. `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 정의하여 기본 통화를 변경할 수 있습니다.

```bash
CASHIER_CURRENCY=EUR
```

<!-- You can also [override prices per currency](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink#price-overrides) using Paddle's dynamic pricing matching system. To do so, pass an array of prices instead of a fixed amount: -->
또한, Paddle의 동적 가격 일치 기능을 사용해 [override prices per currency](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink#price-overrides)할 수도 있습니다. 이 경우, 고정 금액 대신 여러 통화가 포함된 배열을 전달합니다.

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
Paddle에 등록된 특정 상품에 대해 일회성 결제를 진행하고자 한다면, billable 모델 인스턴스에서 `chargeProduct` 메서드를 사용해 pay 링크를 생성할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $request->user()->chargeProduct($productId = 123)
    ]);
});
```

<!-- Then, you may provide the pay link to the `paddle-button` component to allow the user to initialize the Paddle widget: -->
이후, 이 pay 링크를 `paddle-button` 컴포넌트에 제공하면 사용자가 Paddle 위젯을 실행할 수 있습니다.

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

<!-- The `chargeProduct` method accepts an array as its second argument, allowing you to pass any options you wish to the underlying Paddle pay link creation. Please consult [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) regarding the options that are available to you when creating charges: -->
`chargeProduct` 메서드는 두 번째 인수로 배열을 전달할 수 있어, pay 링크 생성 시 원하는 옵션을 설정할 수 있습니다. 사용 가능한 옵션에 대해서는 [the Paddle documentation](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하시기 바랍니다.

```
$payLink = $user->chargeProduct($productId, [
    'custom_option' => $value,
]);
```

<a name="refunding-orders"></a>
<!-- ### Refunding Orders -->
### Refunding Orders

<!-- If you need to refund a Paddle order, you may use the `refund` method. This method accepts the Paddle order ID as its first argument. You may retrieve the receipts for a given billable model using the `receipts` method: -->
Paddle 주문을 환불해야 하는 경우, `refund` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 Paddle 주문 ID를 받습니다. 해당 billable 모델에 대한 영수증(receipt)는 `receipts` 메서드를 통해 조회할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$receipt = $user->receipts()->first();

$refundRequestId = $user->refund($receipt->order_id);
```

<!-- You may optionally specify a specific amount to refund as well as a reason for the refund: -->
필요하다면 환불할 금액과 환불 사유도 추가 인수로 함께 지정할 수 있습니다.

```
$receipt = $user->receipts()->first();

$refundRequestId = $user->refund(
    $receipt->order_id, 5.00, 'Unused product time'
);
```

> [!TIP]
> Paddle 지원팀에 환불 관련 문의할 때 `$refundRequestId`를 참조용으로 사용할 수 있습니다.

<a name="receipts"></a>
<!-- ## Receipts -->
## Receipts

<!-- You may easily retrieve an array of a billable model's receipts via the `receipts` property: -->
`receipts` 속성을 통해 billable 모델의 영수증 배열을 쉽게 불러올 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$receipts = $user->receipts;
```

<!-- When listing the receipts for the customer, you may use the receipt instance's methods to display the relevant receipt information. For example, you may wish to list every receipt in a table, allowing the user to easily download any of the receipts: -->
고객의 영수증 목록을 표시할 때, 각 receipt 인스턴스의 메서드를 사용해 관련 정보를 출력할 수 있습니다. 예를 들어, 모든 영수증을 표로 나열해 사용자가 원하는 영수증을 쉽게 다운로드할 수 있도록 할 수 있습니다.

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
정기 구독의 과거 결제 내역이나 다가오는 결제 일정을 조회하고 싶을 때는 `lastPayment` 및 `nextPayment` 메서드를 사용할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription('default');

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

<!-- Both of these methods will return an instance of `Laravel\Paddle\Payment`; however, `nextPayment` will return `null` when the billing cycle has ended (such as when a subscription has been cancelled): -->
이 두 메서드는 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 다만, 구독이 취소되는 등 결제 주기가 종료된 경우 `nextPayment`는 `null`을 반환합니다.

```
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="handling-failed-payments"></a>
<!-- ## Handling Failed Payments -->
## Handling Failed Payments

<!-- Subscription payments fail for various reasons, such as expired cards or a card having insufficient funds. When this happens, we recommend that you let Paddle handle payment failures for you. Specifically, you may [setup Paddle's automatic billing emails](https://vendors.paddle.com/subscription-settings) in your Paddle dashboard. -->
구독 결제는 카드 만료, 잔액 부족 등 다양한 이유로 실패할 수 있습니다. 이런 상황에서는 Paddle이 결제 실패 처리를 담당하도록 맡기는 것이 좋습니다. 구체적으로, Paddle 대시보드에서 [setup Paddle's automatic billing emails](https://vendors.paddle.com/subscription-settings)을 설정할 수 있습니다.

<!-- Alternatively, you can perform more precise customization by catching the [`subscription_payment_failed`](https://developer.paddle.com/webhook-reference/subscription-alerts/subscription-payment-failed) webhook and enabling the "Subscription Payment Failed" option in the Webhook settings of your Paddle dashboard: -->
좀 더 세밀한 처리가 필요하다면 [`subscription_payment_failed`](https://developer.paddle.com/webhook-reference/subscription-alerts/subscription-payment-failed) 웹훅을 수신해, Paddle 대시보드의 Webhook 설정에서 "Subscription Payment Failed" 옵션을 활성화하면 됩니다.

```
<?php

namespace App\Http\Controllers;

use Laravel\Paddle\Http\Controllers\WebhookController as CashierController;

class WebhookController extends CashierController
{
    /**
     * Handle subscription payment failed.
     *
     * @param  array  $payload
     * @return void
     */
    public function handleSubscriptionPaymentFailed($payload)
    {
        // Handle the failed subscription payment...
    }
}
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- While testing, you should manually test your billing flow to make sure your integration works as expected. -->
빌링 플로우가 정상적으로 동작하는지 수동으로 테스트해보는 것이 좋습니다.

<!-- For automated tests, including those executed within a CI environment, you may use [Laravel's HTTP Client](/docs/8.x/http-client#testing) to fake HTTP calls made to Paddle. Although this does not test the actual responses from Paddle, it does provide a way to test your application without actually calling Paddle's API. -->
CI 환경을 포함한 자동화 테스트에서는 [Laravel's HTTP Client](/docs/8.x/http-client#testing)를 사용해 Paddle로의 HTTP 호출을 가짜로 만들어 처리할 수 있습니다. 비록 Paddle의 실제 응답을 테스트할 수는 없지만, Paddle API에 실제로 요청을 보내지 않고도 애플리케이션의 동작을 검증할 수 있습니다.