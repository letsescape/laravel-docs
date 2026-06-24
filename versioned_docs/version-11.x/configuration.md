<!-- # Configuration -->
# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
    - [Environment Variable Types](#environment-variable-types)
    - [Retrieving Environment Configuration](#retrieving-environment-configuration)
    - [Determining the Current Environment](#determining-the-current-environment)
    - [Encrypting Environment Files](#encrypting-environment-files)
- [Accessing Configuration Values](#accessing-configuration-values)
- [Configuration Caching](#configuration-caching)
- [Configuration Publishing](#configuration-publishing)
- [Debug Mode](#debug-mode)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 설명이 달려 있으므로, 파일을 살펴보며 사용할 수 있는 다양한 옵션을 익혀 보시길 권장합니다.

<!-- These configuration files allow you to configure things like your database connection information, your mail server information, as well as various other core configuration values such as your application URL and encryption key. -->
이러한 설정 파일을 통해 데이터베이스 연결 정보, 메일 서버 정보, 애플리케이션 URL, 암호화 키 등 애플리케이션의 핵심 설정값을 자유롭게 관리할 수 있습니다.

<a name="the-about-command"></a>
<!-- #### The `about` Command -->
#### The `about` Command

<!-- Laravel can display an overview of your application's configuration, drivers, and environment via the `about` Artisan command. -->
Laravel에서는 `about` 아티즌 명령어를 통해 애플리케이션의 설정, 드라이버, 환경 전반에 대한 정보를 한눈에 확인할 수 있습니다.

```shell
php artisan about
```

<!-- If you're only interested in a particular section of the application overview output, you may filter for that section using the `--only` option: -->
특정 섹션만 보고 싶을 때는 `--only` 옵션을 사용해 해당 부분만 출력할 수 있습니다.

```shell
php artisan about --only=environment
```

<!-- Or, to explore a specific configuration file's values in detail, you may use the `config:show` Artisan command: -->
또는, 특정 설정 파일의 구체적인 값을 확인하고 싶다면 `config:show` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
<!-- ## Environment Configuration -->
## Environment Configuration

<!-- It is often helpful to have different configuration values based on the environment where the application is running. For example, you may wish to use a different cache driver locally than you do on your production server. -->
애플리케이션이 실행되는 환경에 따라 각기 다른 설정값을 사용하는 것이 좋을 때가 많습니다. 예를 들어, 로컬 환경에서는 프로덕션 서버와 다른 캐시 드라이버를 사용하고 싶을 수 있습니다.

<!-- To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file that defines many common environment variables. During the Laravel installation process, this file will automatically be copied to `.env`. -->
Laravel은 이러한 환경별 설정을 아주 쉽게 다룰 수 있도록 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 새롭게 설치된 Laravel 프로젝트의 루트 디렉터리에는 `.env.example` 파일이 있는데, 여기에는 일반적으로 많이 쓰이는 환경 변수들이 정의되어 있습니다. Laravel 설치 시점에 이 파일이 자동으로 `.env`로 복사됩니다.

<!-- Laravel's default `.env` file contains some common configuration values that may differ based on whether your application is running locally or on a production web server. These values are then read by the configuration files within the `config` directory using Laravel's `env` function. -->
Laravel의 기본 `.env` 파일에는 로컬 환경과 운영(프로덕션) 웹 서버에서 각각 다르게 적용될 수 있는 여러 공통 설정값이 담겨 있습니다. 이 값들은 Laravel의 `env` 함수를 통해 `config` 디렉터리의 설정 파일에서 읽어올 수 있습니다.

<!-- If you are developing with a team, you may wish to continue including and updating the `.env.example` file with your application. By putting placeholder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application. -->
여러 명이 함께 개발하는 경우, `.env.example` 파일을 애플리케이션과 함께 계속 포함하고 업데이트하는 것이 좋습니다. 예시 설정 파일에 플레이스홀더 값을 미리 채워두면, 팀원들은 애플리케이션 실행에 필요한 환경 변수 목록을 한눈에 파악할 수 있습니다.

> [!NOTE]
> `.env` 파일에 정의된 어떤 변수라도 서버나 시스템 등 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
<!-- #### Environment File Security -->
#### Environment File Security

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
`.env` 파일은 각 개발자/서버가 서로 다른 환경 구성을 요구할 수 있기 때문에, 소스 코드 저장소에 커밋하지 않아야 합니다. 만약 누군가가 소스 저장소에 무단으로 접근하게 되면 중요한 자격 증명이 유출될 수 있으므로, 보안상 매우 위험합니다.

<!-- However, it is possible to encrypt your environment file using Laravel's built-in [environment encryption](#encrypting-environment-files). Encrypted environment files may be placed in source control safely. -->
하지만, Laravel의 내장 [environment encryption](#encrypting-environment-files) 기능을 사용하면 환경 파일을 암호화하여 소스 저장소에 안전하게 포함할 수 있습니다.

<a name="additional-environment-files"></a>
<!-- #### Additional Environment Files -->
#### Additional Environment Files

<!-- Before loading your application's environment variables, Laravel determines if an `APP_ENV` environment variable has been externally provided or if the `--env` CLI argument has been specified. If so, Laravel will attempt to load an `.env.[APP_ENV]` file if it exists. If it does not exist, the default `.env` file will be loaded. -->
애플리케이션의 환경 변수를 불러오기 전에, Laravel은 외부에서 `APP_ENV` 환경 변수가 제공되었는지 또는 CLI의 `--env` 인자가 지정되었는지 먼저 확인합니다. 둘 중 하나라도 설정되어 있다면, 해당 이름을 가진 `.env.[APP_ENV]` 파일이 존재할 경우 이를 먼저 불러옵니다. 만약 없다면 기본 `.env` 파일이 로드됩니다.

<a name="environment-variable-types"></a>
<!-- ### Environment Variable Types -->
### Environment Variable Types

<!-- All variables in your `.env` files are typically parsed as strings, so some reserved values have been created to allow you to return a wider range of types from the `env()` function: -->
`.env` 파일의 변수들은 기본적으로 문자열로 파싱되지만, `env()` 함수에서 다양한 자료형을 다룰 수 있도록 예약된 값들이 제공됩니다:

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| `.env` 값    | `env()` 반환값    |
| ------------ | --------------- |
| true         | (bool) true     |
| (true)       | (bool) true     |
| false        | (bool) false    |
| (false)      | (bool) false    |
| empty        | (string) ''     |
| (empty)      | (string) ''     |
| null         | (null) null     |
| (null)       | (null) null     |

<!-- </div> -->
</div>

<!-- If you need to define an environment variable with a value that contains spaces, you may do so by enclosing the value in double quotes: -->
값에 공백이 포함되어야 한다면, 큰따옴표로 감싸서 정의할 수 있습니다.

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
<!-- ### Retrieving Environment Configuration -->
### Retrieving Environment Configuration

<!-- All of the variables listed in the `.env` file will be loaded into the `$_ENV` PHP super-global when your application receives a request. However, you may use the `env` function to retrieve values from these variables in your configuration files. In fact, if you review the Laravel configuration files, you will notice many of the options are already using this function: -->
`.env` 파일에 기재된 모든 변수는 애플리케이션이 요청을 받을 때 PHP의 `$_ENV` 슈퍼글로벌에 로드됩니다. 하지만 설정 파일에서 값을 참조할 때는 `env` 함수를 사용하는 것이 일반적입니다. 실제로 Laravel 공식 설정 파일들을 보면, 많은 옵션이 이미 이 함수를 사용하고 있음을 알 수 있습니다.

```
'debug' => env('APP_DEBUG', false),
```

<!-- The second value passed to the `env` function is the "default value". This value will be returned if no environment variable exists for the given key. -->
`env` 함수에 두 번째 인자를 전달하면, 해당 키에 대응하는 환경 변수가 없을 때 기본값으로 사용됩니다.

<a name="determining-the-current-environment"></a>
<!-- ### Determining the Current Environment -->
### Determining the Current Environment

<!-- The current application environment is determined via the `APP_ENV` variable from your `.env` file. You may access this value via the `environment` method on the `App` [facade](/docs/11.x/facades): -->
애플리케이션의 현재 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [facade](/docs/11.x/facades)의 `environment` 메서드를 통해 확인할 수 있습니다.

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

<!-- You may also pass arguments to the `environment` method to determine if the environment matches a given value. The method will return `true` if the environment matches any of the given values: -->
`environment` 메서드에 인자를 전달하면, 환경이 해당 값과 일치하는지 확인할 수도 있습니다. 일치하면 `true`를 반환합니다.

```
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}
```

> [!NOTE]
> 서버 수준의 `APP_ENV` 환경 변수를 통해 애플리케이션의 현재 환경 감지를 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
<!-- ### Encrypting Environment Files -->
### Encrypting Environment Files

<!-- Unencrypted environment files should never be stored in source control. However, Laravel allows you to encrypt your environment files so that they may safely be added to source control with the rest of your application. -->
암호화되지 않은 환경 파일은 절대로 소스 저장소에 포함해서는 안 됩니다. 그러나 Laravel에서는 환경 파일을 안전하게 암호화하여 애플리케이션과 함께 소스 저장소에 저장할 수 있도록 해줍니다.

<a name="encryption"></a>
<!-- #### Encryption -->
#### Encryption

<!-- To encrypt an environment file, you may use the `env:encrypt` command: -->
환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용합니다.

```shell
php artisan env:encrypt
```

<!-- Running the `env:encrypt` command will encrypt your `.env` file and place the encrypted contents in an `.env.encrypted` file. The decryption key is presented in the output of the command and should be stored in a secure password manager. If you would like to provide your own encryption key you may use the `--key` option when invoking the command: -->
`env:encrypt` 명령을 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일에 저장됩니다. 암호화에 사용된 키는 명령어 실행 후 출력 결과로 제공되며, 안전한 비밀번호 관리 프로그램에 별도로 저장해야 합니다. 직접 사용할 암호화 키를 명시하려면 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 지정하는 키의 길이는 사용 중인 암호화 알고리즘이 요구하는 길이와 일치해야 합니다. 기본적으로 Laravel은 `AES-256-CBC` 암호화를 사용하며, 32자 키가 필요합니다. `--cipher` 옵션을 사용하면 Laravel의 [encrypter](/docs/11.x/encryption)에서 지원하는 아무 암호화 방식이나 선택할 수 있습니다.

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be encrypted by providing the environment name via the `--env` option: -->
여러 환경 파일(예: `.env`, `.env.staging`)을 사용하는 경우, `--env` 옵션으로 암호화할 환경 이름을 지정할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
<!-- #### Decryption -->
#### Decryption

<!-- To decrypt an environment file, you may use the `env:decrypt` command. This command requires a decryption key, which Laravel will retrieve from the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable: -->
환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령은 복호화 키가 필요하며, Laravel은 이를 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 읽어옵니다.

```shell
php artisan env:decrypt
```

<!-- Or, the key may be provided directly to the command via the `--key` option: -->
또는 `--key` 옵션으로 키를 직접 전달할 수도 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

<!-- When the `env:decrypt` command is invoked, Laravel will decrypt the contents of the `.env.encrypted` file and place the decrypted contents in the `.env` file. -->
`env:decrypt` 명령을 실행하면 `.env.encrypted` 파일의 내용을 복호화하여 `.env` 파일로 저장합니다.

<!-- The `--cipher` option may be provided to the `env:decrypt` command in order to use a custom encryption cipher: -->
복호화 시 암호화 알고리즘을 직접 지정하고 싶다면 `env:decrypt` 명령어에 `--cipher` 옵션을 사용할 수 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be decrypted by providing the environment name via the `--env` option: -->
여러 환경 파일(예: `.env`, `.env.staging`)을 사용하는 경우, `--env` 옵션으로 복호화할 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:decrypt --env=staging
```

<!-- In order to overwrite an existing environment file, you may provide the `--force` option to the `env:decrypt` command: -->
기존 환경 파일을 덮어쓰려면 `env:decrypt` 명령어에 `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
<!-- ## Accessing Configuration Values -->
## Accessing Configuration Values

<!-- You may easily access your configuration values using the `Config` facade or global `config` function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist: -->
애플리케이션 어디서나 `Config` 파사드나 전역 `config` 함수를 통해 손쉽게 설정값에 접근할 수 있습니다. 파일명과 옵션명을 포함하는 "dot" 문법을 사용하며, 존재하지 않는 옵션에 대한 기본값도 지정할 수 있습니다.

```
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');
```

<!-- To set configuration values at runtime, you may invoke the `Config` facade's `set` method or pass an array to the `config` function: -->
런타임 중에 설정값을 변경해야 할 경우, `Config` 파사드의 `set` 메서드나 `config` 함수에 배열을 전달하면 값을 설정할 수 있습니다.

```
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

<!-- To assist with static analysis, the `Config` facade also provides typed configuration retrieval methods. If the retrieved configuration value does not match the expected type, an exception will be thrown: -->
정적 분석을 지원하기 위해, `Config` 파사드는 타입별 설정값 조회 메서드도 제공합니다. 실제 값이 기대한 타입이 아닐 경우 예외가 발생합니다.

```
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework. -->
애플리케이션의 성능을 높이기 위해, 모든 설정 파일을 하나로 묶어 캐싱할 수 있습니다. 이를 위해 `config:cache` 아티즌 명령어를 사용합니다. 설정값이 단일 파일로 통합되어 프레임워크가 빠르게 로딩할 수 있습니다.

<!-- You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development. -->
일반적으로 프로덕션 배포 과정의 일부로 `php artisan config:cache` 명령을 실행해야 합니다. 하지만 로컬 개발 중에는 자주 설정이 바뀌므로, 이 명령을 실행하지 않는 것이 좋습니다.

<!-- Once the configuration has been cached, your application's `.env` file will not be loaded by the framework during requests or Artisan commands; therefore, the `env` function will only return external, system level environment variables. -->
설정이 캐시되면, 애플리케이션의 `.env` 파일은 프레임워크가 요청이나 아티즌 명령을 처리할 때 더 이상 로드하지 않습니다. 그 결과, `env` 함수는 오직 시스템(외부) 수준 환경 변수만 반환합니다.

<!-- For this reason, you should ensure you are only calling the `env` function from within your application's configuration (`config`) files. You can see many examples of this by examining Laravel's default configuration files. Configuration values may be accessed from anywhere in your application using the `config` function [described above](#accessing-configuration-values). -->
따라서, 반드시 `env` 함수는 오직 애플리케이션의 `config`(설정) 파일 내부에서만 호출해야 합니다. 이 원칙은 Laravel 기본 설정 파일의 예시를 참조하면 쉽게 이해할 수 있습니다. 애플리케이션 내 어디에서든 [described above](#accessing-configuration-values) `config` 함수를 통해 설정값을 사용할 수 있습니다.

<!-- The `config:clear` command may be used to purge the cached configuration: -->
캐시된 설정을 삭제하려면 `config:clear` 명령어를 사용합니다.

```shell
php artisan config:clear
```

> [!WARNING]
> 배포(Deployment) 과정에서 `config:cache` 명령어를 사용하는 경우, 반드시 `env` 함수가 오직 설정 파일 내부에서만 호출되도록 해야 합니다. 일단 캐시가 생성되면 `.env` 파일이 로드되지 않으므로, `env` 함수는 외부 시스템 환경 변수만 반환하게 됩니다.

<a name="configuration-publishing"></a>
<!-- ## Configuration Publishing -->
## Configuration Publishing

<!-- Most of Laravel's configuration files are already published in your application's `config` directory; however, certain configuration files like `cors.php` and `view.php` are not published by default, as most applications will never need to modify them. -->
Laravel의 대부분 설정 파일은 기본적으로 애플리케이션의 `config` 디렉터리에 배포(발행)되어 있습니다. 하지만, `cors.php`, `view.php`와 같은 일부 설정 파일은 거의 수정할 일이 없으므로, 처음에는 디렉터리에 포함되어 있지 않습니다.

<!-- However, you may use the `config:publish` Artisan command to publish any configuration files that are not published by default: -->
필요하다면, `config:publish` 아티즌 명령어를 사용해 이들 설정 파일도 발행할 수 있습니다.

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 설정 파일에 있는 `debug` 옵션은 실제로 에러에 관한 정보를 사용자에게 얼마나 상세히 노출할지 결정합니다. 이 옵션은 기본적으로 `.env` 파일 안의 `APP_DEBUG` 환경 변수 값을 따르도록 구성되어 있습니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 하지만, 프로덕션 환경에서는 반드시 `false`여야 합니다. 만약 프로덕션에서 `true`로 설정한다면, 중요한 설정값이 사용자의 눈에 노출되는 심각한 위험이 발생할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- ## Maintenance Mode -->
## Maintenance Mode

<!-- When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503. -->
애플리케이션이 점검(유지보수) 모드에 들어가면, 모든 요청에 대해 사용자 정의 화면이 표시됩니다. 이 기능을 통해 업데이트나 유지보수 작업 동안 쉽게 애플리케이션 접근을 "잠글" 수 있습니다. 점검 모드 체크는 기본 미들웨어 스택에 포함되어 있으며, 이 상태에서 요청이 오면 `Symfony\Component\HttpKernel\Exception\HttpException` 예외(503 상태 코드)가 발생합니다.

<!-- To enable maintenance mode, execute the `down` Artisan command: -->
점검 모드를 활성화하려면 `down` 아티즌 명령어를 실행합니다.

```shell
php artisan down
```

<!-- If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds: -->
점검 모드에서 모든 응답에 `Refresh` HTTP 헤더를 추가하고 싶다면, `down` 명령어를 실행할 때 `refresh` 옵션을 사용하세요. `Refresh` 헤더는 브라우저가 지정한 시간(초) 후 자동으로 페이지를 새로 고치도록 안내합니다.

```shell
php artisan down --refresh=15
```

<!-- You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header: -->
`down` 명령어에 `retry` 옵션도 제공되며, 이는 `Retry-After` HTTP 헤더의 값으로 설정됩니다. 하지만 대부분의 브라우저는 이 헤더를 별도로 처리하지 않습니다.

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
<!-- #### Bypassing Maintenance Mode -->
#### Bypassing Maintenance Mode

<!-- To allow maintenance mode to be bypassed using a secret token, you may use the `secret` option to specify a maintenance mode bypass token: -->
비밀 토큰을 사용해 점검 모드를 우회하도록 하려면, `secret` 옵션에 우회용 토큰 값을 지정할 수 있습니다.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
이후 해당 토큰이 포함된 애플리케이션 URL에 접속하면, Laravel이 브라우저에 점검 모드 우회 쿠키를 발급합니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

<!-- If you would like Laravel to generate the secret token for you, you may use the `with-secret` option. The secret will be displayed to you once the application is in maintenance mode: -->
Laravel이 자동으로 비밀 토큰을 생성하도록 하려면, `with-secret` 옵션을 사용할 수 있습니다. 점검 모드 진입 시 생성된 토큰이 표시됩니다.

```shell
php artisan down --with-secret
```

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
이 숨겨진 경로로 접근하면, 애플리케이션의 `/` 경로로 자동 리디렉션됩니다. 브라우저에 쿠키가 발급된 후에는 점검 모드가 아니었던 것처럼 자유롭게 사이트를 이용할 수 있습니다.

> [!NOTE]
> 점검 모드 비밀 토큰에는 일반적으로 영숫자(alphanumeric) 문자와 필요하다면 하이픈(-)을 사용하세요. URL에서 특수 의미를 가지는 문자(`?`, `&` 등)는 사용을 피해야 합니다.

<a name="maintenance-mode-on-multiple-servers"></a>
<!-- #### Maintenance Mode on Multiple Servers -->
#### Maintenance Mode on Multiple Servers

<!-- By default, Laravel determines if your application is in maintenance mode using a file-based system. This means to activate maintenance mode, the `php artisan down` command has to be executed on each server hosting your application. -->
기본적으로 Laravel은 파일 기반 시스템을 통해 점검 모드를 판단합니다. 즉, 점검 모드를 활성화하려면 애플리케이션을 호스팅하는 모든 서버에서 각각 `php artisan down` 명령을 실행해야 합니다.

<!-- Alternatively, Laravel offers a cache-based method for handling maintenance mode. This method requires running the `php artisan down` command on just one server. To use this approach, modify the maintenance mode variables in your application's `.env` file. You should select a cache `store` that is accessible by all of your servers. This ensures the maintenance mode status is consistently maintained across every server: -->
대안으로, 캐시를 활용한 방식도 제공됩니다. 이 방법은 하나의 서버에서만 `php artisan down` 명령을 실행하면 됩니다. 이를 사용하려면 애플리케이션의 `.env` 파일에 아래와 같이 점검 모드 관련 변수를 수정하세요. 모든 서버가 접근할 수 있는 캐시 `store`를 지정해야 하며, 이를 통해 모든 서버에서 점검 모드 상태가 일관되게 유지됩니다.

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering the Maintenance Mode View -->
#### Pre-Rendering the Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
배포 중 `php artisan down` 명령어를 사용하는 경우, Composer 의존성 설치나 관련 인프라가 업데이트되는 동안 사용자가 접속하면 에러 페이지가 나타날 수 있습니다. 이는 점검 모드 판단 및 화면 렌더링에 Laravel의 많은 컴포넌트가 초기화되어야 하기 때문입니다.

<!-- For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
이런 문제를 막기 위해 Laravel은 점검 모드 초기 단계에서 반환될 미리 렌더링된 화면을 준비할 수 있게 해줍니다. 이 화면은 애플리케이션의 의존성 로드 이전에 가장 먼저 출력됩니다. `down` 명령어의 `render` 옵션을 활용해 원하는 템플릿을 미리 렌더링할 수 있습니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
<!-- #### Redirecting Maintenance Mode Requests -->
#### Redirecting Maintenance Mode Requests

<!-- While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI: -->
점검 모드에서 사용자가 어떤 URL로 접근해도 기본 점검 화면이 표시됩니다. 만약 모든 요청을 특정 URL로 리디렉션하고 싶다면, `redirect` 옵션을 사용할 수 있습니다. 예를 들어, 모든 요청을 `/` 경로로 보내려면 아래와 같이 명령을 실행합니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
<!-- #### Disabling Maintenance Mode -->
#### Disabling Maintenance Mode

<!-- To disable maintenance mode, use the `up` command: -->
점검(유지보수) 모드를 종료하려면 `up` 명령어를 사용하세요.

```shell
php artisan up
```

> [!NOTE]
> 기본 점검(유지보수) 모드 템플릿은 `resources/views/errors/503.blade.php` 경로에 직접 정의해 커스터마이징할 수 있습니다.

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode and Queues -->
#### Maintenance Mode and Queues

<!-- While your application is in maintenance mode, no [queued jobs](/docs/11.x/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
애플리케이션이 점검 모드일 때는 [queued jobs](/docs/11.x/queues)이 실행되지 않습니다. 점검 모드가 해제되면 평소처럼 작업 처리가 재개됩니다.

<a name="alternatives-to-maintenance-mode"></a>
<!-- #### Alternatives to Maintenance Mode -->
#### Alternatives to Maintenance Mode

<!-- Since maintenance mode requires your application to have several seconds of downtime, consider alternatives like [Laravel Vapor](https://vapor.laravel.com) and [Envoyer](https://envoyer.io) to accomplish zero-downtime deployment with Laravel. -->
점검 모드 사용 시 수 초간의 다운타임이 불가피합니다. 완전 무중단 배포를 원한다면, [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io)와 같은 솔루션을 고려해보시기 바랍니다.
