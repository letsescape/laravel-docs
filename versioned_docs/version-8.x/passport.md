<!-- # Laravel Passport -->
# Laravel Passport

- [Introduction](#introduction)
    - [Passport Or Sanctum?](#passport-or-sanctum)
- [Installation](#installation)
    - [Deploying Passport](#deploying-passport)
    - [Migration Customization](#migration-customization)
    - [Upgrading Passport](#upgrading-passport)
- [Configuration](#configuration)
    - [Client Secret Hashing](#client-secret-hashing)
    - [Token Lifetimes](#token-lifetimes)
    - [Overriding Default Models](#overriding-default-models)
- [Issuing Access Tokens](#issuing-access-tokens)
    - [Managing Clients](#managing-clients)
    - [Requesting Tokens](#requesting-tokens)
    - [Refreshing Tokens](#refreshing-tokens)
    - [Revoking Tokens](#revoking-tokens)
    - [Purging Tokens](#purging-tokens)
- [Authorization Code Grant with PKCE](#code-grant-pkce)
    - [Creating The Client](#creating-a-auth-pkce-grant-client)
    - [Requesting Tokens](#requesting-auth-pkce-grant-tokens)
- [Password Grant Tokens](#password-grant-tokens)
    - [Creating A Password Grant Client](#creating-a-password-grant-client)
    - [Requesting Tokens](#requesting-password-grant-tokens)
    - [Requesting All Scopes](#requesting-all-scopes)
    - [Customizing The User Provider](#customizing-the-user-provider)
    - [Customizing The Username Field](#customizing-the-username-field)
    - [Customizing The Password Validation](#customizing-the-password-validation)
- [Implicit Grant Tokens](#implicit-grant-tokens)
- [Client Credentials Grant Tokens](#client-credentials-grant-tokens)
- [Personal Access Tokens](#personal-access-tokens)
    - [Creating A Personal Access Client](#creating-a-personal-access-client)
    - [Managing Personal Access Tokens](#managing-personal-access-tokens)
- [Protecting Routes](#protecting-routes)
    - [Via Middleware](#via-middleware)
    - [Passing The Access Token](#passing-the-access-token)
- [Token Scopes](#token-scopes)
    - [Defining Scopes](#defining-scopes)
    - [Default Scope](#default-scope)
    - [Assigning Scopes To Tokens](#assigning-scopes-to-tokens)
    - [Checking Scopes](#checking-scopes)
- [Consuming Your API With JavaScript](#consuming-your-api-with-javascript)
- [Events](#events)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Passport](https://github.com/laravel/passport) provides a full OAuth2 server implementation for your Laravel application in a matter of minutes. Passport is built on top of the [League OAuth2 server](https://github.com/thephpleague/oauth2-server) that is maintained by Andy Millington and Simon Hamp. -->
[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션을 위한 완전한 OAuth2 서버 구현을 몇 분 만에 구축할 수 있도록 해줍니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되어 있습니다.

> [!NOTE]
> 이 문서는 독자가 이미 OAuth2에 대해 어느 정도 알고 있다는 것을 전제로 작성되었습니다. OAuth2에 대해 전혀 모르실 경우, 계속 읽기 전에 먼저 일반적인 [terminology](https://oauth2.thephpleague.com/terminology/)을 익히시길 권장합니다.

<a name="passport-or-sanctum"></a>
<!-- ### Passport Or Sanctum? -->
### Passport Or Sanctum?

<!-- Before getting started, you may wish to determine if your application would be better served by Laravel Passport or [Laravel Sanctum](/docs/8.x/sanctum). If your application absolutely needs to support OAuth2, then you should use Laravel Passport. -->
본격적으로 시작하기 전에, 여러분의 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/8.x/sanctum) 중 어느 것이 더 적합할지 고민해볼 필요가 있습니다. 만약 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

<!-- However, if you are attempting to authenticate a single-page application, mobile application, or issue API tokens, you should use [Laravel Sanctum](/docs/8.x/sanctum). Laravel Sanctum does not support OAuth2; however, it provides a much simpler API authentication development experience. -->
그러나 단일 페이지 애플리케이션(SPA), 모바일 앱, 또는 단순히 API 토큰 발급을 목적으로 인증 기능을 구현하려는 경우에는 [Laravel Sanctum](/docs/8.x/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2 프로토콜 자체는 지원하지 않지만, 훨씬 더 간단하게 API 인증을 개발할 수 있게 해줍니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Passport via the Composer package manager: -->
먼저 Composer 패키지 매니저를 이용해 Passport를 설치합니다.

```
composer require laravel/passport
```

<!-- Passport's [service provider](/docs/8.x/providers) registers its own database migration directory, so you should migrate your database after installing the package. The Passport migrations will create the tables your application needs to store OAuth2 clients and access tokens: -->
Passport의 [service provider](/docs/8.x/providers)는 자체 데이터베이스 마이그레이션 디렉터리를 등록하므로, 패키지 설치 후 데이터베이스 마이그레이션을 수행해야 합니다. Passport 마이그레이션은 애플리케이션이 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 테이블들을 생성합니다.

```
php artisan migrate
```

<!-- Next, you should execute the `passport:install` Artisan command. This command will create the encryption keys needed to generate secure access tokens. In addition, the command will create "personal access" and "password grant" clients which will be used to generate access tokens: -->
다음으로 `passport:install` 아티즌 명령어를 실행합니다. 이 명령어는 보안 액세스 토큰 생성을 위한 암호화 키를 만듭니다. 또, "퍼스널 액세스" 및 "패스워드 그랜트" 클라이언트도 함께 생성되어, 액세스 토큰을 발급할 때 사용됩니다.

```
php artisan passport:install
```

> [!TIP]
> Passport의 `Client` 모델의 기본 키(primary key)를 auto-increment 정수 대신 UUID로 사용하고 싶다면, [the `uuids` option](#client-uuids)을 참고해 설치하세요.

<!-- After running the `passport:install` command, add the `Laravel\Passport\HasApiTokens` trait to your `App\Models\User` model. This trait will provide a few helper methods to your model which allow you to inspect the authenticated user's token and scopes. If your model is already using the `Laravel\Sanctum\HasApiTokens` trait, you may remove that trait: -->
`passport:install` 명령어 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가하세요. 이 트레이트는 인증된 사용자의 토큰 및 스코프를 검사할 수 있는 몇 가지 헬퍼 메서드를 제공합니다. 이미 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용하고 있다면, 이제는 해당 트레이트를 제거해도 됩니다.

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

<!-- Next, you should call the `Passport::routes` method within the `boot` method of your `App\Providers\AuthServiceProvider`. This method will register the routes necessary to issue access tokens and revoke access tokens, clients, and personal access tokens: -->
이제 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 안에서 `Passport::routes` 메서드를 호출해야 합니다. 이 메서드는 액세스 토큰 발급∙취소, 클라이언트 관리, 퍼스널 액세스 토큰 관련 경로를 자동으로 등록합니다.

```
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;
use Laravel\Passport\Passport;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * The policy mappings for the application.
     *
     * @var array
     */
    protected $policies = [
        'App\Models\Model' => 'App\Policies\ModelPolicy',
    ];

    /**
     * Register any authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        if (! $this->app->routesAreCached()) {
            Passport::routes();
        }
    }
}
```

<!-- Finally, in your application's `config/auth.php` configuration file, you should set the `driver` option of the `api` authentication guard to `passport`. This will instruct your application to use Passport's `TokenGuard` when authenticating incoming API requests: -->
마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드의 `driver` 옵션을 `passport`로 설정합니다. 이제 애플리케이션은 API 요청 인증 시 Passport의 `TokenGuard`를 사용하게 됩니다.

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
`--uuids` 옵션과 함께 `passport:install` 명령어를 실행할 수도 있습니다. 이 옵션을 사용하면 Passport `Client` 모델의 기본 키 값으로 auto-increment 정수 대신 UUID를 사용하도록 Passport에 지시합니다. `--uuids` 옵션과 함께 `passport:install` 명령어를 실행한 후에는, Passport의 기본 마이그레이션을 비활성화하는 추가 지침을 받게 됩니다.

```
php artisan passport:install --uuids
```

<a name="deploying-passport"></a>
<!-- ### Deploying Passport -->
### Deploying Passport

<!-- When deploying Passport to your application's servers for the first time, you will likely need to run the `passport:keys` command. This command generates the encryption keys Passport needs in order to generate access tokens. The generated keys are not typically kept in source control: -->
애플리케이션 서버에 처음으로 Passport를 배포할 때는 `passport:keys` 명령어를 실행해야 합니다. 이 명령어는 액세스 토큰 생성에 필요한 암호화 키를 생성합니다. 이 키들은 보통 소스 코드 저장소에 커밋하지 않습니다.

```
php artisan passport:keys
```

<!-- If necessary, you may define the path where Passport's keys should be loaded from. You may use the `Passport::loadKeysFrom` method to accomplish this. Typically, this method should be called from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
필요하다면 Passport 키를 불러올 경로를 따로 지정할 수도 있습니다. 이때 `Passport::loadKeysFrom` 메서드를 사용할 수 있으며, 보통 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
<!-- #### Loading Keys From The Environment -->
#### Loading Keys From The Environment

<!-- Alternatively, you may publish Passport's configuration file using the `vendor:publish` Artisan command: -->
또한, `vendor:publish` 아티즌 명령어를 사용해서 Passport의 설정 파일을 퍼블리시할 수도 있습니다.

```
php artisan vendor:publish --tag=passport-config
```

<!-- After the configuration file has been published, you may load your application's encryption keys by defining them as environment variables: -->
설정 파일을 퍼블리시하고 나면, 애플리케이션의 암호화 키를 환경 변수로 지정해 불러올 수 있습니다.

```bash
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
Passport의 기본 마이그레이션을 사용하지 않을 계획이라면, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Passport::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션 파일들은 `vendor:publish` 아티즌 명령어로 별도 복사(export)할 수 있습니다.

```
php artisan vendor:publish --tag=passport-migrations
```

<a name="upgrading-passport"></a>
<!-- ### Upgrading Passport -->
### Upgrading Passport

<!-- When upgrading to a new major version of Passport, it's important that you carefully review [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md). -->
Passport의 새로운 주요 버전으로 업그레이드할 때는, [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼하게 확인하는 것이 중요합니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="client-secret-hashing"></a>
<!-- ### Client Secret Hashing -->
### Client Secret Hashing

<!-- If you would like your client's secrets to be hashed when stored in your database, you should call the `Passport::hashClientSecrets` method in the `boot` method of your `App\Providers\AuthServiceProvider` class: -->
클라이언트의 시크릿을 데이터베이스에 저장할 때 해시 형태로 저장하고 싶다면, `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::hashClientSecrets` 메서드를 호출하세요.

```
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

<!-- Once enabled, all of your client secrets will only be displayable to the user immediately after they are created. Since the plain-text client secret value is never stored in the database, it is not possible to recover the secret's value if it is lost. -->
이 설정을 활성화하면, 모든 클라이언트 시크릿은 생성 직후에만 사용자에게 보여지며, 평문(plain-text) 시크릿 값은 데이터베이스에 저장되지 않습니다. 즉, 시크릿을 분실하면 복구가 불가능하게 됩니다.

<a name="token-lifetimes"></a>
<!-- ### Token Lifetimes -->
### Token Lifetimes

<!-- By default, Passport issues long-lived access tokens that expire after one year. If you would like to configure a longer / shorter token lifetime, you may use the `tokensExpireIn`, `refreshTokensExpireIn`, and `personalAccessTokensExpireIn` methods. These methods should be called from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
기본적으로 Passport에서 발급되는 액세스 토큰의 만료 시한은 1년입니다. 더 긴 또는 더 짧은 만료 기간을 설정하고 싶다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

```
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::tokensExpireIn(now()->addDays(15));
    Passport::refreshTokensExpireIn(now()->addDays(30));
    Passport::personalAccessTokensExpireIn(now()->addMonths(6));
}
```

> [!NOTE]
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며 단지 표시 목적으로만 사용됩니다. 실제 만료 정보는 서명 및 암호화된 토큰 자체에 저장됩니다. 토큰을 무효화해야 한다면 [revoke it](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- You are free to extend the models used internally by Passport by defining your own model and extending the corresponding Passport model: -->
Passport에서 내부적으로 사용하는 모델들을 자유롭게 확장할 수 있습니다. 직접 모델을 정의하고 해당 Passport 모델을 상속(extends)하면 됩니다.

```
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

<!-- After defining your model, you may instruct Passport to use your custom model via the `Laravel\Passport\Passport` class. Typically, you should inform Passport about your custom models in the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
모델을 정의한 후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport에 커스텀 모델을 알려야 합니다. 보통 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 지정하면 됩니다.

```
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\PersonalAccessClient;
use App\Models\Passport\Token;

/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::useTokenModel(Token::class);
    Passport::useClientModel(Client::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::usePersonalAccessClientModel(PersonalAccessClient::class);
}
```

<a name="issuing-access-tokens"></a>
<!-- ## Issuing Access Tokens -->
## Issuing Access Tokens

<!-- Using OAuth2 via authorization codes is how most developers are familiar with OAuth2. When using authorization codes, a client application will redirect a user to your server where they will either approve or deny the request to issue an access token to the client. -->
대부분의 개발자는 OAuth2를 사용할 때 권한 코드(authorization code)를 이용하는 방식에 익숙합니다. 이 방법을 사용하면, 클라이언트 애플리케이션이 사용자를 여러분의 서버로 리디렉션하고, 사용자는 해당 요청을 허용하거나 거부한 뒤 클라이언트에게 액세스 토큰을 발급할 수 있습니다.

<a name="managing-clients"></a>
<!-- ### Managing Clients -->
### Managing Clients

<!-- First, developers building applications that need to interact with your application's API will need to register their application with yours by creating a "client". Typically, this consists of providing the name of their application and a URL that your application can redirect to after users approve their request for authorization. -->
여러분의 API와 연동할 애플리케이션을 개발하는 개발자들은 우선 자신들의 애플리케이션을 여러분의 애플리케이션에 "클라이언트"로 등록해야 합니다. 보통 이때 앱 이름과 인증/인가 완료 후 리디렉션할 URL 정보를 입력받습니다.

<a name="the-passportclient-command"></a>
<!-- #### The `passport:client` Command -->
#### The `passport:client` Command

<!-- The simplest way to create a client is using the `passport:client` Artisan command. This command may be used to create your own clients for testing your OAuth2 functionality. When you run the `client` command, Passport will prompt you for more information about your client and will provide you with a client ID and secret: -->
가장 간단하게 클라이언트를 생성하는 방법은 `passport:client` 아티즌 명령어를 사용하는 것입니다. 이 명령어로 자체 테스트용 OAuth2 클라이언트를 쉽고 빠르게 만들 수 있습니다. `client` 명령어를 실행하면 Passport는 클라이언트에 대한 추가 정보를 입력받고, 클라이언트 ID 및 시크릿(비밀 키)을 알려줍니다.

```
php artisan passport:client
```

<!-- **Redirect URLs** -->
**리디렉션 URL**

<!-- If you would like to allow multiple redirect URLs for your client, you may specify them using a comma-delimited list when prompted for the URL by the `passport:client` command. Any URLs which contain commas should be URL encoded: -->
클라이언트에 여러 리디렉션 URL을 허용하려면, `passport:client` 명령어에서 URL 입력 시 쉼표(콤마)로 구분해 여러 개를 지정할 수 있습니다. 쉼표가 포함된 URL은 URL 인코딩해야 합니다.

```bash
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
<!-- #### JSON API -->
#### JSON API

<!-- Since your application's users will not be able to utilize the `client` command, Passport provides a JSON API that you may use to create clients. This saves you the trouble of having to manually code controllers for creating, updating, and deleting clients. -->
애플리케이션의 사용자들은 `client` 명령어를 직접 이용할 수 없으므로, Passport에서는 클라이언트 생성을 위한 JSON API도 제공합니다. 이를 활용하면 별도의 컨트롤러 코드를 구현하지 않아도 클라이언트 생성, 수정, 삭제 기능을 쉽게 만들 수 있습니다.

<!-- However, you will need to pair Passport's JSON API with your own frontend to provide a dashboard for your users to manage their clients. Below, we'll review all of the API endpoints for managing clients. For convenience, we'll use [Axios](https://github.com/axios/axios) to demonstrate making HTTP requests to the endpoints. -->
단, 이 JSON API와 여러분이 개발한 프론트엔드를 연동해, 사용자가 자신의 클라이언트를 관리할 수 있는 대시보드를 직접 구성해야 합니다. 아래는 각 클라이언트 관리 API 엔드포인트를 소개합니다. 참고로 HTTP 요청 예시는 [Axios](https://github.com/axios/axios)를 사용해 설명합니다.

<!-- The JSON API is guarded by the `web` and `auth` middleware; therefore, it may only be called from your own application. It is not able to be called from an external source. -->
이 JSON API는 `web` 및 `auth` 미들웨어로 보호되기 때문에, 반드시 자체 애플리케이션에서만 호출 가능하며 외부에서는 사용할 수 없습니다.

<a name="get-oauthclients"></a>
<!-- #### `GET /oauth/clients` -->
#### `GET /oauth/clients`

<!-- This route returns all of the clients for the authenticated user. This is primarily useful for listing all of the user's clients so that they may edit or delete them: -->
이 엔드포인트는 인증된 사용자의 모든 클라이언트 목록을 반환합니다. 주된 용도는, 사용자가 클라이언트 목록을 조회한 뒤, 수정 또는 삭제할 수 있도록 돕는 것입니다.

```
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
<!-- #### `POST /oauth/clients` -->
#### `POST /oauth/clients`

<!-- This route is used to create new clients. It requires two pieces of data: the client's `name` and a `redirect` URL. The `redirect` URL is where the user will be redirected after approving or denying a request for authorization. -->
이 엔드포인트는 신규 클라이언트 생성을 위한 것으로, 클라이언트의 `name`과 `redirect` URL 두 개의 데이터가 필요합니다. `redirect` URL은 사용자가 인증 요청을 허용/거부한 뒤 리디렉션될 위치입니다.

<!-- When a client is created, it will be issued a client ID and client secret. These values will be used when requesting access tokens from your application. The client creation route will return the new client instance: -->
클라이언트가 생성되면 클라이언트 ID와 시크릿이 발급됩니다. 이 값들은 이후 액세스 토큰을 요청할 때 사용됩니다. 경로 호출 시 새로운 클라이언트 인스턴스를 반환합니다.

```
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
이 엔드포인트는 클라이언트를 수정할 때 사용합니다. 클라이언트의 `name`과 `redirect` URL 두 가지 데이터가 필수입니다. `redirect` URL은 사용자가 인증 요청을 승인하거나 거부한 뒤 리디렉션될 주소입니다. 이 라우트는 갱신된 클라이언트 인스턴스를 반환합니다.

```
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
이 엔드포인트는 클라이언트 삭제에 사용됩니다.

```
axios.delete('/oauth/clients/' + clientId)
    .then(response => {
        //
    });
```

<a name="requesting-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="requesting-tokens-redirecting-for-authorization"></a>
<!-- #### Redirecting For Authorization -->
#### Redirecting For Authorization

<!-- Once a client has been created, developers may use their client ID and secret to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route like so: -->
클라이언트가 생성된 이후, 개발자는 자신의 클라이언트 ID와 시크릿을 이용해 여러분의 애플리케이션에서 권한 코드 및 액세스 토큰을 요청할 수 있습니다. 먼저, 외부 애플리케이션은 여러분의 애플리케이션의 `/oauth/authorize` 경로로 리디렉션 요청을 발생시켜야 합니다. 예시는 아래와 같습니다.

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
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

> [!TIP]
> `/oauth/authorize` 경로는 `Passport::routes` 메서드에 의해 이미 정의되어 있습니다. 해당 경로를 별도로 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
<!-- #### Approving The Request -->
#### Approving The Request

<!-- When receiving authorization requests, Passport will automatically display a template to the user allowing them to approve or deny the authorization request. If they approve the request, they will be redirected back to the `redirect_uri` that was specified by the consuming application. The `redirect_uri` must match the `redirect` URL that was specified when the client was created. -->
인증 요청을 수신하면 Passport가 자동으로 템플릿 화면을 렌더링하여 사용자가 인증 요청을 허용(Approve) 또는 거부(Deny)할 수 있게 해줍니다. 요청을 승인하면, 사용자는 소비 애플리케이션이 지정한 `redirect_uri`로 돌아가게 됩니다. 이 `redirect_uri`는 클라이언트 생성 시 지정한 `redirect` URL과 반드시 일치해야 합니다.

<!-- If you would like to customize the authorization approval screen, you may publish Passport's views using the `vendor:publish` Artisan command. The published views will be placed in the `resources/views/vendor/passport` directory: -->
인증 승인 화면을 커스터마이즈하고 싶다면 `vendor:publish` 아티즌 명령어로 Passport의 뷰 파일을 퍼블리시할 수 있습니다. 퍼블리시된 뷰들은 `resources/views/vendor/passport` 디렉토리에 위치하게 됩니다.

```
php artisan vendor:publish --tag=passport-views
```

<!-- Sometimes you may wish to skip the authorization prompt, such as when authorizing a first-party client. You may accomplish this by [extending the `Client` model](#overriding-default-models) and defining a `skipsAuthorization` method. If `skipsAuthorization` returns `true` the client will be approved and the user will be redirected back to the `redirect_uri` immediately: -->
실제 운영에서는, 실제로 신뢰할 만한 1st party 클라이언트를 인증할 경우, 이 승인 알림 단계를 건너뛰고 싶을 수 있습니다. 이럴 때는 [extending the `Client` model](#overriding-default-models)하고, `skipsAuthorization` 메서드를 정의할 수 있습니다. `skipsAuthorization`이 `true`를 반환하면, 클라이언트가 승인되고 사용자는 인증 프롬프트 없이 즉시 `redirect_uri`로 리디렉션됩니다.

```
<?php

namespace App\Models\Passport;

use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * Determine if the client should skip the authorization prompt.
     *
     * @return bool
     */
    public function skipsAuthorization()
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
<!-- #### Converting Authorization Codes To Access Tokens -->
#### Converting Authorization Codes To Access Tokens

<!-- If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should first verify the `state` parameter against the value that was stored prior to the redirect. If the state parameter matches then the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request: -->
사용자가 인증 요청을 승인하면, 사용자는 외부 애플리케이션으로 다시 리디렉션됩니다. 외부 애플리케이션에서는 우선 리디렉션 전에 저장해두었던 값과 `state` 파라미터를 비교하여 검증해야 합니다. state 파라미터가 일치하면, 외부 애플리케이션은 액세스 토큰을 요청하기 위해 애플리케이션에 `POST` 요청을 보내야 합니다. 이 요청에는 사용자가 인증 요청을 승인할 때 애플리케이션이 발급한 권한 코드(authorization code)가 포함되어야 합니다.

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
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
`/oauth/token` 경로는 `access_token`, `refresh_token`, `expires_in` 속성을 담은 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰 만료까지의 초(seconds)를 의미합니다.

> [!TIP]
> `/oauth/authorize` 경로와 마찬가지로, `/oauth/token` 경로도 `Passport::routes`에서 자동으로 정의되므로, 별도로 정의할 필요가 없습니다.

<a name="tokens-json-api"></a>
<!-- #### JSON API -->
#### JSON API

<!-- Passport also includes a JSON API for managing authorized access tokens. You may pair this with your own frontend to offer your users a dashboard for managing access tokens. For convenience, we'll use [Axios](https://github.com/mzabriskie/axios) to demonstrate making HTTP requests to the endpoints. The JSON API is guarded by the `web` and `auth` middleware; therefore, it may only be called from your own application. -->
Passport는 인증된 액세스 토큰 관리용 JSON API도 제공합니다. 여러분이 직접 개발하는 프론트엔드에서 이 API를 활용하면, 사용자가 본인의 액세스 토큰을 일괄 관리하는 대시보드를 구축할 수 있습니다. HTTP 요청 예시는 [Axios](https://github.com/mzabriskie/axios)를 활용합니다. 이 API 역시 `web` 및 `auth` 미들웨어로 보호되어, 애플리케이션 내부에서만 사용할 수 있습니다.

<a name="get-oauthtokens"></a>
<!-- #### `GET /oauth/tokens` -->
#### `GET /oauth/tokens`

<!-- This route returns all of the authorized access tokens that the authenticated user has created. This is primarily useful for listing all of the user's tokens so that they can revoke them: -->
이 엔드포인트는 인증된 사용자가 생성한 모든 액세스 토큰 목록을 반환합니다. 주로 사용자에게 자신의 토큰 목록을 보여주고, 필요시 개별적으로 취소(revoke)하도록 할 때 유용합니다.

```
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
<!-- #### `DELETE /oauth/tokens/{token-id}` -->
#### `DELETE /oauth/tokens/{token-id}`

<!-- This route may be used to revoke authorized access tokens and their related refresh tokens: -->
이 엔드포인트를 이용해, 인증된 액세스 토큰과 관련된 리프레시 토큰을 함께 취소할 수 있습니다.

```
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
<!-- ### Refreshing Tokens -->
### Refreshing Tokens

<!-- If your application issues short-lived access tokens, users will need to refresh their access tokens via the refresh token that was provided to them when the access token was issued: -->
애플리케이션에서 액세스 토큰을 짧은 수명으로 발급한다면, 사용자들은 토큰이 만료될 때 미리 발급받은 리프레시 토큰을 이용해 액세스 토큰을 갱신해야 할 수도 있습니다.

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
이때도 `/oauth/token` 엔드포인트는 `access_token`, `refresh_token`, `expires_in` 속성을 포함한 JSON 형태로 응답합니다. `expires_in`은 새로 발급받은 액세스 토큰 만료까지 남은 시간(초)입니다.

<a name="revoking-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- You may revoke a token by using the `revokeAccessToken` method on the `Laravel\Passport\TokenRepository`. You may revoke a token's refresh tokens using the `revokeRefreshTokensByAccessTokenId` method on the `Laravel\Passport\RefreshTokenRepository`. These classes may be resolved using Laravel's [service container](/docs/8.x/container): -->
`Laravel\Passport\TokenRepository` 클래스의 `revokeAccessToken` 메서드를 사용해 액세스 토큰을 취소할 수 있습니다. 액세스 토큰에 연결된 리프레시 토큰들은 `Laravel\Passport\RefreshTokenRepository`의 `revokeRefreshTokensByAccessTokenId` 메서드로 취소할 수 있습니다. 두 클래스 모두 Laravel의 [service container](/docs/8.x/container)를 통해 주입할 수 있습니다.

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
토큰이 폐기(revoke)되었거나 만료(expired)된 경우, 데이터베이스에서 해당 토큰을 정리하고 싶을 수 있습니다. Passport에서 제공하는 `passport:purge` 아티즌 명령어를 사용하면 이를 손쉽게 처리할 수 있습니다.

```
# Purge revoked and expired tokens and auth codes...
php artisan passport:purge

# Only purge revoked tokens and auth codes...
php artisan passport:purge --revoked

# Only purge expired tokens and auth codes...
php artisan passport:purge --expired
```

<!-- You may also configure a [scheduled job](/docs/8.x/scheduling) in your application's `App\Console\Kernel` class to automatically prune your tokens on a schedule: -->
또한, 애플리케이션의 `App\Console\Kernel` 클래스에서 [scheduled job](/docs/8.x/scheduling)을 설정하여 주기적으로 토큰을 자동 관리하도록 할 수 있습니다.

```
/**
 * Define the application's command schedule.
 *
 * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
 * @return void
 */
protected function schedule(Schedule $schedule)
{
    $schedule->command('passport:purge')->hourly();
}
```

<a name="code-grant-pkce"></a>
<!-- ## Authorization Code Grant with PKCE -->
## Authorization Code Grant with PKCE

<!-- The Authorization Code grant with "Proof Key for Code Exchange" (PKCE) is a secure way to authenticate single page applications or native applications to access your API. This grant should be used when you can't guarantee that the client secret will be stored confidentially or in order to mitigate the threat of having the authorization code intercepted by an attacker. A combination of a "code verifier" and a "code challenge" replaces the client secret when exchanging the authorization code for an access token. -->
"Proof Key for Code Exchange" (PKCE)를 사용하는 인증 코드 그랜트는 싱글 페이지 애플리케이션(SPA)이나 네이티브 애플리케이션이 API에 안전하게 인증할 수 있는 방법입니다. 클라이언트 시크릿을 안전하게 저장할 수 없거나, 인증 코드를 공격자가 가로채는 위험을 줄이고자 할 때 이 방법을 사용하는 것이 좋습니다. 이 방식에서는 클라이언트 시크릿 대신 "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)"의 조합으로 인증 코드와 액세스 토큰을 교환합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
<!-- ### Creating The Client -->
### Creating The Client

<!-- Before your application can issue tokens via the authorization code grant with PKCE, you will need to create a PKCE-enabled client. You may do this using the `passport:client` Artisan command with the `--public` option: -->
애플리케이션에서 PKCE를 사용하는 인증 코드 그랜트를 통해 토큰을 발급하려면, PKCE가 활성화된 클라이언트를 먼저 생성해야 합니다. 아래의 `passport:client` 아티즌 명령어에서 `--public` 옵션을 사용하여 생성할 수 있습니다.

```
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="code-verifier-code-challenge"></a>
<!-- #### Code Verifier & Code Challenge -->
#### Code Verifier & Code Challenge

<!-- As this authorization grant does not provide a client secret, developers will need to generate a combination of a code verifier and a code challenge in order to request a token. -->
이 인증 방식에서는 클라이언트 시크릿이 제공되지 않으므로, 토큰을 요청하려면 개발자가 코드 검증자(code verifier)와 코드 챌린지(code challenge)를 직접 생성해야 합니다.

<!-- The code verifier should be a random string of between 43 and 128 characters containing letters, numbers, and  `"-"`, `"."`, `"_"`, `"~"` characters, as defined in the [RFC 7636 specification](https://tools.ietf.org/html/rfc7636). -->
코드 검증자는 알파벳, 숫자, 그리고 `"-"`, `"."`, `"_"`, `"~"` 문자를 포함하여 43~128자 사이의 임의 문자열이어야 하며, 이는 [RFC 7636 specification](https://tools.ietf.org/html/rfc7636)에 따라야 합니다.

<!-- The code challenge should be a Base64 encoded string with URL and filename-safe characters. The trailing `'='` characters should be removed and no line breaks, whitespace, or other additional characters should be present. -->
코드 챌린지는 URL 및 파일명에 안전한 문자들로 이루어진 Base64 인코딩 문자열이어야 하며, 끝 부분의 `'='` 문자는 제거하고, 줄바꿈, 공백, 기타 불필요한 문자가 없어야 합니다.

```
$encoded = base64_encode(hash('sha256', $code_verifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
<!-- #### Redirecting For Authorization -->
#### Redirecting For Authorization

<!-- Once a client has been created, you may use the client ID and the generated code verifier and code challenge to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route: -->
클라이언트를 생성한 후에는 클라이언트 ID, 생성한 코드 검증자와 코드 챌린지를 사용하여 인증 코드와 액세스 토큰을 요청할 수 있습니다. 우선, 이용 애플리케이션에서 `/oauth/authorize` 라우트로 리디렉션 요청을 전송해야 합니다.

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
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
<!-- #### Converting Authorization Codes To Access Tokens -->
#### Converting Authorization Codes To Access Tokens

<!-- If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should verify the `state` parameter against the value that was stored prior to the redirect, as in the standard Authorization Code Grant. -->
사용자가 인증 요청을 승인하면, 사용자는 소비 애플리케이션으로 다시 리디렉션됩니다. 이때 표준 인증 코드 그랜트와 마찬가지로, 소비 애플리케이션에서는 이전에 저장한 `state` 값과 리디렉션된 값이 일치하는지 검증해야 합니다.

<!-- If the state parameter matches, the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request along with the originally generated code verifier: -->
state 파라미터가 일치한다면, 소비 애플리케이션에서는 액세스 토큰을 요청하는 `POST` 요청을 애플리케이션에 전송해야 합니다. 이 요청에는 사용자가 인증 요청을 승인할 때 발급 받은 인증 코드와, 처음에 생성한 코드 검증자(code verifier)를 포함해야 합니다.

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

> [!NOTE]
> 패스워드 그랜트 토큰(password grant tokens)은 더 이상 사용을 권장하지 않습니다. 대신, [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하시기 바랍니다.

<!-- The OAuth2 password grant allows your other first-party clients, such as a mobile application, to obtain an access token using an email address / username and password. This allows you to issue access tokens securely to your first-party clients without requiring your users to go through the entire OAuth2 authorization code redirect flow. -->
OAuth2 패스워드 그랜트는 다른 1st-party 클라이언트(예: 모바일 애플리케이션)에서 이메일 주소/사용자명과 비밀번호로 액세스 토큰을 발급받을 수 있게 해줍니다. 이를 통해, 모든 OAuth2 인증 코드 리디렉션 과정을 거치지 않고도 안전하게 토큰을 발급할 수 있습니다.

<a name="creating-a-password-grant-client"></a>
<!-- ### Creating A Password Grant Client -->
### Creating A Password Grant Client

<!-- Before your application can issue tokens via the password grant, you will need to create a password grant client. You may do this using the `passport:client` Artisan command with the `--password` option. **If you have already run the `passport:install` command, you do not need to run this command:** -->
패스워드 그랜트를 통해 토큰을 발급하려면 먼저 패스워드 그랜트 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어의 `--password` 옵션을 사용하여 생성할 수 있습니다. **이미 `passport:install`을 실행했다면, 이 명령어를 다시 실행할 필요가 없습니다.**

```
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<!-- Once you have created a password grant client, you may request an access token by issuing a `POST` request to the `/oauth/token` route with the user's email address and password. Remember, this route is already registered by the `Passport::routes` method so there is no need to define it manually. If the request is successful, you will receive an `access_token` and `refresh_token` in the JSON response from the server: -->
패스워드 그랜트 클라이언트를 생성했으면, 사용자의 이메일 주소와 비밀번호를 포함한 `POST` 요청을 `/oauth/token` 라우트로 전송하여 액세스 토큰을 발급받을 수 있습니다. 이 라우트는 이미 `Passport::routes` 메서드에 의해 등록되어 있으므로, 별도로 정의할 필요가 없습니다. 요청이 성공하면, 서버에서 `access_token`과 `refresh_token`이 담긴 JSON 응답을 받게 됩니다.

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

> [!TIP]
> 액세스 토큰은 기본적으로 긴 유효 기간을 가집니다. 필요하다면 [configure your maximum access token lifetime](#configuration)할 수 있습니다.

<a name="requesting-all-scopes"></a>
<!-- ### Requesting All Scopes -->
### Requesting All Scopes

<!-- When using the password grant or client credentials grant, you may wish to authorize the token for all of the scopes supported by your application. You can do this by requesting the `*` scope. If you request the `*` scope, the `can` method on the token instance will always return `true`. This scope may only be assigned to a token that is issued using the `password` or `client_credentials` grant: -->
패스워드 그랜트 또는 클라이언트 크리덴셜 그랜트(Client Credentials Grant)를 사용할 때, 애플리케이션에서 지원하는 모든 스코프(scope)에 대해 토큰을 발급받고 싶을 수 있습니다. 이를 위해 `*` 스코프를 요청하면 됩니다. `*` 스코프를 요청할 경우, 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 `password` 또는 `client_credentials` 그랜트 유형으로 발급된 토큰에만 부여할 수 있습니다.

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
<!-- ### Customizing The User Provider -->
### Customizing The User Provider

<!-- If your application uses more than one [authentication user provider](/docs/8.x/authentication#introduction), you may specify which user provider the password grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --password` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#via-middleware) to ensure that only users from the guard's specified provider are authorized. -->
애플리케이션에서 2개 이상의 [authentication user provider](/docs/8.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --password` 명령어로 클라이언트를 생성할 때 `--provider` 옵션을 통해 어떤 프로바이더를 사용할 것인지 지정할 수 있습니다. 지정한 프로바이더명은 애플리케이션의 `config/auth.php` 설정 파일에 정의된 유효한 프로바이더와 일치해야 합니다. 이후 [protect your route using middleware](#via-middleware)도 할 수 있습니다.

<a name="customizing-the-username-field"></a>
<!-- ### Customizing The Username Field -->
### Customizing The Username Field

<!-- When authenticating using the password grant, Passport will use the `email` attribute of your authenticatable model as the "username". However, you may customize this behavior by defining a `findForPassport` method on your model: -->
패스워드 그랜트로 인증할 때, Passport는 인증 가능한 모델의 `email` 속성을 "사용자명"으로 사용합니다. 다만, 이 동작을 변경하고 싶다면 모델에 `findForPassport` 메서드를 정의할 수 있습니다.

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
     *
     * @param  string  $username
     * @return \App\Models\User
     */
    public function findForPassport($username)
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
<!-- ### Customizing The Password Validation -->
### Customizing The Password Validation

<!-- When authenticating using the password grant, Passport will use the `password` attribute of your model to validate the given password. If your model does not have a `password` attribute or you wish to customize the password validation logic, you can define a `validateForPassportPasswordGrant` method on your model: -->
패스워드 그랜트 인증 시 Passport는 모델의 `password` 속성을 이용해 사용자 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나, 비밀번호 검증 로직을 직접 구현하고 싶다면, `validateForPassportPasswordGrant` 메서드를 모델에 정의할 수 있습니다.

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
     *
     * @param  string  $password
     * @return bool
     */
    public function validateForPassportPasswordGrant($password)
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant-tokens"></a>
<!-- ## Implicit Grant Tokens -->
## Implicit Grant Tokens

> [!NOTE]
> 임플리시트 그랜트 토큰(implicit grant tokens)은 더 이상 사용을 권장하지 않습니다. 대신, [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하시기 바랍니다.

<!-- The implicit grant is similar to the authorization code grant; however, the token is returned to the client without exchanging an authorization code. This grant is most commonly used for JavaScript or mobile applications where the client credentials can't be securely stored. To enable the grant, call the `enableImplicitGrant` method in the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
임플리시트 그랜트는 인증 코드 그랜트와 유사하지만, 인증 코드를 교환하는 절차 없이 바로 토큰이 클라이언트에 전달된다는 점이 다릅니다. 이 방식은 클라이언트 자격증명을 안전하게 저장할 수 없는 JavaScript 또는 모바일 애플리케이션에서 주로 사용됩니다. 임플리시트 그랜트를 활성화하려면, 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하세요.

```
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::enableImplicitGrant();
}
```

<!-- Once the grant has been enabled, developers may use their client ID to request an access token from your application. The consuming application should make a redirect request to your application's `/oauth/authorize` route like so: -->
임플리시트 그랜트가 활성화되면, 개발자는 해당 클라이언트 ID를 사용해 애플리케이션에서 액세스 토큰을 요청할 수 있습니다. 소비 애플리케이션은 아래 예시처럼 `/oauth/authorize` 라우트에 리디렉션 요청을 하면 됩니다.

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
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

> [!TIP]
> `/oauth/authorize` 라우트는 이미 `Passport::routes` 메서드에 의해 정의되어 있으므로, 별도로 라우트를 등록할 필요가 없습니다.

<a name="client-credentials-grant-tokens"></a>
<!-- ## Client Credentials Grant Tokens -->
## Client Credentials Grant Tokens

<!-- The client credentials grant is suitable for machine-to-machine authentication. For example, you might use this grant in a scheduled job which is performing maintenance tasks over an API. -->
클라이언트 크리덴셜 그랜트는 머신-투-머신(M2M) 인증에 적합합니다. 예를 들어, API를 통해 유지보수 작업을 수행하는 정기 작업(스케쥴 작업) 등에서 이 그랜트 방식을 사용할 수 있습니다.

<!-- Before your application can issue tokens via the client credentials grant, you will need to create a client credentials grant client. You may do this using the `--client` option of the `passport:client` Artisan command: -->
클라이언트 크리덴셜 그랜트를 통해 토큰을 발급하려면, 먼저 클라이언트 크리덴셜 그랜트 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어의 `--client` 옵션을 사용해 생성할 수 있습니다.

```
php artisan passport:client --client
```

<!-- Next, to use this grant type, you need to add the `CheckClientCredentials` middleware to the `$routeMiddleware` property of your `app/Http/Kernel.php` file: -->
이후, 이 그랜트 유형을 사용하려면 `app/Http/Kernel.php` 파일의 `$routeMiddleware` 속성에 `CheckClientCredentials` 미들웨어를 추가해야 합니다.

```
use Laravel\Passport\Http\Middleware\CheckClientCredentials;

protected $routeMiddleware = [
    'client' => CheckClientCredentials::class,
];
```

<!-- Then, attach the middleware to a route: -->
그 다음, 해당 미들웨어를 라우트에 적용하면 됩니다.

```
Route::get('/orders', function (Request $request) {
    ...
})->middleware('client');
```

<!-- To restrict access to the route to specific scopes, you may provide a comma-delimited list of the required scopes when attaching the `client` middleware to the route: -->
특정 스코프에 요청을 제한하려면, `client` 미들웨어를 라우트에 연결할 때 콤마로 구분된 스코프 목록을 전달하면 됩니다.

```
Route::get('/orders', function (Request $request) {
    ...
})->middleware('client:check-status,your-scope');
```

<a name="retrieving-tokens"></a>
<!-- ### Retrieving Tokens -->
### Retrieving Tokens

<!-- To retrieve a token using this grant type, make a request to the `oauth/token` endpoint: -->
이 그랜트 유형을 이용해 토큰을 발급받으려면, `oauth/token` 엔드포인트에 요청을 보내면 됩니다.

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
사용자가 일반적인 인증 코드 리디렉션 과정을 거치지 않고, 직접 자신의 액세스 토큰을 발급 받을 수 있도록 허용해야 할 때가 있습니다. 예를 들어, 사용자가 API를 실험하거나, 액세스 토큰을 보다 단순하게 발급받는 등 다양한 목적으로 이 기능을 제공할 수 있습니다.

> [!TIP]
> 애플리케이션에서 주로 개인 액세스 토큰 발급만 필요하다면, Passport 대신 [Laravel Sanctum](/docs/8.x/sanctum) 사용을 고려해보세요. Sanctum은 Laravel에서 직접 제공하는 경량의 API 토큰 발급 라이브러리입니다.

<a name="creating-a-personal-access-client"></a>
<!-- ### Creating A Personal Access Client -->
### Creating A Personal Access Client

<!-- Before your application can issue personal access tokens, you will need to create a personal access client. You may do this by executing the `passport:client` Artisan command with the `--personal` option. If you have already run the `passport:install` command, you do not need to run this command: -->
개인 액세스 토큰을 발급하려면 먼저 개인 액세스 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어의 `--personal` 옵션을 실행하여 생성할 수 있습니다. 이미 `passport:install`을 실행했다면, 별도 명령 실행이 필요 없습니다.

```
php artisan passport:client --personal
```

<!-- After creating your personal access client, place the client's ID and plain-text secret value in your application's `.env` file: -->
클라이언트 생성 후에는 클라이언트의 ID와 플레인텍스트 시크릿 값을 애플리케이션의 `.env` 파일에 저장해야 합니다.

```bash
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
<!-- ### Managing Personal Access Tokens -->
### Managing Personal Access Tokens

<!-- Once you have created a personal access client, you may issue tokens for a given user using the `createToken` method on the `App\Models\User` model instance. The `createToken` method accepts the name of the token as its first argument and an optional array of [scopes](#token-scopes) as its second argument: -->
개인 액세스 클라이언트를 생성했다면, 이제 `App\Models\User` 모델 인스턴스의 `createToken` 메서드를 통해 지정된 사용자에게 토큰을 발급할 수 있습니다. `createToken` 메서드는 첫 번째 인수로 토큰 이름, 두 번째 인수(옵션)로 [scopes](#token-scopes) 배열을 받습니다.

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
Passport는 개인 액세스 토큰 관리를 위한 JSON API도 내장하고 있습니다. 프론트엔드와 연동하여 사용자에게 토큰 대시보드를 직접 제공할 수 있습니다. 아래 예제에서는 HTTP 요청에 [Axios](https://github.com/mzabriskie/axios)를 사용합니다.

<!-- The JSON API is guarded by the `web` and `auth` middleware; therefore, it may only be called from your own application. It is not able to be called from an external source. -->
JSON API는 `web` 및 `auth` 미들웨어로 보호되어 있기 때문에 오직 애플리케이션 내부에서만 호출할 수 있습니다. 외부에서는 호출할 수 없습니다.

<a name="get-oauthscopes"></a>
<!-- #### `GET /oauth/scopes` -->
#### `GET /oauth/scopes`

<!-- This route returns all of the [scopes](#token-scopes) defined for your application. You may use this route to list the scopes a user may assign to a personal access token: -->
이 라우트는 애플리케이션에 정의된 [scopes](#token-scopes) 전부를 반환합니다. 사용자가 개인 액세스 토큰에 어떤 스코프를 부여할 수 있는지 목록을 가져올 때 유용합니다.

```
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
<!-- #### `GET /oauth/personal-access-tokens` -->
#### `GET /oauth/personal-access-tokens`

<!-- This route returns all of the personal access tokens that the authenticated user has created. This is primarily useful for listing all of the user's tokens so that they may edit or revoke them: -->
이 라우트는 인증된 사용자가 생성한 개인 액세스 토큰 전체를 반환합니다. 사용자가 자신의 토큰을 목록으로 확인하고, 편집하거나 폐기할 수 있도록 보여주기에 적합합니다.

```
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
<!-- #### `POST /oauth/personal-access-tokens` -->
#### `POST /oauth/personal-access-tokens`

<!-- This route creates new personal access tokens. It requires two pieces of data: the token's `name` and the `scopes` that should be assigned to the token: -->
이 라우트는 새로운 개인 액세스 토큰을 생성합니다. 요청 시 토큰의 `name`(이름)과 토큰에 부여할 `scopes`(스코프) 정보가 필요합니다.

```
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
이 라우트는 개인 액세스 토큰을 폐기(revoke)할 때 사용합니다.

```
axios.delete('/oauth/personal-access-tokens/' + tokenId);
```

<a name="protecting-routes"></a>
<!-- ## Protecting Routes -->
## Protecting Routes

<a name="via-middleware"></a>
<!-- ### Via Middleware -->
### Via Middleware

<!-- Passport includes an [authentication guard](/docs/8.x/authentication#adding-custom-guards) that will validate access tokens on incoming requests. Once you have configured the `api` guard to use the `passport` driver, you only need to specify the `auth:api` middleware on any routes that should require a valid access token: -->
Passport는 [authentication guard](/docs/8.x/authentication#adding-custom-guards)를 제공하여 들어오는 요청의 액세스 토큰을 검증할 수 있습니다. `api` 가드에서 `passport` 드라이버를 사용하도록 구성했다면, 유효한 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어만 지정해주면 됩니다.

```
Route::get('/user', function () {
    //
})->middleware('auth:api');
```

> [!NOTE]
> [client credentials grant](#client-credentials-grant-tokens)를 사용하는 경우에는, 라우트 보호에 `auth:api` 미들웨어 대신 [the `client` middleware](#client-credentials-grant-tokens)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
<!-- #### Multiple Authentication Guards -->
#### Multiple Authentication Guards

<!-- If your application authenticates different types of users that perhaps use entirely different Eloquent models, you will likely need to define a guard configuration for each user provider type in your application. This allows you to protect requests intended for specific user providers. For example, given the following guard configuration the `config/auth.php` configuration file: -->
애플리케이션에서 서로 다른 Eloquent 모델을 사용하는 여러 종류의 사용자를 인증해야 할 경우, 각 사용자 프로바이더에 맞는 가드 설정을 추가해야 할 수 있습니다. 이를 통해 특정 사용자 프로바이더에만 요청을 제한하고 보호할 수 있습니다. 예를 들어, 다음은 `config/auth.php`의 가드 설정 예시입니다.

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
다음과 같은 라우트는 `customers` 사용자 프로바이더를 사용하는 `api-customers` 가드를 활용하여 요청을 인증하게 됩니다.

```
Route::get('/customer', function () {
    //
})->middleware('auth:api-customers');
```

> [!TIP]
> Passport에서 여러 사용자 프로바이더를 사용하는 상세 방법은 [password grant documentation](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
<!-- ### Passing The Access Token -->
### Passing The Access Token

<!-- When calling routes that are protected by Passport, your application's API consumers should specify their access token as a `Bearer` token in the `Authorization` header of their request. For example, when using the Guzzle HTTP library: -->
Passport로 보호된 라우트에 접근할 때, API 소비자는 요청의 `Authorization` 헤더에 액세스 토큰을 `Bearer` 토큰 형태로 명시해야 합니다. 예를 들어, Guzzle HTTP 라이브러리를 사용하는 경우는 다음과 같습니다.

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
스코프(scope)를 통해 API 클라이언트가 계정 접근을 요청할 때, 허용하려는 권한 범위를 제한할 수 있습니다. 예를 들어, 전자상거래 애플리케이션을 만든다면, 모든 API 소비자가 주문을 할 필요는 없을 것입니다. 대신, 주문의 배송 상태만 접근하도록 권한 요청을 제한할 수 있습니다. 즉, 스코프를 활용하면 제3자 애플리케이션이 사용자를 대신해 수행할 수 있는 작업을 제한할 수 있습니다.

<a name="defining-scopes"></a>
<!-- ### Defining Scopes -->
### Defining Scopes

<!-- You may define your API's scopes using the `Passport::tokensCan` method in the `boot` method of your application's `App\Providers\AuthServiceProvider` class. The `tokensCan` method accepts an array of scope names and scope descriptions. The scope description may be anything you wish and will be displayed to users on the authorization approval screen: -->
`App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 API의 스코프를 등록할 수 있습니다. `tokensCan`은 스코프명과 해당 스코프의 설명이 담긴 배열을 인수로 받습니다. 이 설명은 인증 승인 화면에서 사용자에게 표시됩니다.

```
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

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
특정 스코프를 지정하지 않은 경우, Passport 서버에서 토큰에 기본적으로 부여할 스코프를 `setDefaultScope` 메서드를 통해 설정할 수 있습니다. 일반적으로 이 메서드는 `App\Providers\AuthServiceProvider`의 `boot` 메서드에서 호출합니다.

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

<a name="assigning-scopes-to-tokens"></a>

<!-- ### Assigning Scopes To Tokens -->
### Assigning Scopes To Tokens

<a name="when-requesting-authorization-codes"></a>
<!-- #### When Requesting Authorization Codes -->
#### When Requesting Authorization Codes

<!-- When requesting an access token using the authorization code grant, consumers should specify their desired scopes as the `scope` query string parameter. The `scope` parameter should be a space-delimited list of scopes: -->
인가 코드 그랜트 방식을 통해 액세스 토큰을 요청할 때, 클라이언트는 원하는 범위를 `scope` 쿼리 문자열 파라미터로 지정해야 합니다. `scope` 파라미터에는 공백 문자로 구분된 범위 목록을 전달합니다:

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
`App\Models\User` 모델의 `createToken` 메서드를 사용해 퍼스널 액세스 토큰을 발급하는 경우, 원하는 범위 배열을 두 번째 인수로 메서드에 전달할 수 있습니다:

```
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="checking-scopes"></a>
<!-- ### Checking Scopes -->
### Checking Scopes

<!-- Passport includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given scope. To get started, add the following middleware to the `$routeMiddleware` property of your `app/Http/Kernel.php` file: -->
Passport에는 들어오는 요청이 특정 범위가 부여된 토큰으로 인증되었는지 확인할 수 있는 두 가지 미들웨어가 있습니다. 먼저, 아래 미들웨어들을 `app/Http/Kernel.php` 파일의 `$routeMiddleware` 속성에 추가하세요:

```
'scopes' => \Laravel\Passport\Http\Middleware\CheckScopes::class,
'scope' => \Laravel\Passport\Http\Middleware\CheckForAnyScope::class,
```

<a name="check-for-all-scopes"></a>
<!-- #### Check For All Scopes -->
#### Check For All Scopes

<!-- The `scopes` middleware may be assigned to a route to verify that the incoming request's access token has all of the listed scopes: -->
`scopes` 미들웨어를 라우트에 할당하면, 해당 요청의 액세스 토큰이 나열된 모든 범위를 가지고 있는지 확인합니다:

```
Route::get('/orders', function () {
    // Access token has both "check-status" and "place-orders" scopes...
})->middleware(['auth:api', 'scopes:check-status,place-orders']);
```

<a name="check-for-any-scopes"></a>
<!-- #### Check For Any Scopes -->
#### Check For Any Scopes

<!-- The `scope` middleware may be assigned to a route to verify that the incoming request's access token has *at least one* of the listed scopes: -->
`scope` 미들웨어를 사용하면, 요청의 액세스 토큰에 나열된 범위 중 하나라도 있으면 인증을 허용합니다:

```
Route::get('/orders', function () {
    // Access token has either "check-status" or "place-orders" scope...
})->middleware(['auth:api', 'scope:check-status,place-orders']);
```

<a name="checking-scopes-on-a-token-instance"></a>
<!-- #### Checking Scopes On A Token Instance -->
#### Checking Scopes On A Token Instance

<!-- Once an access token authenticated request has entered your application, you may still check if the token has a given scope using the `tokenCan` method on the authenticated `App\Models\User` instance: -->
액세스 토큰으로 인증된 요청이 애플리케이션에 진입한 후에도, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 사용해 해당 토큰에 특정 범위가 있는지 확인할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('place-orders')) {
        //
    }
});
```

<a name="additional-scope-methods"></a>
<!-- #### Additional Scope Methods -->
#### Additional Scope Methods

<!-- The `scopeIds` method will return an array of all defined IDs / names: -->
`scopeIds` 메서드를 사용하면, 정의된 모든 ID/이름이 배열로 반환됩니다:

```
use Laravel\Passport\Passport;

Passport::scopeIds();
```

<!-- The `scopes` method will return an array of all defined scopes as instances of `Laravel\Passport\Scope`: -->
`scopes` 메서드는 정의된 모든 범위가 `Laravel\Passport\Scope` 인스턴스 배열로 반환됩니다:

```
Passport::scopes();
```

<!-- The `scopesFor` method will return an array of `Laravel\Passport\Scope` instances matching the given IDs / names: -->
`scopesFor` 메서드는 전달한 ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```
Passport::scopesFor(['place-orders', 'check-status']);
```

<!-- You may determine if a given scope has been defined using the `hasScope` method: -->
특정 범위가 정의되어 있는지 확인하려면 `hasScope` 메서드를 사용할 수 있습니다:

```
Passport::hasScope('place-orders');
```

<a name="consuming-your-api-with-javascript"></a>
<!-- ## Consuming Your API With JavaScript -->
## Consuming Your API With JavaScript

<!-- When building an API, it can be extremely useful to be able to consume your own API from your JavaScript application. This approach to API development allows your own application to consume the same API that you are sharing with the world. The same API may be consumed by your web application, mobile applications, third-party applications, and any SDKs that you may publish on various package managers. -->
API를 개발할 때, JavaScript 애플리케이션에서 직접 자신이 만든 API를 호출할 수 있으면 매우 유용합니다. 이 방법은 내 애플리케이션이 외부에 공개하는 API를 그대로 내부에서도 사용할 수 있도록 해줍니다. 동일한 API를 웹 애플리케이션, 모바일 애플리케이션, 서드파티 애플리케이션, 그리고 패키지 매니저에 배포하는 각종 SDK 등에서 모두 사용할 수 있습니다.

<!-- Typically, if you want to consume your API from your JavaScript application, you would need to manually send an access token to the application and pass it with each request to your application. However, Passport includes a middleware that can handle this for you. All you need to do is add the `CreateFreshApiToken` middleware to your `web` middleware group in your `app/Http/Kernel.php` file: -->
일반적으로 JavaScript 애플리케이션에서 여러분의 API를 호출하려면 액세스 토큰을 직접 전달하고, 이 토큰을 요청마다 함께 전송해야 합니다. 하지만 Passport는 이러한 과정을 자동으로 처리해주는 미들웨어를 제공합니다. 여러분은 `app/Http/Kernel.php` 파일의 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어만 추가하면 됩니다:

```
'web' => [
    // Other middleware...
    \Laravel\Passport\Http\Middleware\CreateFreshApiToken::class,
],
```

> [!NOTE]
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택에서 반드시 가장 마지막에 위치해야 합니다.

<!-- This middleware will attach a `laravel_token` cookie to your outgoing responses. This cookie contains an encrypted JWT that Passport will use to authenticate API requests from your JavaScript application. The JWT has a lifetime equal to your `session.lifetime` configuration value. Now, since the browser will automatically send the cookie with all subsequent requests, you may make requests to your application's API without explicitly passing an access token: -->
이 미들웨어는 응답에 `laravel_token` 쿠키를 추가합니다. 이 쿠키는 Passport가 JavaScript 애플리케이션으로부터 들어오는 API 요청을 인증할 때 사용하는 암호화된 JWT를 담고 있습니다. 이 JWT의 유효기간은 `session.lifetime` 설정값과 동일하게 적용됩니다. 이제 브라우저가 모든 후속 요청에 쿠키를 자동으로 보내므로, 여러분은 액세스 토큰을 직접 전달하지 않고도 API 요청을 보낼 수 있습니다:

```
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
<!-- #### Customizing The Cookie Name -->
#### Customizing The Cookie Name

<!-- If needed, you can customize the `laravel_token` cookie's name using the `Passport::cookie` method. Typically, this method should be called from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
필요하다면, `Passport::cookie` 메서드를 사용해 `laravel_token` 쿠키의 이름을 변경할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- When using this method of authentication, you will need to ensure a valid CSRF token header is included in your requests. The default Laravel JavaScript scaffolding includes an Axios instance, which will automatically use the encrypted `XSRF-TOKEN` cookie value to send an `X-XSRF-TOKEN` header on same-origin requests. -->
이 인증 방식을 쓸 때는 요청에 올바른 CSRF 토큰 헤더가 반드시 포함되어야 합니다. Laravel 기본 JavaScript 스캐폴딩에는 Axios 인스턴스가 내장되어 있으며, 이 인스턴스는 암호화된 `XSRF-TOKEN` 쿠키 값을 이용해 동일 출처 요청에 자동으로 `X-XSRF-TOKEN` 헤더를 전송합니다.

> [!TIP]
> 만약 `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 보내고 싶다면, `csrf_token()`에서 반환된 암호화되지 않은 토큰을 사용해야 합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Passport raises events when issuing access tokens and refresh tokens. You may use these events to prune or revoke other access tokens in your database. If you would like, you may attach listeners to these events in your application's `App\Providers\EventServiceProvider` class: -->
Passport는 액세스 토큰 및 리프레시 토큰이 발급될 때 이벤트를 발생시킵니다. 이러한 이벤트를 활용해 필요하면 데이터베이스 내의 다른 액세스 토큰을 정리하거나 폐기할 수 있습니다. 원한다면, 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에서 이벤트에 리스너를 연결할 수 있습니다:

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
Passport의 `actingAs` 메서드는 현재 인증된 사용자와 부여된 범위도 함께 지정할 수 있습니다. `actingAs` 메서드의 첫 번째 인자는 사용자 인스턴스이고, 두 번째 인자는 사용자 토큰에 부여할 범위 배열입니다:

```
use App\Models\User;
use Laravel\Passport\Passport;

public function test_servers_can_be_created()
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
Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트와 부여된 범위를 함께 지정할 수 있습니다. `actingAsClient` 메서드의 첫 번째 인자는 클라이언트 인스턴스이고, 두 번째 인자는 클라이언트 토큰에 부여할 범위 배열입니다:

```
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_orders_can_be_retrieved()
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['check-status']
    );

    $response = $this->get('/api/orders');

    $response->assertStatus(200);
}
```
