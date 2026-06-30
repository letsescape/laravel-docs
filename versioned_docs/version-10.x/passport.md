<!-- # Laravel Passport -->
# Laravel Passport

- [Introduction](#introduction)
    - [Passport or Sanctum?](#passport-or-sanctum)
- [Installation](#installation)
    - [Deploying Passport](#deploying-passport)
    - [Migration Customization](#migration-customization)
    - [Upgrading Passport](#upgrading-passport)
- [Configuration](#configuration)
    - [Client Secret Hashing](#client-secret-hashing)
    - [Token Lifetimes](#token-lifetimes)
    - [Overriding Default Models](#overriding-default-models)
    - [Overriding Routes](#overriding-routes)
- [Issuing Access Tokens](#issuing-access-tokens)
    - [Managing Clients](#managing-clients)
    - [Requesting Tokens](#requesting-tokens)
    - [Refreshing Tokens](#refreshing-tokens)
    - [Revoking Tokens](#revoking-tokens)
    - [Purging Tokens](#purging-tokens)
- [Authorization Code Grant With PKCE](#code-grant-pkce)
    - [Creating the Client](#creating-a-auth-pkce-grant-client)
    - [Requesting Tokens](#requesting-auth-pkce-grant-tokens)
- [Password Grant Tokens](#password-grant-tokens)
    - [Creating a Password Grant Client](#creating-a-password-grant-client)
    - [Requesting Tokens](#requesting-password-grant-tokens)
    - [Requesting All Scopes](#requesting-all-scopes)
    - [Customizing the User Provider](#customizing-the-user-provider)
    - [Customizing the Username Field](#customizing-the-username-field)
    - [Customizing the Password Validation](#customizing-the-password-validation)
- [Implicit Grant Tokens](#implicit-grant-tokens)
- [Client Credentials Grant Tokens](#client-credentials-grant-tokens)
- [Personal Access Tokens](#personal-access-tokens)
    - [Creating a Personal Access Client](#creating-a-personal-access-client)
    - [Managing Personal Access Tokens](#managing-personal-access-tokens)
- [Protecting Routes](#protecting-routes)
    - [Via Middleware](#via-middleware)
    - [Passing the Access Token](#passing-the-access-token)
- [Token Scopes](#token-scopes)
    - [Defining Scopes](#defining-scopes)
    - [Default Scope](#default-scope)
    - [Assigning Scopes to Tokens](#assigning-scopes-to-tokens)
    - [Checking Scopes](#checking-scopes)
- [Consuming Your API With JavaScript](#consuming-your-api-with-javascript)
- [Events](#events)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Passport](https://github.com/laravel/passport) provides a full OAuth2 server implementation for your Laravel application in a matter of minutes. Passport is built on top of the [League OAuth2 server](https://github.com/thephpleague/oauth2-server) that is maintained by Andy Millington and Simon Hamp. -->
[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에 몇 분 만에 완전한 OAuth2 서버를 구축할 수 있도록 해주는 패키지입니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 만들어졌습니다.

> [!WARNING]
> 이 문서는 여러분이 OAuth2에 대해 기본적으로 알고 있다는 전제 하에 작성되었습니다. OAuth2에 대한 지식이 없으시다면, 먼저 [terminology](https://oauth2.thephpleague.com/terminology/) 및 기본적인 기능을 익힌 후에 이 문서를 읽으시길 권장합니다.

<a name="passport-or-sanctum"></a>
<!-- ### Passport or Sanctum? -->
### Passport or Sanctum?

<!-- Before getting started, you may wish to determine if your application would be better served by Laravel Passport or [Laravel Sanctum](/docs/10.x/sanctum). If your application absolutely needs to support OAuth2, then you should use Laravel Passport. -->
시작하기 전에, 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/10.x/sanctum) 중 어떤 것이 더 적합한지 판단하는 것이 좋습니다. 만약 애플리케이션에서 반드시 OAuth2를 지원해야만 한다면, Laravel Passport를 사용하는 것이 맞습니다.

<!-- However, if you are attempting to authenticate a single-page application, mobile application, or issue API tokens, you should use [Laravel Sanctum](/docs/10.x/sanctum). Laravel Sanctum does not support OAuth2; however, it provides a much simpler API authentication development experience. -->
하지만 싱글 페이지 애플리케이션(SPA), 모바일 애플리케이션, 또는 단순한 API 토큰 발급이 필요하다면 [Laravel Sanctum](/docs/10.x/sanctum)을 사용하는 것이 더 나은 선택일 수 있습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 간단한 방식으로 API 인증 기능을 구현할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Passport via the Composer package manager: -->
먼저, Composer 패키지 매니저를 통해 Passport를 설치합니다:

```shell
composer require laravel/passport
```

<!-- Passport's [service provider](/docs/10.x/providers) registers its own database migration directory, so you should migrate your database after installing the package. The Passport migrations will create the tables your application needs to store OAuth2 clients and access tokens: -->
Passport의 [service provider](/docs/10.x/providers)가 자체적으로 데이터베이스 마이그레이션 디렉터리를 등록하기 때문에, 패키지를 설치한 후에는 데이터베이스 마이그레이션을 실행해야 합니다. Passport 마이그레이션은 OAuth2 클라이언트와 액세스 토큰 관련 테이블을 생성합니다:

```shell
php artisan migrate
```

<!-- Next, you should execute the `passport:install` Artisan command. This command will create the encryption keys needed to generate secure access tokens. In addition, the command will create "personal access" and "password grant" clients which will be used to generate access tokens: -->
다음으로, `passport:install` 아티즌 명령어를 실행해야 합니다. 이 명령어는 보안 액세스 토큰을 생성할 때 필요한 암호화 키를 만들어줍니다. 또한, 이 명령어는 "personal access"와 "password grant" 클라이언트를 생성해서, 액세스 토큰 발급에 활용할 수 있도록 해줍니다:

```shell
php artisan passport:install
```

> [!NOTE]
> Passport의 `Client` 모델에서 자동 증가 정수(ID) 대신 UUID를 기본키 값으로 사용하고자 한다면, [the `uuids` option](#client-uuids)을 참고하여 Passport를 설치하세요.

<!-- After running the `passport:install` command, add the `Laravel\Passport\HasApiTokens` trait to your `App\Models\User` model. This trait will provide a few helper methods to your model which allow you to inspect the authenticated user's token and scopes. If your model is already using the `Laravel\Sanctum\HasApiTokens` trait, you may remove that trait: -->
`passport:install` 명령을 모두 실행한 후, `App\Models\User` 사용자 모델에 `Laravel\Passport\HasApiTokens` 트레잇을 추가하세요. 이 트레잇은 인증된 유저의 토큰 및 스코프를 확인할 수 있는 유용한 메서드들을 제공합니다. 만약 기존에 `Laravel\Sanctum\HasApiTokens` 트레잇을 사용하고 있다면, 해당 트레잇은 제거해도 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

<!-- Finally, in your application's `config/auth.php` configuration file, you should define an `api` authentication guard and set the `driver` option to `passport`. This will instruct your application to use Passport's `TokenGuard` when authenticating incoming API requests: -->
마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서, `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면, API 요청 인증 시 Passport의 `TokenGuard`가 사용되도록 지정할 수 있습니다.

```
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],

    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],
],
```

<a name="client-uuids"></a>
<!-- #### Client UUIDs -->
#### Client UUIDs

<!-- You may also run the `passport:install` command with the `--uuids` option present. This option will instruct Passport that you would like to use UUIDs instead of auto-incrementing integers as the Passport `Client` model's primary key values. After running the `passport:install` command with the `--uuids` option, you will be given additional instructions regarding disabling Passport's default migrations: -->
`--uuids` 옵션과 함께 `passport:install` 명령어를 실행할 수도 있습니다. 이 옵션을 사용하면 Passport `Client` 모델의 기본키 값으로 자동 증가 정수 대신 UUID를 사용하도록 Passport에 지시합니다. `--uuids` 옵션과 함께 `passport:install` 명령어를 실행한 후에는, Passport의 기본 마이그레이션을 비활성화하는 추가 안내를 받게 됩니다:

```shell
php artisan passport:install --uuids
```

<a name="deploying-passport"></a>
<!-- ### Deploying Passport -->
### Deploying Passport

<!-- When deploying Passport to your application's servers for the first time, you will likely need to run the `passport:keys` command. This command generates the encryption keys Passport needs in order to generate access tokens. The generated keys are not typically kept in source control: -->
처음으로 서버에 Passport를 배포할 때는, `passport:keys` 명령어를 실행해야 할 수도 있습니다. 이 명령어는 토큰 발급과 검증에 필요한 암호화 키를 생성합니다. 보통 이 키들은 버전 관리(소스 컨트롤)에 포함하지 않습니다.

```shell
php artisan passport:keys
```

<!-- If necessary, you may define the path where Passport's keys should be loaded from. You may use the `Passport::loadKeysFrom` method to accomplish this. Typically, this method should be called from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
경우에 따라, Passport의 키 로딩 경로를 직접 지정할 수 있습니다. 이때는 `Passport::loadKeysFrom` 메서드를 사용하면 되며, 보통 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```
/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
<!-- #### Loading Keys From the Environment -->
#### Loading Keys From the Environment

<!-- Alternatively, you may publish Passport's configuration file using the `vendor:publish` Artisan command: -->
또는, `vendor:publish` 아티즌 명령어로 Passport의 설정 파일을 퍼블리시할 수도 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

<!-- After the configuration file has been published, you may load your application's encryption keys by defining them as environment variables: -->
설정 파일을 퍼블리시한 후, 다음과 같이 애플리케이션의 암호화 키를 환경 변수로 지정해 Passport에서 읽어들이도록 할 수 있습니다:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="migration-customization"></a>
<!-- ### Migration Customization -->
### Migration Customization

<!-- If you are not going to use Passport's default migrations, you should call the `Passport::ignoreMigrations` method in the `register` method of your `App\Providers\AppServiceProvider` class. You may export the default migrations using the `vendor:publish` Artisan command: -->
Passport의 기본 마이그레이션을 사용하지 않고 자체 마이그레이션을 정의하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Passport::ignoreMigrations`를 호출하면 됩니다. 기본 마이그레이션은 아래와 같이 `vendor:publish` 명령으로 내보낼 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-migrations
```

<a name="upgrading-passport"></a>
<!-- ### Upgrading Passport -->
### Upgrading Passport

<!-- When upgrading to a new major version of Passport, it's important that you carefully review [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md). -->
Passport의 메이저 버전을 업그레이드할 때는, 반드시 [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="client-secret-hashing"></a>
<!-- ### Client Secret Hashing -->
### Client Secret Hashing

<!-- If you would like your client's secrets to be hashed when stored in your database, you should call the `Passport::hashClientSecrets` method in the `boot` method of your `App\Providers\AuthServiceProvider` class: -->
클라이언트 시크릿 값을 데이터베이스에 저장할 때 해싱 처리하고 싶다면, `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::hashClientSecrets`를 호출하면 됩니다:

```
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

<!-- Once enabled, all of your client secrets will only be displayable to the user immediately after they are created. Since the plain-text client secret value is never stored in the database, it is not possible to recover the secret's value if it is lost. -->
이 기능을 활성화하면, 각 클라이언트 생성 직후에만 해시되지 않은(본문 그대로의) 시크릿 값을 확인할 수 있습니다. 평문 시크릿 값이 데이터베이스에 저장되지 않으므로, 시크릿 값을 분실했을 경우 복구는 불가능합니다.

<a name="token-lifetimes"></a>
<!-- ### Token Lifetimes -->
### Token Lifetimes

<!-- By default, Passport issues long-lived access tokens that expire after one year. If you would like to configure a longer / shorter token lifetime, you may use the `tokensExpireIn`, `refreshTokensExpireIn`, and `personalAccessTokensExpireIn` methods. These methods should be called from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
기본적으로, Passport는 만료 기간이 1년인 장수명 액세스 토큰을 발급합니다. 토큰의 만료 기간을 더 길거나 짧게 조정하려면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 보통 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```
/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    Passport::tokensExpireIn(now()->addDays(15));
    Passport::refreshTokensExpireIn(now()->addDays(30));
    Passport::personalAccessTokensExpireIn(now()->addMonths(6));
}
```

> [!WARNING]
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며, 표시용으로만 사용됩니다. 토큰 발급 시, 만료 정보는 서명되고 암호화된 토큰 내부에 저장됩니다. 토큰을 무효화하려면 [revoke it](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- You are free to extend the models used internally by Passport by defining your own model and extending the corresponding Passport model: -->
Passport에서 내부적으로 사용하는 모델을 직접 확장(상속)해서 모델을 교체할 수 있습니다. 예를 들어, 여러분만의 모델을 만든 후, Passport가 해당 모델을 사용하도록 할 수 있습니다.

```
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

<!-- After defining your model, you may instruct Passport to use your custom model via the `Laravel\Passport\Passport` class. Typically, you should inform Passport about your custom models in the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
모델을 정의한 후, `Laravel\Passport\Passport` 클래스를 통해 커스텀 모델을 Passport에 등록하면 됩니다. 보통은 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 Passport에 모델을 등록합니다.

```
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\PersonalAccessClient;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;

/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::usePersonalAccessClientModel(PersonalAccessClient::class);
}
```

<a name="overriding-routes"></a>
<!-- ### Overriding Routes -->
### Overriding Routes

<!-- Sometimes you may wish to customize the routes defined by Passport. To achieve this, you first need to ignore the routes registered by Passport by adding `Passport::ignoreRoutes` to the `register` method of your application's `AppServiceProvider`: -->
Passport에서 미리 정의한 라우트를 직접 커스터마이즈하고 싶을 때가 있습니다. 이 경우 먼저, 애플리케이션의 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하여 Passport가 라우트를 등록하지 않도록 해야 합니다.

```
use Laravel\Passport\Passport;

/**
 * Register any application services.
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```

<!-- Then, you may copy the routes defined by Passport in [its routes file](https://github.com/laravel/passport/blob/11.x/routes/web.php) to your application's `routes/web.php` file and modify them to your liking: -->
그 다음, [its routes file](https://github.com/laravel/passport/blob/11.x/routes/web.php)에 정의된 라우트를 애플리케이션의 `routes/web.php`로 복사해서 자유롭게 변경할 수 있습니다.

```
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport routes...
});
```

<a name="issuing-access-tokens"></a>
<!-- ## Issuing Access Tokens -->
## Issuing Access Tokens

<!-- Using OAuth2 via authorization codes is how most developers are familiar with OAuth2. When using authorization codes, a client application will redirect a user to your server where they will either approve or deny the request to issue an access token to the client. -->
대부분의 개발자들이 OAuth2에서 익숙하게 사용하는 방식이 바로 인가 코드(authorization codes)를 통한 방식입니다. 인가 코드를 사용할 때는, 클라이언트 애플리케이션이 사용자를 여러분의 서버로 리다이렉트 시키고, 사용자는 클라이언트에 액세스 토큰 제공을 승인하거나 거부하게 됩니다.

<a name="managing-clients"></a>
<!-- ### Managing Clients -->
### Managing Clients

<!-- First, developers building applications that need to interact with your application's API will need to register their application with yours by creating a "client". Typically, this consists of providing the name of their application and a URL that your application can redirect to after users approve their request for authorization. -->
여러분의 애플리케이션에 API로 접근하려는 외부 애플리케이션을 개발하는 개발자는, 반드시 자신의 애플리케이션을 여러분의 서비스에 "클라이언트"로 등록해야 합니다. 일반적으로, 애플리케이션 이름과, 사용자가 인가를 승인한 뒤에 리다이렉트될 URL 정보를 제공해야 합니다.

<a name="the-passportclient-command"></a>
<!-- #### The `passport:client` Command -->
#### The `passport:client` Command

<!-- The simplest way to create a client is using the `passport:client` Artisan command. This command may be used to create your own clients for testing your OAuth2 functionality. When you run the `client` command, Passport will prompt you for more information about your client and will provide you with a client ID and secret: -->
클라이언트를 가장 쉽게 생성하는 방법은 `passport:client` 아티즌 명령어를 사용하는 것입니다. 이 명령어로 OAuth2 기능을 테스트하기 위해 직접 클라이언트를 만들 수 있습니다. `client` 명령어를 실행하면, Passport가 클라이언트에 대한 추가 정보를 물어본 뒤 클라이언트 ID와 시크릿을 발급해줍니다.

```shell
php artisan passport:client
```

<!-- **Redirect URLs** -->
**리다이렉트 URL**

<!-- If you would like to allow multiple redirect URLs for your client, you may specify them using a comma-delimited list when prompted for the URL by the `passport:client` command. Any URLs which contain commas should be URL encoded: -->
클라이언트에 여러 리다이렉트 URL을 허용하고 싶다면, `passport:client` 명령어를 실행할 때 URL 입력란에 콤마(,)로 구분해서 여러 주소를 입력하면 됩니다. 만약 URL 자체에 콤마가 포함되어 있다면, 반드시 URL 인코딩을 해주어야 합니다.

```shell
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
<!-- #### JSON API -->
#### JSON API

<!-- Since your application's users will not be able to utilize the `client` command, Passport provides a JSON API that you may use to create clients. This saves you the trouble of having to manually code controllers for creating, updating, and deleting clients. -->
애플리케이션의 일반 사용자는 `client` 명령어를 사용할 수 없기 때문에, Passport는 클라이언트 관리에 활용할 수 있는 JSON API도 제공합니다. 이 API를 사용하면, 직접 컨트롤러를 만들어서 생성/수정/삭제 기능을 구현할 필요 없이 클라이언트를 관리할 수 있습니다.

<!-- However, you will need to pair Passport's JSON API with your own frontend to provide a dashboard for your users to manage their clients. Below, we'll review all of the API endpoints for managing clients. For convenience, we'll use [Axios](https://github.com/axios/axios) to demonstrate making HTTP requests to the endpoints. -->
다만, Passport의 JSON API와 프론트엔드를 연동해서, 사용자가 클라이언트를 직접 관리할 수 있는 대시보드를 만들어줘야 합니다. 아래에서는 각 엔드포인트 별로 클라이언트 관리에 사용되는 API를 정리합니다. 예제에서는 [Axios](https://github.com/axios/axios)를 사용해 HTTP 요청 예시를 보여줍니다.

<!-- The JSON API is guarded by the `web` and `auth` middleware; therefore, it may only be called from your own application. It is not able to be called from an external source. -->
JSON API는 반드시 `web` 미들웨어와 `auth` 미들웨어를 통과해야 하므로, 반드시 여러분의 애플리케이션 내부에서만 호출할 수 있습니다. 외부 애플리케이션이나 사용자는 접근할 수 없습니다.

<a name="get-oauthclients"></a>
<!-- #### `GET /oauth/clients` -->
#### `GET /oauth/clients`

<!-- This route returns all of the clients for the authenticated user. This is primarily useful for listing all of the user's clients so that they may edit or delete them: -->
이 라우트는 인증된 사용자가 생성한 모든 클라이언트 목록을 반환합니다. 클라이언트 관리 대시보드에서 사용자가 클라이언트를 확인, 편집, 삭제할 때 주로 활용됩니다.

```js
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
<!-- #### `POST /oauth/clients` -->
#### `POST /oauth/clients`

<!-- This route is used to create new clients. It requires two pieces of data: the client's `name` and a `redirect` URL. The `redirect` URL is where the user will be redirected after approving or denying a request for authorization. -->
이 엔드포인트는 새로운 클라이언트를 생성할 때 사용합니다. 반드시 클라이언트의 `name`과 `redirect` URL 두 가지 정보가 필요합니다. `redirect` URL은 사용자가 인가 요청을 승인 또는 거부한 뒤에 이동할 주소입니다.

<!-- When a client is created, it will be issued a client ID and client secret. These values will be used when requesting access tokens from your application. The client creation route will return the new client instance: -->
클라이언트가 생성되면, 클라이언트 ID와 시크릿이 발급됩니다. 이 값들은 여러분이 토큰을 요청할 때 사용됩니다. API는 생성된 클라이언트 객체를 반환합니다.

```js
const data = {
    name: 'Client Name',
    redirect: 'http://example.com/callback'
};

axios.post('/oauth/clients', data)
    .then(response => {
        console.log(response.data);
    })
    .catch (response => {
        // List errors on response...
    });
```

<a name="put-oauthclientsclient-id"></a>
<!-- #### `PUT /oauth/clients/{client-id}` -->
#### `PUT /oauth/clients/{client-id}`

<!-- This route is used to update clients. It requires two pieces of data: the client's `name` and a `redirect` URL. The `redirect` URL is where the user will be redirected after approving or denying a request for authorization. The route will return the updated client instance: -->
이 엔드포인트는 클라이언트를 수정할 때 사용합니다. 클라이언트의 `name`과 `redirect` URL 두 가지 정보가 필요합니다. `redirect` URL은 사용자가 인가 요청을 승인 또는 거부한 뒤에 리다이렉트될 주소입니다. 이 엔드포인트는 변경된 클라이언트 인스턴스를 반환합니다.

```js
const data = {
    name: 'New Client Name',
    redirect: 'http://example.com/callback'
};

axios.put('/oauth/clients/' + clientId, data)
    .then(response => {
        console.log(response.data);
    })
    .catch (response => {
        // List errors on response...
    });
```

<a name="delete-oauthclientsclient-id"></a>
<!-- #### `DELETE /oauth/clients/{client-id}` -->
#### `DELETE /oauth/clients/{client-id}`

<!-- This route is used to delete clients: -->
이 엔드포인트는 클라이언트를 삭제할 때 사용합니다.

```js
axios.delete('/oauth/clients/' + clientId)
    .then(response => {
        // ...
    });
```

<a name="requesting-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="requesting-tokens-redirecting-for-authorization"></a>
<!-- #### Redirecting for Authorization -->
#### Redirecting for Authorization

<!-- Once a client has been created, developers may use their client ID and secret to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route like so: -->
클라이언트를 생성한 후, 개발자는 해당 클라이언트의 ID, 시크릿을 사용해 인가 코드 및 액세스 토큰을 요청할 수 있습니다. 우선, 소비 애플리케이션에서 여러분의 애플리케이션 `/oauth/authorize` 라우트로 리다이렉트 요청을 보냅니다.

```
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'client-id',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => '',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

<!-- The `prompt` parameter may be used to specify the authentication behavior of the Passport application. -->
`prompt` 파라미터는 Passport 애플리케이션의 인증 행동 방식을 지정할 때 사용할 수 있습니다.

<!-- If the `prompt` value is `none`, Passport will always throw an authentication error if the user is not already authenticated with the Passport application. If the value is `consent`, Passport will always display the authorization approval screen, even if all scopes were previously granted to the consuming application. When the value is `login`, the Passport application will always prompt the user to re-login to the application, even if they already have an existing session. -->
`prompt` 값이 `none`이면, 사용자가 아직 Passport 애플리케이션에 인증되어 있지 않을 경우 Passport는 항상 인증 에러를 발생시킵니다. 값이 `consent`라면, 이미 모든 스코프가 소비 애플리케이션에 허가된 경우라도 Passport는 항상 인가 승인 화면을 표시합니다. 값이 `login`이면, 기존에 세션이 있더라도 Passport 애플리케이션은 항상 사용자에게 애플리케이션 재로그인을 요청합니다.

<!-- If no `prompt` value is provided, the user will be prompted for authorization only if they have not previously authorized access to the consuming application for the requested scopes. -->
`prompt` 값을 명시하지 않으면, 사용자가 해당 스코프에 대해 이전에 인가하지 않았다면 인가 화면이 표시되며, 이미 인가했다면 별도의 승인은 필요하지 않습니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport에서 이미 등록되어 있으니, 별도로 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
<!-- #### Approving the Request -->
#### Approving the Request

<!-- When receiving authorization requests, Passport will automatically respond based on the value of `prompt` parameter (if present) and may display a template to the user allowing them to approve or deny the authorization request. If they approve the request, they will be redirected back to the `redirect_uri` that was specified by the consuming application. The `redirect_uri` must match the `redirect` URL that was specified when the client was created. -->
인가 요청을 수신하면, Passport는 `prompt` 파라미터 값에 따라 동작하며(존재하는 경우), 사용자에게 인가 화면을 보여주거나 자동으로 승인/거부 응답을 처리합니다. 사용자가 요청을 승인하면, 클라이언트가 설정한 `redirect_uri`로 리다이렉트 됩니다. 이때 `redirect_uri`는 클라이언트 생성 시 등록한 `redirect` URL과 일치해야 합니다.

<!-- If you would like to customize the authorization approval screen, you may publish Passport's views using the `vendor:publish` Artisan command. The published views will be placed in the `resources/views/vendor/passport` directory: -->
인가 승인 화면을 직접 커스터마이즈하고 싶을 때는, `vendor:publish` 아티즌 명령어로 Passport 뷰를 퍼블리시할 수 있습니다. 퍼블리시된 뷰는 `resources/views/vendor/passport` 디렉터리에 복사됩니다.

```shell
php artisan vendor:publish --tag=passport-views
```

<!-- Sometimes you may wish to skip the authorization prompt, such as when authorizing a first-party client. You may accomplish this by [extending the `Client` model](#overriding-default-models) and defining a `skipsAuthorization` method. If `skipsAuthorization` returns `true` the client will be approved and the user will be redirected back to the `redirect_uri` immediately, unless the consuming application has explicitly set the `prompt` parameter when redirecting for authorization: -->
일부 상황에서는, 예를 들어 1차 클라이언트(자신이 만든 서비스 등)를 인가할 때처럼 인가 프롬프트를 건너뛰고 싶을 수도 있습니다. 이 경우 [extending the `Client` model](#overriding-default-models)한 뒤 `skipsAuthorization` 메서드를 정의하면 됩니다. `skipsAuthorization`이 `true`를 반환하면, 소비 애플리케이션이 인가 리다이렉트 시 `prompt` 파라미터를 명시적으로 설정하지 않은 한, 클라이언트가 승인되고 사용자는 즉시 `redirect_uri`로 리다이렉트됩니다.

```
<?php

namespace App\Models\Passport;

use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * Determine if the client should skip the authorization prompt.
     */
    public function skipsAuthorization(): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
<!-- #### Converting Authorization Codes to Access Tokens -->
#### Converting Authorization Codes to Access Tokens

<!-- If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should first verify the `state` parameter against the value that was stored prior to the redirect. If the state parameter matches then the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request: -->
사용자가 인가 요청을 승인하면, 소비 애플리케이션으로 다시 리다이렉트됩니다. 소비 애플리케이션에서는 먼저 `state` 파라미터를 리다이렉트 전 저장한 값과 대조(검증)해야 합니다. 상태값이 일치하면, 애플리케이션이 여러분의 서버로 `POST` 요청을 보내 액세스 토큰을 요청할 수 있습니다. 이때, 사용자가 인가 요청을 승인할 때 발급된 인증 코드도 함께 전달해야 합니다.

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class,
        'Invalid state value.'
    );

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<!-- This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires. -->
`/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. 이 중 `expires_in`은 액세스 토큰이 만료되기까지 남은 초를 의미합니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로, `/oauth/token` 라우트도 Passport에서 이미 정의되어 있으니, 별도로 추가할 필요가 없습니다.

<a name="tokens-json-api"></a>
<!-- #### JSON API -->
#### JSON API

<!-- Passport also includes a JSON API for managing authorized access tokens. You may pair this with your own frontend to offer your users a dashboard for managing access tokens. For convenience, we'll use [Axios](https://github.com/mzabriskie/axios) to demonstrate making HTTP requests to the endpoints. The JSON API is guarded by the `web` and `auth` middleware; therefore, it may only be called from your own application. -->
Passport는 인가된 액세스 토큰을 관리할 수 있도록 별도의 JSON API도 제공합니다. 이 API를 이용해 여러분만의 프론트엔드와 연동하여, 사용자가 자신의 액세스 토큰을 직접 관리할 수 있는 대시보드를 구축할 수 있습니다. 아래 예시에서도 [Axios](https://github.com/mzabriskie/axios)로 엔드포인트에 요청을 보내는 방법을 안내합니다. 이 API 역시 `web` 및 `auth` 미들웨어로 보호되므로, 반드시 애플리케이션 내부에서만 호출할 수 있습니다.

<a name="get-oauthtokens"></a>
<!-- #### `GET /oauth/tokens` -->
#### `GET /oauth/tokens`

<!-- This route returns all of the authorized access tokens that the authenticated user has created. This is primarily useful for listing all of the user's tokens so that they can revoke them: -->
이 라우트는 인증된 사용자가 생성한 모든 인가된 액세스 토큰의 목록을 반환합니다. 사용자가 자신의 토큰을 확인, 폐기할 수 있도록 리스트를 만드는 데 유용합니다.

```js
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
<!-- #### `DELETE /oauth/tokens/{token-id}` -->
#### `DELETE /oauth/tokens/{token-id}`

<!-- This route may be used to revoke authorized access tokens and their related refresh tokens: -->
이 라우트는 인가된 액세스 토큰과 관련된 리프레시 토큰까지 함께 취소(폐기)할 때 사용할 수 있습니다.

```js
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
<!-- ### Refreshing Tokens -->
### Refreshing Tokens

<!-- If your application issues short-lived access tokens, users will need to refresh their access tokens via the refresh token that was provided to them when the access token was issued: -->
만약 애플리케이션에서 단기 유효 액세스 토큰(짧은 만료 기간)을 발급한다면, 사용자는 액세스 토큰이 만료될 때마다 발급 시 함께 제공된 리프레시 토큰을 활용해 토큰을 갱신해야 합니다.

```
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'scope' => '',
]);

return $response->json();
```

<!-- This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires. -->
`/oauth/token` 라우트는 다시 한 번, `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in`은 토큰 만료까지 남은 초를 나타냅니다.

<a name="revoking-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- You may revoke a token by using the `revokeAccessToken` method on the `Laravel\Passport\TokenRepository`. You may revoke a token's refresh tokens using the `revokeRefreshTokensByAccessTokenId` method on the `Laravel\Passport\RefreshTokenRepository`. These classes may be resolved using Laravel's [service container](/docs/10.x/container): -->
토큰을 폐기하고 싶을 때는 `Laravel\Passport\TokenRepository`의 `revokeAccessToken` 메서드를 사용할 수 있습니다. 특정 액세스 토큰에 연결된 리프레시 토큰도 같이 폐기하고 싶을 때는, `Laravel\Passport\RefreshTokenRepository`의 `revokeRefreshTokensByAccessTokenId` 메서드를 사용할 수 있습니다. 이 클래스들은 Laravel의 [service container](/docs/10.x/container)에서 바로 주입받을 수 있습니다.

```
use Laravel\Passport\TokenRepository;
use Laravel\Passport\RefreshTokenRepository;

$tokenRepository = app(TokenRepository::class);
$refreshTokenRepository = app(RefreshTokenRepository::class);

// Revoke an access token...
$tokenRepository->revokeAccessToken($tokenId);

// Revoke all of the token's refresh tokens...
$refreshTokenRepository->revokeRefreshTokensByAccessTokenId($tokenId);
```

<a name="purging-tokens"></a>

<!-- ### Purging Tokens -->
### Purging Tokens

<!-- When tokens have been revoked or expired, you might want to purge them from the database. Passport's included `passport:purge` Artisan command can do this for you: -->
토큰이 폐기되었거나 만료된 경우, 데이터베이스에서 해당 토큰을 정리하고 싶을 수 있습니다. Passport에 포함된 `passport:purge` 아티즌 명령어를 사용해 이 작업을 수행할 수 있습니다.

```shell
# Purge revoked and expired tokens and auth codes...
php artisan passport:purge

# Only purge tokens expired for more than 6 hours...
php artisan passport:purge --hours=6

# Only purge revoked tokens and auth codes...
php artisan passport:purge --revoked

# Only purge expired tokens and auth codes...
php artisan passport:purge --expired
```

<!-- You may also configure a [scheduled job](/docs/10.x/scheduling) in your application's `App\Console\Kernel` class to automatically prune your tokens on a schedule: -->
또한, 애플리케이션의 `App\Console\Kernel` 클래스에서 [scheduled job](/docs/10.x/scheduling)을 설정하여 토큰 정리를 자동화할 수 있습니다.

```
/**
 * Define the application's command schedule.
 */
protected function schedule(Schedule $schedule): void
{
    $schedule->command('passport:purge')->hourly();
}
```

<a name="code-grant-pkce"></a>
<!-- ## Authorization Code Grant With PKCE -->
## Authorization Code Grant With PKCE

<!-- The Authorization Code grant with "Proof Key for Code Exchange" (PKCE) is a secure way to authenticate single page applications or native applications to access your API. This grant should be used when you can't guarantee that the client secret will be stored confidentially or in order to mitigate the threat of having the authorization code intercepted by an attacker. A combination of a "code verifier" and a "code challenge" replaces the client secret when exchanging the authorization code for an access token. -->
"Proof Key for Code Exchange"(PKCE)가 포함된 인증 코드 그랜트는, 싱글 페이지 애플리케이션(SPA)이나 네이티브 애플리케이션처럼 클라이언트 비밀을 안전하게 보관할 수 없는 경우, 또는 인가 코드가 공격자에게 가로채지는 것을 방지하고 싶을 때 안전하게 API를 인증할 수 있는 방식입니다. 이 방식에서는 클라이언트 비밀 대신, "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)"의 조합을 사용하여 인가 코드를 액세스 토큰으로 교환합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
<!-- ### Creating the Client -->
### Creating the Client

<!-- Before your application can issue tokens via the authorization code grant with PKCE, you will need to create a PKCE-enabled client. You may do this using the `passport:client` Artisan command with the `--public` option: -->
애플리케이션에서 PKCE가 적용된 인증 코드 그랜트를 통해 토큰을 발급하려면, 먼저 PKCE를 지원하는 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어에 `--public` 옵션을 사용하여 생성할 수 있습니다.

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="code-verifier-code-challenge"></a>
<!-- #### Code Verifier and Code Challenge -->
#### Code Verifier and Code Challenge

<!-- As this authorization grant does not provide a client secret, developers will need to generate a combination of a code verifier and a code challenge in order to request a token. -->
이 인증 방식은 클라이언트 비밀을 제공하지 않으므로, 개발자는 토큰을 요청할 때 코드 검증자와 코드 챌린지의 조합을 생성해야 합니다.

<!-- The code verifier should be a random string of between 43 and 128 characters containing letters, numbers, and  `"-"`, `"."`, `"_"`, `"~"` characters, as defined in the [RFC 7636 specification](https://tools.ietf.org/html/rfc7636). -->
코드 검증자는 [RFC 7636 specification](https://tools.ietf.org/html/rfc7636)에 정의된 대로, 영문자와 숫자, 그리고 `"-"`, `"."`, `"_"`, `"~"` 문자를 포함한 43~128자 길이의 임의의 문자열이어야 합니다.

<!-- The code challenge should be a Base64 encoded string with URL and filename-safe characters. The trailing `'='` characters should be removed and no line breaks, whitespace, or other additional characters should be present. -->
코드 챌린지는 URL 및 파일 이름에 안전한 문자로 이루어진 Base64 인코딩 문자열이어야 하며, 끝에 오는 `'='` 문자는 제거하고 줄바꿈, 공백 등 추가 문자가 없어야 합니다.

```
$encoded = base64_encode(hash('sha256', $code_verifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
<!-- #### Redirecting for Authorization -->
#### Redirecting for Authorization

<!-- Once a client has been created, you may use the client ID and the generated code verifier and code challenge to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route: -->
클라이언트가 생성되면, 클라이언트 ID와 위에서 생성한 코드 검증자 및 코드 챌린지를 이용해 인가 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 사용하는 애플리케이션에서 `/oauth/authorize` 경로로 리다이렉트 요청을 보냅니다.

```
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $request->session()->put(
        'code_verifier', $code_verifier = Str::random(128)
    );

    $codeChallenge = strtr(rtrim(
        base64_encode(hash('sha256', $code_verifier, true))
    , '='), '+/', '-_');

    $query = http_build_query([
        'client_id' => 'client-id',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => '',
        'state' => $state,
        'code_challenge' => $codeChallenge,
        'code_challenge_method' => 'S256',
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
<!-- #### Converting Authorization Codes to Access Tokens -->
#### Converting Authorization Codes to Access Tokens

<!-- If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should verify the `state` parameter against the value that was stored prior to the redirect, as in the standard Authorization Code Grant. -->
사용자가 인가 요청을 승인하면, 사용자는 다시 사용 애플리케이션으로 리다이렉트됩니다. 이때, 표준 인증 코드 그랜트와 마찬가지로, 사용자는 리다이렉트 전에 세션에 저장한 `state` 값을 확인해야 합니다.

<!-- If the state parameter matches, the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request along with the originally generated code verifier: -->
state 파라미터가 일치하면, 발급받은 인가 코드와 함께 처음 생성한 코드 검증자를 포함하여 애플리케이션에 `POST` 요청을 보내 액세스 토큰을 요청해야 합니다.

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    $codeVerifier = $request->session()->pull('code_verifier');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
    );

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'client-id',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'code_verifier' => $codeVerifier,
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<a name="password-grant-tokens"></a>
<!-- ## Password Grant Tokens -->
## Password Grant Tokens

> [!WARNING]
> 패스워드 그랜트 토큰 사용은 더 이상 권장하지 않습니다. 대신 [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하시기 바랍니다.

<!-- The OAuth2 password grant allows your other first-party clients, such as a mobile application, to obtain an access token using an email address / username and password. This allows you to issue access tokens securely to your first-party clients without requiring your users to go through the entire OAuth2 authorization code redirect flow. -->
OAuth2 패스워드 그랜트를 통해, 모바일 애플리케이션과 같은 1차 애플리케이션에서 이메일 주소/사용자명과 비밀번호로 액세스 토큰을 받을 수 있습니다. 이 방법을 사용하면 사용자가 전체 OAuth2 인가 코드 리다이렉트 과정을 거치지 않고도, 1차 애플리케이션에 안전하게 액세스 토큰을 발급할 수 있습니다.

<a name="creating-a-password-grant-client"></a>
<!-- ### Creating a Password Grant Client -->
### Creating a Password Grant Client

<!-- Before your application can issue tokens via the password grant, you will need to create a password grant client. You may do this using the `passport:client` Artisan command with the `--password` option. **If you have already run the `passport:install` command, you do not need to run this command:** -->
패스워드 그랜트를 통해 토큰을 발급하려면, 먼저 패스워드 그랜트 클라이언트를 만들어야 합니다. `passport:client` 아티즌 명령어에 `--password` 옵션을 사용해 생성할 수 있습니다. **이미 `passport:install` 명령어를 실행했다면 이 명령어는 다시 실행할 필요가 없습니다.**

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<!-- Once you have created a password grant client, you may request an access token by issuing a `POST` request to the `/oauth/token` route with the user's email address and password. Remember, this route is already registered by Passport so there is no need to define it manually. If the request is successful, you will receive an `access_token` and `refresh_token` in the JSON response from the server: -->
패스워드 그랜트 클라이언트를 생성하였다면, 사용자의 이메일 주소와 비밀번호를 포함하여 `/oauth/token` 경로에 `POST` 요청을 보내 액세스 토큰을 요청할 수 있습니다. 이 경로는 Passport에서 이미 등록되어 있으므로, 별도로 정의할 필요가 없습니다. 요청이 성공하면, 서버의 JSON 응답에서 `access_token`과 `refresh_token`을 받을 수 있습니다.

```
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 만료 기간이 깁니다. 필요한 경우 [configure your maximum access token lifetime](#configuration)할 수 있습니다.

<a name="requesting-all-scopes"></a>
<!-- ### Requesting All Scopes -->
### Requesting All Scopes

<!-- When using the password grant or client credentials grant, you may wish to authorize the token for all of the scopes supported by your application. You can do this by requesting the `*` scope. If you request the `*` scope, the `can` method on the token instance will always return `true`. This scope may only be assigned to a token that is issued using the `password` or `client_credentials` grant: -->
패스워드 그랜트나 클라이언트 자격 증명 그랜트(client credentials grant)를 사용할 때, 애플리케이션에서 지원하는 모든 스코프에 대해 토큰을 발급하고 싶을 수 있습니다. 이때는 `*` 스코프를 요청하면 됩니다. `*` 스코프를 요청하면, 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환하게 됩니다. 이 스코프는 오직 `password` 또는 `client_credentials` 그랜트로 발급된 토큰에만 할당할 수 있습니다.

```
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
<!-- ### Customizing the User Provider -->
### Customizing the User Provider

<!-- If your application uses more than one [authentication user provider](/docs/10.x/authentication#introduction), you may specify which user provider the password grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --password` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#via-middleware) to ensure that only users from the guard's specified provider are authorized. -->
애플리케이션에서 여러 [authentication user provider](/docs/10.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --password` 명령을 실행할 때 `--provider` 옵션을 지정하여 패스워드 그랜트 클라이언트가 사용할 프로바이더를 정할 수 있습니다. 지정한 프로바이더 이름은 `config/auth.php` 설정 파일에 정의된 올바른 프로바이더와 일치해야 합니다. 그 후, [protect your route using middleware](#via-middleware)하여 해당 guard의 프로바이더로부터 인증된 사용자만 접근할 수 있도록 할 수 있습니다.

<a name="customizing-the-username-field"></a>
<!-- ### Customizing the Username Field -->
### Customizing the Username Field

<!-- When authenticating using the password grant, Passport will use the `email` attribute of your authenticatable model as the "username". However, you may customize this behavior by defining a `findForPassport` method on your model: -->
패스워드 그랜트 인증시, Passport는 기본적으로 인증 가능한 모델의 `email` 속성을 "사용자명"으로 사용합니다. 그러나 이 동작을 커스터마이즈하려면, 모델에 `findForPassport` 메서드를 정의하세요.

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Find the user instance for the given username.
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
<!-- ### Customizing the Password Validation -->
### Customizing the Password Validation

<!-- When authenticating using the password grant, Passport will use the `password` attribute of your model to validate the given password. If your model does not have a `password` attribute or you wish to customize the password validation logic, you can define a `validateForPassportPasswordGrant` method on your model: -->
패스워드 그랜트 인증시 Passport는 모델의 `password` 속성을 사용해 비밀번호를 검증합니다. 모델에 `password` 속성이 없거나, 비밀번호 검증 방식을 커스터마이징하고 싶을 경우, 모델에 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Hash;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Validate the password of the user for the Passport password grant.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant-tokens"></a>
<!-- ## Implicit Grant Tokens -->
## Implicit Grant Tokens

> [!WARNING]
> 임플리시트 그랜트 토큰 사용은 더 이상 권장하지 않습니다. 대신 [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하세요.

<!-- The implicit grant is similar to the authorization code grant; however, the token is returned to the client without exchanging an authorization code. This grant is most commonly used for JavaScript or mobile applications where the client credentials can't be securely stored. To enable the grant, call the `enableImplicitGrant` method in the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
임플리시트(Implicit) 그랜트는 인증 코드 그랜트와 비슷하지만, 인가 코드를 교환하는 절차 없이 바로 토큰이 클라이언트로 반환됩니다. 이 방식은 클라이언트 비밀을 안전하게 저장할 수 없는 JavaScript 또는 모바일 애플리케이션에서 주로 사용됩니다. 이 방식을 활성화하려면, 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하세요.

```
/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

<!-- Once the grant has been enabled, developers may use their client ID to request an access token from your application. The consuming application should make a redirect request to your application's `/oauth/authorize` route like so: -->
임플리시트 그랜트가 활성화된 후, 개발자는 클라이언트 ID를 활용해 애플리케이션에 액세스 토큰을 요청할 수 있습니다. 사용하는 애플리케이션에서는 `/oauth/authorize` 경로로 리다이렉트 요청을 아래와 같이 보냅니다.

```
use Illuminate\Http\Request;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'client-id',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'response_type' => 'token',
        'scope' => '',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> `/oauth/authorize` 경로는 Passport에서 이미 정의되어 있으므로 별도로 정의할 필요가 없습니다.

<a name="client-credentials-grant-tokens"></a>
<!-- ## Client Credentials Grant Tokens -->
## Client Credentials Grant Tokens

<!-- The client credentials grant is suitable for machine-to-machine authentication. For example, you might use this grant in a scheduled job which is performing maintenance tasks over an API. -->
클라이언트 자격 증명 그랜트는 머신끼리의 인증에 적합합니다. 예를 들어, 스케줄된 작업이 API를 통해 유지보수 작업을 수행할 때 이 그랜트를 사용할 수 있습니다.

<!-- Before your application can issue tokens via the client credentials grant, you will need to create a client credentials grant client. You may do this using the `--client` option of the `passport:client` Artisan command: -->
이 그랜트를 통해 토큰을 발급하려면, 먼저 클라이언트 자격 증명 그랜트 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어의 `--client` 옵션을 사용하면 생성할 수 있습니다.

```shell
php artisan passport:client --client
```

<!-- Next, to use this grant type, you may add the `CheckClientCredentials` middleware to the `$middlewareAliases` property of your application's `app/Http/Kernel.php` file: -->
다음으로, 이 그랜트 타입을 사용하려면, 애플리케이션의 `app/Http/Kernel.php` 파일의 `$middlewareAliases` 속성에 `CheckClientCredentials` 미들웨어를 등록합니다.

```
use Laravel\Passport\Http\Middleware\CheckClientCredentials;

protected $middlewareAliases = [
    'client' => CheckClientCredentials::class,
];
```

<!-- Then, attach the middleware to a route: -->
이제 해당 미들웨어를 라우트에 적용합니다.

```
Route::get('/orders', function (Request $request) {
    ...
})->middleware('client');
```

<!-- To restrict access to the route to specific scopes, you may provide a comma-delimited list of the required scopes when attaching the `client` middleware to the route: -->
특정 스코프에 대해서만 접근을 허용하고 싶다면, 라우트에 `client` 미들웨어를 적용할 때 쉼표로 구분된 필요한 스코프 목록을 지정할 수 있습니다.

```
Route::get('/orders', function (Request $request) {
    ...
})->middleware('client:check-status,your-scope');
```

<a name="retrieving-tokens"></a>
<!-- ### Retrieving Tokens -->
### Retrieving Tokens

<!-- To retrieve a token using this grant type, make a request to the `oauth/token` endpoint: -->
이 그랜트 타입으로 토큰을 받으려면, `oauth/token` 엔드포인트로 요청을 보내면 됩니다.

```
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'scope' => 'your-scope',
]);

return $response->json()['access_token'];
```

<a name="personal-access-tokens"></a>
<!-- ## Personal Access Tokens -->
## Personal Access Tokens

<!-- Sometimes, your users may want to issue access tokens to themselves without going through the typical authorization code redirect flow. Allowing users to issue tokens to themselves via your application's UI can be useful for allowing users to experiment with your API or may serve as a simpler approach to issuing access tokens in general. -->
경우에 따라 사용자가 인가 코드 리다이렉트 흐름을 거치지 않고 직접 자신의 액세스 토큰을 발급받고 싶어할 수 있습니다. 사용자에게 애플리케이션의 UI를 통해 직접 토큰을 발급하게 하면, API 테스트 또는 보다 간편하게 액세스 토큰을 발급하고자 할 때 유용할 수 있습니다.

> [!NOTE]
> 애플리케이션이 주로 개인 액세스 토큰 발급 용도로 Passport를 사용한다면, Laravel의 경량 1차 API 토큰 라이브러리인 [Laravel Sanctum](/docs/10.x/sanctum) 사용을 고려해보세요.

<a name="creating-a-personal-access-client"></a>
<!-- ### Creating a Personal Access Client -->
### Creating a Personal Access Client

<!-- Before your application can issue personal access tokens, you will need to create a personal access client. You may do this by executing the `passport:client` Artisan command with the `--personal` option. If you have already run the `passport:install` command, you do not need to run this command: -->
개인 액세스 토큰을 발급하려면, 먼저 개인 액세스 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어의 `--personal` 옵션을 사용해 생성할 수 있습니다. 이미 `passport:install` 명령어를 실행했다면 이 명령어는 다시 실행할 필요가 없습니다.

```shell
php artisan passport:client --personal
```

<!-- After creating your personal access client, place the client's ID and plain-text secret value in your application's `.env` file: -->
개인 액세스 클라이언트를 생성한 후, 해당 클라이언트의 ID와 평문 비밀 값을 애플리케이션의 `.env` 파일에 아래와 같이 설정해 주세요.

```ini
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
<!-- ### Managing Personal Access Tokens -->
### Managing Personal Access Tokens

<!-- Once you have created a personal access client, you may issue tokens for a given user using the `createToken` method on the `App\Models\User` model instance. The `createToken` method accepts the name of the token as its first argument and an optional array of [scopes](#token-scopes) as its second argument: -->
개인 액세스 클라이언트를 생성했으면, `App\Models\User` 모델 인스턴스의 `createToken` 메서드를 사용해 사용자를 위한 토큰을 발급할 수 있습니다. `createToken` 메서드는 토큰 이름을 첫 번째 인수로, [scopes](#token-scopes) 배열(옵션)을 두 번째 인수로 받을 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

// Creating a token without scopes...
$token = $user->createToken('Token Name')->accessToken;

// Creating a token with scopes...
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="personal-access-tokens-json-api"></a>
<!-- #### JSON API -->
#### JSON API

<!-- Passport also includes a JSON API for managing personal access tokens. You may pair this with your own frontend to offer your users a dashboard for managing personal access tokens. Below, we'll review all of the API endpoints for managing personal access tokens. For convenience, we'll use [Axios](https://github.com/mzabriskie/axios) to demonstrate making HTTP requests to the endpoints. -->
Passport는 개인 액세스 토큰을 관리할 수 있는 JSON API도 제공합니다. 이를 프론트엔드와 연동하면, 사용자에게 손쉽게 개인 액세스 토큰을 관리하는 대시보드를 제공할 수 있습니다. 아래에서는 이 API 엔드포인트들을 [Axios](https://github.com/mzabriskie/axios)를 활용한 예시와 함께 소개합니다.

<!-- The JSON API is guarded by the `web` and `auth` middleware; therefore, it may only be called from your own application. It is not able to be called from an external source. -->
이 JSON API는 `web` 및 `auth` 미들웨어에 의해 보호되므로, 오직 자체 애플리케이션에서만 호출할 수 있습니다. 외부에서 직접 호출할 수는 없습니다.

<a name="get-oauthscopes"></a>
<!-- #### `GET /oauth/scopes` -->
#### `GET /oauth/scopes`

<!-- This route returns all of the [scopes](#token-scopes) defined for your application. You may use this route to list the scopes a user may assign to a personal access token: -->
이 경로는 애플리케이션에 정의된 모든 [scopes](#token-scopes)를 반환합니다. 사용자가 개인 액세스 토큰에 부여할 수 있는 스코프 목록을 표시할 때 활용할 수 있습니다.

```js
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
<!-- #### `GET /oauth/personal-access-tokens` -->
#### `GET /oauth/personal-access-tokens`

<!-- This route returns all of the personal access tokens that the authenticated user has created. This is primarily useful for listing all of the user's tokens so that they may edit or revoke them: -->
이 경로는 인증된 사용자가 생성한 모든 개인 액세스 토큰을 반환합니다. 주로 사용자가 본인의 토큰을 조회하거나, 수정·폐기할 수 있도록 목록을 제공할 때 사용합니다.

```js
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
<!-- #### `POST /oauth/personal-access-tokens` -->
#### `POST /oauth/personal-access-tokens`

<!-- This route creates new personal access tokens. It requires two pieces of data: the token's `name` and the `scopes` that should be assigned to the token: -->
이 경로는 새로운 개인 액세스 토큰을 생성합니다. 요청 시 토큰의 `name`과 해당 토큰에 부여할 `scopes` 데이터가 필요합니다.

```js
const data = {
    name: 'Token Name',
    scopes: []
};

axios.post('/oauth/personal-access-tokens', data)
    .then(response => {
        console.log(response.data.accessToken);
    })
    .catch (response => {
        // List errors on response...
    });
```

<a name="delete-oauthpersonal-access-tokenstoken-id"></a>
<!-- #### `DELETE /oauth/personal-access-tokens/{token-id}` -->
#### `DELETE /oauth/personal-access-tokens/{token-id}`

<!-- This route may be used to revoke personal access tokens: -->
이 경로는 개인 액세스 토큰을 폐기(삭제)할 때 사용합니다.

```js
axios.delete('/oauth/personal-access-tokens/' + tokenId);
```

<a name="protecting-routes"></a>
<!-- ## Protecting Routes -->
## Protecting Routes

<a name="via-middleware"></a>
<!-- ### Via Middleware -->
### Via Middleware

<!-- Passport includes an [authentication guard](/docs/10.x/authentication#adding-custom-guards) that will validate access tokens on incoming requests. Once you have configured the `api` guard to use the `passport` driver, you only need to specify the `auth:api` middleware on any routes that should require a valid access token: -->
Passport에는 요청이 들어왓을 때 액세스 토큰을 검증해주는 [authentication guard](/docs/10.x/authentication#adding-custom-guards)가 포함되어 있습니다. `api` 가드를 `passport` 드라이버로 설정한 경우, 유효한 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어만 지정하면 됩니다.

```
Route::get('/user', function () {
    // ...
})->middleware('auth:api');
```

> [!WARNING]
> [client credentials grant](#client-credentials-grant-tokens)를 사용하는 경우, 해당 라우트 보호에는 `auth:api` 미들웨어 대신 [the `client` middleware](#client-credentials-grant-tokens)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
<!-- #### Multiple Authentication Guards -->
#### Multiple Authentication Guards

<!-- If your application authenticates different types of users that perhaps use entirely different Eloquent models, you will likely need to define a guard configuration for each user provider type in your application. This allows you to protect requests intended for specific user providers. For example, given the following guard configuration the `config/auth.php` configuration file: -->
애플리케이션에서 서로 다른 Eloquent 모델을 사용하는 여러 종류의 사용자를 인증해야 한다면, 각 사용자 프로바이더 유형별로 가드 설정을 따로 정의해야 할 수 있습니다. 이를 통해 특정 사용자 프로바이더에 맞춘 요청만 보호할 수 있습니다. 예를 들어, `config/auth.php`에 아래와 같이 가드 설정이 있을 때:

```
'api' => [
    'driver' => 'passport',
    'provider' => 'users',
],

'api-customers' => [
    'driver' => 'passport',
    'provider' => 'customers',
],
```

<!-- The following route will utilize the `api-customers` guard, which uses the `customers` user provider, to authenticate incoming requests: -->
아래 라우트는 `customers` 사용자 프로바이더를 사용하는 `api-customers` 가드를 통해 인증된 요청만 허용합니다.

```
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자(providers)를 사용하는 방법에 대한 자세한 내용은 [password grant documentation](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
<!-- ### Passing the Access Token -->
### Passing the Access Token

<!-- When calling routes that are protected by Passport, your application's API consumers should specify their access token as a `Bearer` token in the `Authorization` header of their request. For example, when using the Guzzle HTTP library: -->
Passport로 보호된 라우트에 요청을 보낼 때, API 클라이언트는 요청의 `Authorization` 헤더에 액세스 토큰을 `Bearer` 토큰으로 지정해야 합니다. 예를 들어 Guzzle HTTP 라이브러리를 사용할 때는 다음과 같이 요청합니다.

```
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => 'Bearer '.$accessToken,
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
<!-- ## Token Scopes -->
## Token Scopes

<!-- Scopes allow your API clients to request a specific set of permissions when requesting authorization to access an account. For example, if you are building an e-commerce application, not all API consumers will need the ability to place orders. Instead, you may allow the consumers to only request authorization to access order shipment statuses. In other words, scopes allow your application's users to limit the actions a third-party application can perform on their behalf. -->
스코프는 API 클라이언트가 계정 접근 권한을 요청할 때, 어떤 권한이 필요한지 구체적으로 지정할 수 있게 합니다. 예를 들어, 이커머스 애플리케이션에서 모든 API 소비자가 주문을 생성할 필요는 없습니다. 대신, 주문 발송 상태만 조회할 권한을 요청하도록 제한할 수 있습니다. 즉, 스코프를 활용해 사용자는 제3자 애플리케이션이 자신을 대신해 할 수 있는 작업의 범위를 제한할 수 있습니다.

<a name="defining-scopes"></a>
<!-- ### Defining Scopes -->
### Defining Scopes

<!-- You may define your API's scopes using the `Passport::tokensCan` method in the `boot` method of your application's `App\Providers\AuthServiceProvider` class. The `tokensCan` method accepts an array of scope names and scope descriptions. The scope description may be anything you wish and will be displayed to users on the authorization approval screen: -->
API의 스코프는 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 정의할 수 있습니다. `tokensCan` 메서드에는 스코프 이름과 설명(사용자에게 표시될 내용)을 배열로 지정합니다.

```
/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'place-orders' => 'Place orders',
        'check-status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
<!-- ### Default Scope -->
### Default Scope

<!-- If a client does not request any specific scopes, you may configure your Passport server to attach default scope(s) to the token using the `setDefaultScope` method. Typically, you should call this method from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
클라이언트에서 특정 스코프를 요청하지 않은 경우, Passport 서버가 토큰에 기본 스코프를 부여하도록 `setDefaultScope` 메서드로 설정할 수 있습니다. 보통 이 메서드는 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```
use Laravel\Passport\Passport;

Passport::tokensCan([
    'place-orders' => 'Place orders',
    'check-status' => 'Check order status',
]);

Passport::setDefaultScope([
    'check-status',
    'place-orders',
]);
```

> [!NOTE]
> Passport의 기본 스코프 설정은 사용자가 직접 발급한 개인 액세스 토큰에는 적용되지 않습니다.

<a name="assigning-scopes-to-tokens"></a>

<!-- ### Assigning Scopes to Tokens -->
### Assigning Scopes to Tokens

<a name="when-requesting-authorization-codes"></a>
<!-- #### When Requesting Authorization Codes -->
#### When Requesting Authorization Codes

<!-- When requesting an access token using the authorization code grant, consumers should specify their desired scopes as the `scope` query string parameter. The `scope` parameter should be a space-delimited list of scopes: -->
Authorization Code Grant를 사용하여 액세스 토큰을 요청할 때, 소비자는 원하는 스코프를 `scope` 쿼리 문자열 파라미터로 지정해야 합니다. `scope` 파라미터에는 스코프 이름을 공백으로 구분하여 나열해야 합니다.

```
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => 'client-id',
        'redirect_uri' => 'http://example.com/callback',
        'response_type' => 'code',
        'scope' => 'place-orders check-status',
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="when-issuing-personal-access-tokens"></a>
<!-- #### When Issuing Personal Access Tokens -->
#### When Issuing Personal Access Tokens

<!-- If you are issuing personal access tokens using the `App\Models\User` model's `createToken` method, you may pass the array of desired scopes as the second argument to the method: -->
`App\Models\User` 모델의 `createToken` 메서드를 사용해서 개인 액세스 토큰을 발급할 때는, 두 번째 인수로 원하는 스코프들을 배열로 전달할 수 있습니다.

```
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="checking-scopes"></a>
<!-- ### Checking Scopes -->
### Checking Scopes

<!-- Passport includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given scope. To get started, add the following middleware to the `$middlewareAliases` property of your `app/Http/Kernel.php` file: -->
Passport에는 들어오는 요청이 주어진 스코프로 발급받은 토큰으로 인증되었는지 확인해주는 두 가지 미들웨어가 포함되어 있습니다. 먼저, 아래와 같이 `app/Http/Kernel.php` 파일의 `$middlewareAliases` 속성에 미들웨어를 등록해야 합니다.

```
'scopes' => \Laravel\Passport\Http\Middleware\CheckScopes::class,
'scope' => \Laravel\Passport\Http\Middleware\CheckForAnyScope::class,
```

<a name="check-for-all-scopes"></a>
<!-- #### Check For All Scopes -->
#### Check For All Scopes

<!-- The `scopes` middleware may be assigned to a route to verify that the incoming request's access token has all of the listed scopes: -->
`scopes` 미들웨어를 라우트에 지정하면, 들어오는 요청의 액세스 토큰이 나열된 모든 스코프를 가지고 있는지 확인할 수 있습니다.

```
Route::get('/orders', function () {
    // Access token has both "check-status" and "place-orders" scopes...
})->middleware(['auth:api', 'scopes:check-status,place-orders']);
```

<a name="check-for-any-scopes"></a>
<!-- #### Check for Any Scopes -->
#### Check for Any Scopes

<!-- The `scope` middleware may be assigned to a route to verify that the incoming request's access token has *at least one* of the listed scopes: -->
`scope` 미들웨어를 라우트에 지정하면, 들어오는 요청의 액세스 토큰이 나열된 스코프 중 *하나 이상*을 가지고 있는지 확인할 수 있습니다.

```
Route::get('/orders', function () {
    // Access token has either "check-status" or "place-orders" scope...
})->middleware(['auth:api', 'scope:check-status,place-orders']);
```

<a name="checking-scopes-on-a-token-instance"></a>
<!-- #### Checking Scopes on a Token Instance -->
#### Checking Scopes on a Token Instance

<!-- Once an access token authenticated request has entered your application, you may still check if the token has a given scope using the `tokenCan` method on the authenticated `App\Models\User` instance: -->
액세스 토큰으로 인증된 요청이 애플리케이션 안으로 들어온 후에도, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 사용해 해당 토큰에 특정 스코프가 포함되어 있는지 추가로 확인할 수 있습니다.

```
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('place-orders')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
<!-- #### Additional Scope Methods -->
#### Additional Scope Methods

<!-- The `scopeIds` method will return an array of all defined IDs / names: -->
`scopeIds` 메서드는 정의된 모든 ID/이름의 배열을 반환합니다.

```
use Laravel\Passport\Passport;

Passport::scopeIds();
```

<!-- The `scopes` method will return an array of all defined scopes as instances of `Laravel\Passport\Scope`: -->
`scopes` 메서드는 `Laravel\Passport\Scope` 인스턴스 배열로 모든 정의된 스코프를 반환합니다.

```
Passport::scopes();
```

<!-- The `scopesFor` method will return an array of `Laravel\Passport\Scope` instances matching the given IDs / names: -->
`scopesFor` 메서드는 전달된 ID/이름에 맞는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다.

```
Passport::scopesFor(['place-orders', 'check-status']);
```

<!-- You may determine if a given scope has been defined using the `hasScope` method: -->
특정 스코프가 정의되어 있는지 확인하려면 `hasScope` 메서드를 사용할 수 있습니다.

```
Passport::hasScope('place-orders');
```

<a name="consuming-your-api-with-javascript"></a>
<!-- ## Consuming Your API With JavaScript -->
## Consuming Your API With JavaScript

<!-- When building an API, it can be extremely useful to be able to consume your own API from your JavaScript application. This approach to API development allows your own application to consume the same API that you are sharing with the world. The same API may be consumed by your web application, mobile applications, third-party applications, and any SDKs that you may publish on various package managers. -->
API를 구축할 때, JavaScript 애플리케이션에서 자신의 API를 직접 소비할 수 있다는 것은 매우 유용한 접근 방식입니다. 이렇게 하면 본인의 웹 애플리케이션, 모바일 앱, 서드파티 앱, 그리고 각종 패키지 관리자에서 배포하는 SDK가 하나의 API를 함께 사용할 수 있게 됩니다.

<!-- Typically, if you want to consume your API from your JavaScript application, you would need to manually send an access token to the application and pass it with each request to your application. However, Passport includes a middleware that can handle this for you. All you need to do is add the `CreateFreshApiToken` middleware to your `web` middleware group in your `app/Http/Kernel.php` file: -->
일반적으로 JavaScript 애플리케이션에서 자신의 API를 호출할 때에는 직접 액세스 토큰을 전달하고, 이 토큰을 모든 요청마다 포함해야 합니다. 하지만 Passport는 이를 자동으로 처리할 수 있는 미들웨어를 제공합니다. 즉, `app/Http/Kernel.php` 파일의 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하면 됩니다.

```
'web' => [
    // Other middleware...
    \Laravel\Passport\Http\Middleware\CreateFreshApiToken::class,
],
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어가 반드시 미들웨어 스택의 마지막에 위치해야 합니다.

<!-- This middleware will attach a `laravel_token` cookie to your outgoing responses. This cookie contains an encrypted JWT that Passport will use to authenticate API requests from your JavaScript application. The JWT has a lifetime equal to your `session.lifetime` configuration value. Now, since the browser will automatically send the cookie with all subsequent requests, you may make requests to your application's API without explicitly passing an access token: -->
이 미들웨어는 응답에 `laravel_token`이라는 쿠키를 자동으로 추가합니다. 이 쿠키에는 Passport에서 인증에 사용하는 암호화된 JWT가 들어 있습니다. JWT의 유효 기간은 `session.lifetime` 설정 값과 동일합니다. 브라우저가 이 쿠키를 자동으로 모든 후속 요청에 포함하기 때문에, API를 호출할 때 액세스 토큰을 명시적으로 전달할 필요가 없습니다.

```
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
<!-- #### Customizing the Cookie Name -->
#### Customizing the Cookie Name

<!-- If needed, you can customize the `laravel_token` cookie's name using the `Passport::cookie` method. Typically, this method should be called from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
필요하다면, `Passport::cookie` 메서드를 사용하여 `laravel_token` 쿠키 이름을 커스터마이즈할 수 있습니다. 이 메서드는 대개 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```
/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- When using this method of authentication, you will need to ensure a valid CSRF token header is included in your requests. The default Laravel JavaScript scaffolding includes an Axios instance, which will automatically use the encrypted `XSRF-TOKEN` cookie value to send an `X-XSRF-TOKEN` header on same-origin requests. -->
이 인증 방식을 이용할 때는, 요청에 유효한 CSRF 토큰 헤더가 반드시 포함되어야 합니다. 기본 Laravel JavaScript 스캐폴딩은 Axios 인스턴스를 포함하며, 이 인스턴스는 암호화된 `XSRF-TOKEN` 쿠키 값을 자동으로 읽어 같은 도메인 요청의 `X-XSRF-TOKEN` 헤더로 전송합니다.

> [!NOTE]
> 만약 `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 보내고 싶다면, `csrf_token()`에서 제공하는 암호화되지 않은 토큰을 사용해야 합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Passport raises events when issuing access tokens and refresh tokens. You may use these events to prune or revoke other access tokens in your database. If you would like, you may attach listeners to these events in your application's `App\Providers\EventServiceProvider` class: -->
Passport는 액세스 토큰 및 리프레시 토큰이 발급될 때 이벤트를 발생시킵니다. 이 이벤트들을 이용해 데이터베이스에 있는 다른 액세스 토큰을 정리하거나 폐기할 수 있습니다. 원한다면, 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 리스너를 연결할 수 있습니다.

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Laravel\Passport\Events\AccessTokenCreated' => [
        'App\Listeners\RevokeOldTokens',
    ],

    'Laravel\Passport\Events\RefreshTokenCreated' => [
        'App\Listeners\PruneOldTokens',
    ],
];
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Passport's `actingAs` method may be used to specify the currently authenticated user as well as its scopes. The first argument given to the `actingAs` method is the user instance and the second is an array of scopes that should be granted to the user's token: -->
Passport의 `actingAs` 메서드는 현재 인증된 사용자와, 그 토큰에 부여할 스코프를 지정할 수 있습니다. `actingAs` 메서드의 첫 번째 인수에는 유저 인스턴스를, 두 번째 인수에는 허용할 스코프 배열을 전달합니다.

```
use App\Models\User;
use Laravel\Passport\Passport;

public function test_servers_can_be_created(): void
{
    Passport::actingAs(
        User::factory()->create(),
        ['create-servers']
    );

    $response = $this->post('/api/create-server');

    $response->assertStatus(201);
}
```

<!-- Passport's `actingAsClient` method may be used to specify the currently authenticated client as well as its scopes. The first argument given to the `actingAsClient` method is the client instance and the second is an array of scopes that should be granted to the client's token: -->
Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트와, 그 토큰에 부여할 스코프를 지정할 수 있습니다. `actingAsClient` 메서드의 첫 번째 인수에는 클라이언트 인스턴스를, 두 번째 인수에는 허용할 스코프 배열을 전달합니다.

```
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_orders_can_be_retrieved(): void
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['check-status']
    );

    $response = $this->get('/api/orders');

    $response->assertStatus(200);
}
```
