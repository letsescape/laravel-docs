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
Laravel 프레임워크의 모든 구성 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션에는 문서가 제공되어 있으니 파일을 자세히 살펴보고 사용할 수 있는 옵션에 익숙해지시기 바랍니다.

<!-- These configuration files allow you to configure things like your database connection information, your mail server information, as well as various other core configuration values such as your application URL and encryption key. -->
이러한 구성 파일을 통해 데이터베이스 연결 정보, 메일 서버 정보, 그리고 애플리케이션 URL 및 암호화 키 등과 같은 다양한 핵심 구성 값을 설정할 수 있습니다.

<a name="the-about-command"></a>
<!-- #### The `about` Command -->
#### The `about` Command

<!-- Laravel can display an overview of your application's configuration, drivers, and environment via the `about` Artisan command. -->
Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경에 대한 개요를 표시할 수 있습니다.

```shell
php artisan about
```

<!-- If you're only interested in a particular section of the application overview output, you may filter for that section using the `--only` option: -->
애플리케이션 개요 출력에서 특정 섹션만 보고 싶다면, `--only` 옵션을 사용해 해당 섹션만 필터링할 수 있습니다.

```shell
php artisan about --only=environment
```

<!-- Or, to explore a specific configuration file's values in detail, you may use the `config:show` Artisan command: -->
또는 특정 구성 파일의 값을 자세히 확인하고 싶다면, `config:show` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
<!-- ## Environment Configuration -->
## Environment Configuration

<!-- It is often helpful to have different configuration values based on the environment where the application is running. For example, you may wish to use a different cache driver locally than you do on your production server. -->
애플리케이션이 실행되는 환경에 따라 서로 다른 구성 값을 사용하는 것이 흔히 도움이 됩니다. 예를 들어, 로컬 환경과 운영 서버에서는 서로 다른 캐시 드라이버를 사용할 수 있습니다.

<!-- To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file that defines many common environment variables. During the Laravel installation process, this file will automatically be copied to `.env`. -->
이를 간편하게 관리할 수 있도록, Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 새로 설치된 Laravel에는 애플리케이션 루트 디렉토리에 `.env.example` 파일이 포함되어 있으며, 여기에는 여러 일반적인 환경 변수가 정의되어 있습니다. Laravel 설치 과정에서 이 파일이 자동으로 `.env` 파일로 복사됩니다.

<!-- Laravel's default `.env` file contains some common configuration values that may differ based on whether your application is running locally or on a production web server. These values are then read by the configuration files within the `config` directory using Laravel's `env` function. -->
Laravel의 기본 `.env` 파일에는 로컬 환경과 운영 웹 서버에서 서로 다를 수 있는 몇 가지 기본 구성 값이 담겨 있습니다. 이러한 값은 `config` 디렉토리의 구성 파일에서 Laravel의 `env` 함수를 통해 읽게 됩니다.

<!-- If you are developing with a team, you may wish to continue including and updating the `.env.example` file with your application. By putting placeholder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application. -->
팀으로 개발할 경우, `.env.example` 파일을 계속 포함하고 업데이트하는 것이 좋습니다. 예시 파일에 플레이스홀더 값을 입력하면, 팀의 다른 개발자들도 애플리케이션 실행에 필요한 환경 변수를 명확히 확인할 수 있습니다.

> [!NOTE]
> `.env` 파일의 어떤 변수든 서버 수준이나 시스템 수준의 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
<!-- #### Environment File Security -->
#### Environment File Security

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
각 개발자/서버마다 사용해야 하는 환경 구성이 다를 수 있으므로, `.env` 파일은 소스 제어에 커밋하지 않아야 합니다. 또한 만약 공격자가 소스 제어 저장소에 접근한다면 중요한 인증 정보가 노출될 수 있어 보안상 위험합니다.

<!-- However, it is possible to encrypt your environment file using Laravel's built-in [environment encryption](#encrypting-environment-files). Encrypted environment files may be placed in source control safely. -->
하지만 Laravel의 내장 [environment encryption](#encrypting-environment-files) 기능을 이용하면 환경 파일을 암호화할 수 있습니다. 암호화된 환경 파일은 소스 제어에 안전하게 포함할 수 있습니다.

<a name="additional-environment-files"></a>
<!-- #### Additional Environment Files -->
#### Additional Environment Files

<!-- Before loading your application's environment variables, Laravel determines if an `APP_ENV` environment variable has been externally provided or if the `--env` CLI argument has been specified. If so, Laravel will attempt to load an `.env.[APP_ENV]` file if it exists. If it does not exist, the default `.env` file will be loaded. -->
애플리케이션의 환경 변수를 로딩하기 전에, Laravel은 외부에서 `APP_ENV` 환경 변수가 제공되었는지 혹은 `--env` CLI 인수가 지정되었는지 확인합니다. 만약 그렇다면, Laravel은 `.env.[APP_ENV]` 파일이 존재하는지 확인한 뒤, 존재하면 해당 파일을 로드합니다. 만약 없다면 기본 `.env` 파일이 로드됩니다.

<a name="environment-variable-types"></a>
<!-- ### Environment Variable Types -->
### Environment Variable Types

<!-- All variables in your `.env` files are typically parsed as strings, so some reserved values have been created to allow you to return a wider range of types from the `env()` function: -->
`.env` 파일의 모든 변수는 일반적으로 문자열로 파싱되지만, `env()` 함수에서 좀 더 다양한 타입을 반환할 수 있도록 예약된 값들이 마련되어 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| `.env` 값    | `env()` 반환값   |
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
값에 공백이 포함된 환경 변수를 정의하려면 값을 큰따옴표로 감싸면 됩니다.

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
<!-- ### Retrieving Environment Configuration -->
### Retrieving Environment Configuration

<!-- All of the variables listed in the `.env` file will be loaded into the `$_ENV` PHP super-global when your application receives a request. However, you may use the `env` function to retrieve values from these variables in your configuration files. In fact, if you review the Laravel configuration files, you will notice many of the options are already using this function: -->
`.env` 파일에 명시된 모든 변수는 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 그러나 구성 파일에서는 `env` 함수를 사용해 이러한 변수의 값을 가져올 수 있습니다. 실제로 Laravel의 구성 파일을 살펴보면, 여러 옵션에서 이미 이 함수를 사용하는 모습을 확인할 수 있습니다.

```php
'debug' => (bool) env('APP_DEBUG', false),
```

<!-- The second value passed to the `env` function is the "default value". This value will be returned if no environment variable exists for the given key. -->
`env` 함수에 두 번째로 전달하는 값은 "기본값"입니다. 해당 키에 대한 환경 변수가 없을 때 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
<!-- ### Determining the Current Environment -->
### Determining the Current Environment

<!-- The current application environment is determined via the `APP_ENV` variable from your `.env` file. You may access this value via the `environment` method on the `App` [facade](/docs/master/facades): -->
현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [facade](/docs/master/facades)의 `environment` 메서드를 통해 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

<!-- You may also pass arguments to the `environment` method to determine if the environment matches a given value. The method will return `true` if the environment matches any of the given values: -->
또한, `environment` 메서드에 인수를 전달하여 환경이 특정 값과 일치하는지 확인할 수도 있습니다. 환경이 전달한 값 중 하나와 일치하면 `true`를 반환합니다.

```php
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}
```

> [!NOTE]
> 현재 애플리케이션 환경 결정은 서버 수준의 `APP_ENV` 환경 변수를 정의하여 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
<!-- ### Encrypting Environment Files -->
### Encrypting Environment Files

<!-- Unencrypted environment files should never be stored in source control. However, Laravel allows you to encrypt your environment files so that they may safely be added to source control with the rest of your application. -->
암호화되지 않은 환경 파일을 소스 제어에 저장해서는 안 됩니다. 하지만 Laravel은 환경 파일을 암호화할 수 있게 하여, 애플리케이션을 소스 제어에 포함할 때 안전하게 다룰 수 있도록 해줍니다.

<a name="encryption"></a>
<!-- #### Encryption -->
#### Encryption

<!-- To encrypt an environment file, you may use the `env:encrypt` command: -->
환경 파일을 암호화하려면, `env:encrypt` 명령어를 사용할 수 있습니다.

```shell
php artisan env:encrypt
```

<!-- Running the `env:encrypt` command will encrypt your `.env` file and place the encrypted contents in an `.env.encrypted` file. The decryption key is presented in the output of the command and should be stored in a secure password manager. If you would like to provide your own encryption key you may use the `--key` option when invoking the command: -->
`env:encrypt` 명령어를 실행하면 `.env` 파일이 암호화되어, 암호화된 내용이 `.env.encrypted` 파일로 저장됩니다. 복호화 키는 명령어 실행 결과에 제공되며, 반드시 안전한 비밀번호 관리 도구에 저장해야 합니다. 직접 암호화 키를 지정하려면, 명령어 실행 시 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 제공하는 키의 길이는 사용되는 암호화 알고리즘의 키 길이와 일치해야 합니다. 기본적으로 Laravel은 32자 키가 필요한 `AES-256-CBC` 알고리즘을 사용합니다. 명령어 실행 시 `--cipher` 옵션을 넘기면 Laravel의 [encrypter](/docs/master/encryption)가 지원하는 다른 알고리즘도 사용할 수 있습니다.

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be encrypted by providing the environment name via the `--env` option: -->
`.env`, `.env.staging` 등 여러 환경 파일이 있을 경우, `--env` 옵션에 환경명을 지정하여 암호화할 파일을 선택할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="readable-variable-names"></a>
<!-- #### Readable Variable Names -->
#### Readable Variable Names

<!-- When encrypting your environment file, you may use the `--readable` option to retain visible variable names while encrypting their values: -->
환경 파일 암호화 시, `--readable` 옵션을 사용하면 변수명은 그대로 보이고 값만 암호화됩니다.

```shell
php artisan env:encrypt --readable
```

<!-- This will produce an encrypted file with the following format: -->
그러면 아래와 같이 변수명은 노출되고 값만 암호화된 파일이 생성됩니다.

```ini
APP_NAME=eyJpdiI6...
APP_ENV=eyJpdiI6...
APP_KEY=eyJpdiI6...
APP_DEBUG=eyJpdiI6...
APP_URL=eyJpdiI6...
```

<!-- Using the readable format allows you to see which environment variables exist without exposing sensitive data. It also makes reviewing pull requests much easier since you can see which variables were added, removed, or renamed without needing to decrypt the file. -->
가독성 있는 형식을 사용하면 예민한 데이터는 보호하면서도, 어떤 환경 변수가 있는지 쉽게 파악할 수 있습니다. 덕분에 pull request를 리뷰할 때도 어떤 변수가 추가, 삭제, 수정되었는지 암호를 해제할 필요 없이 확인할 수 있습니다.

<!-- When decrypting environment files, Laravel automatically detects which format was used, so no additional options are needed for the `env:decrypt` command. -->
환경 파일을 복호화할 때는 Laravel이 사용된 형식을 자동으로 감지하므로, `env:decrypt` 명령어에 추가 옵션이 필요하지 않습니다.

> [!NOTE]
> `--readable` 옵션을 사용할 경우, 원본 환경 파일의 주석 및 빈 줄은 암호화된 파일에 포함되지 않습니다.

<a name="decryption"></a>
<!-- #### Decryption -->
#### Decryption

<!-- To decrypt an environment file, you may use the `env:decrypt` command. This command requires a decryption key, which Laravel will retrieve from the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable: -->
환경 파일을 복호화하려면, `env:decrypt` 명령어를 사용할 수 있습니다. 이 명령어는 복호화 키가 필요하며, Laravel은 이를 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 읽어옵니다.

```shell
php artisan env:decrypt
```

<!-- Or, the key may be provided directly to the command via the `--key` option: -->
또는, `--key` 옵션을 통해 직접 키를 전달할 수도 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

<!-- When the `env:decrypt` command is invoked, Laravel will decrypt the contents of the `.env.encrypted` file and place the decrypted contents in the `.env` file. -->
`env:decrypt` 명령어를 실행하면, `.env.encrypted` 파일의 내용을 복호화하여 `.env` 파일에 저장합니다.

<!-- The `--cipher` option may be provided to the `env:decrypt` command in order to use a custom encryption cipher: -->
커스텀 암호화 알고리즘을 사용하려면, `env:decrypt` 명령어에서 `--cipher` 옵션을 사용할 수 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be decrypted by providing the environment name via the `--env` option: -->
`.env`, `.env.staging` 등 여러 환경 파일이 있을 경우, `--env` 옵션에 환경명을 지정하여 복호화할 파일을 선택할 수 있습니다.

```shell
php artisan env:decrypt --env=staging
```

<!-- In order to overwrite an existing environment file, you may provide the `--force` option to the `env:decrypt` command: -->
기존 환경 파일을 덮어쓰려면, `env:decrypt` 명령어에 `--force` 옵션을 추가합니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
<!-- ## Accessing Configuration Values -->
## Accessing Configuration Values

<!-- You may easily access your configuration values using the `Config` facade or global `config` function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist: -->
애플리케이션 어디서든 `Config` 파사드 또는 전역 `config` 함수를 사용하여 구성 값에 쉽게 접근할 수 있습니다. 접근 시 파일명과 옵션명을 포함하는 "도트(dot)" 문법으로 사용할 수 있으며, 옵션이 없을 경우 반환할 기본값을 지정할 수도 있습니다.

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');
```

<!-- To set configuration values at runtime, you may invoke the `Config` facade's `set` method or pass an array to the `config` function: -->
실행 중에 구성 값을 설정하려면, `Config` 파사드의 `set` 메서드를 호출하거나 `config` 함수에 배열을 전달하면 됩니다.

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

<!-- To assist with static analysis, the `Config` facade also provides typed configuration retrieval methods. If the retrieved configuration value does not match the expected type, an exception will be thrown: -->
정적 분석(static analysis)를 지원하기 위해, `Config` 파사드는 타입별 구성 값 조회 메서드도 제공합니다. 반환된 값이 기대하는 타입이 아닐 경우 예외가 발생합니다.

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
Config::collection('config-key');
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework. -->
애플리케이션의 속도를 높이기 위해, 모든 구성 파일을 하나의 파일로 캐싱할 수 있습니다. 이를 위해 `config:cache` Artisan 명령어를 사용합니다. 이 명령어는 애플리케이션의 모든 구성 옵션을 하나의 파일로 병합하여, 프레임워크가 더욱 빠르게 로드할 수 있도록 해줍니다.

<!-- You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development. -->
`php artisan config:cache` 명령어는 보통 운영 환경 배포 과정의 일부로 실행해야 하며, 로컬 개발 도중에는 빈번한 구성 변경이 필요하므로 실행하지 않는 것이 좋습니다.

<!-- Once the configuration has been cached, your application's `.env` file will not be loaded by the framework during requests or Artisan commands; therefore, the `env` function will only return external, system level environment variables. -->
구성이 캐싱되면, 애플리케이션의 `.env` 파일은 요청이나 Artisan 명령 실행 시 프레임워크에 의해 로드되지 않습니다. 따라서 `env` 함수는 외부 시스템 환경 변수만 반환하게 됩니다.

<!-- For this reason, you should ensure you are only calling the `env` function from within your application's configuration (`config`) files. You can see many examples of this by examining Laravel's default configuration files. Configuration values may be accessed from anywhere in your application using the `config` function [described above](#accessing-configuration-values). -->
이런 이유로, `env` 함수는 반드시 애플리케이션의 구성(`config`) 파일 안에서만 호출해야 합니다. 자세한 내용은 위의 [described above](#accessing-configuration-values) 섹션을 참고하세요. 구성 값은 애플리케이션 어디서든 `config` 함수를 통해 접근하면 됩니다.

<!-- The `config:clear` command may be used to purge the cached configuration: -->
캐싱된 구성을 삭제하려면 `config:clear` 명령어를 사용합니다.

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행할 경우, 반드시 `env` 함수를 구성 파일 안에서만 호출하는지 확인해야 합니다. 구성이 캐싱되면 `.env` 파일이 로드되지 않으므로, `env` 함수는 오직 외부 시스템 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
<!-- ## Configuration Publishing -->
## Configuration Publishing

<!-- Most of Laravel's configuration files are already published in your application's `config` directory; however, certain configuration files like `cors.php` and `view.php` are not published by default, as most applications will never need to modify them. -->
대부분의 Laravel 구성 파일은 이미 애플리케이션의 `config` 디렉토리에 퍼블리시되어 있습니다. 하지만, `cors.php`, `view.php` 같은 일부 파일은 대부분의 애플리케이션에서 수정할 필요가 없으므로 기본적으로는 퍼블리시되지 않습니다.

<!-- However, you may use the `config:publish` Artisan command to publish any configuration files that are not published by default: -->
그럼에도 불구하고, 필요하다면 `config:publish` Artisan 명령어를 사용해 기본적으로 퍼블리시되지 않은 모든 구성 파일을 퍼블리시할 수 있습니다.

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 구성 파일의 `debug` 옵션은 실제로 사용자에게 에러 정보가 얼마나 표시되는지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 이 값을 반드시 `false`로 설정하세요. 운영 환경에서 `true`로 설정하면, 민감한 구성 값이 애플리케이션 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
<!-- ## Maintenance Mode -->
## Maintenance Mode

<!-- When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503. -->
애플리케이션이 유지보수 모드일 때, 모든 요청에 대해 커스텀 화면이 표시됩니다. 이를 통해 업데이트나 유지보수를 진행하는 동안 애플리케이션을 손쉽게 "비활성화"할 수 있습니다. 유지보수 모드 확인은 애플리케이션의 기본 미들웨어 스택에 포함되어 있으며, 유지보수 상태일 때는 `Symfony\Component\HttpKernel\Exception\HttpException`(상태 코드 503)이 발생합니다.

<!-- To enable maintenance mode, execute the `down` Artisan command: -->
유지보수 모드를 활성화하려면 `down` Artisan 명령어를 실행합니다.

```shell
php artisan down
```

<!-- If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds: -->
모든 유지보수 표시 응답에 `Refresh` HTTP 헤더를 전송하려면, `down` 명령어를 실행할 때 `refresh` 옵션을 사용할 수 있습니다. `Refresh` 헤더는 브라우저가 지정한 초 후에 페이지를 자동으로 새로고침하도록 안내합니다.

```shell
php artisan down --refresh=15
```

<!-- You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header: -->
또한, `down` 명령어에 `retry` 옵션을 추가하면 HTTP 응답의 `Retry-After` 헤더로 해당 값을 전송할 수 있습니다(대부분의 브라우저에서는 이 헤더를 무시합니다).

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
<!-- #### Bypassing Maintenance Mode -->
#### Bypassing Maintenance Mode

<!-- To allow maintenance mode to be bypassed using a secret token, you may use the `secret` option to specify a maintenance mode bypass token: -->
유지보수 모드를 비밀 토큰으로 우회하도록 하려면, `secret` 옵션을 사용해 우회 토큰을 지정할 수 있습니다.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
유지보수 모드 상태에서 위 토큰에 해당하는 애플리케이션 URL로 접근하면, Laravel이 유지보수 모드 우회 쿠키를 브라우저에 발급합니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

<!-- If you would like Laravel to generate the secret token for you, you may use the `with-secret` option. The secret will be displayed to you once the application is in maintenance mode: -->
Laravel이 비밀 토큰을 자동 생성하도록 하려면, `with-secret` 옵션을 사용하면 됩니다. 생성된 비밀 토큰은 애플리케이션이 유지보수 모드에 진입한 이후에 표시됩니다.

```shell
php artisan down --with-secret
```

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
이 숨겨진 경로로 접속하면 `/` 경로로 리디렉션되어, 쿠키가 발급된 후에는 유지보수 모드가 아닌 것처럼 애플리케이션을 정상적으로 이용할 수 있습니다.

> [!NOTE]
> 유지보수 모드 비밀 토큰 값은 일반적으로 영문, 숫자, 그리고 선택적으로 대시(-)로 구성해야 하며, `?`, `&`처럼 URL에서 특별한 의미를 갖는 문자는 피해야 합니다.

<a name="maintenance-mode-on-multiple-servers"></a>
<!-- #### Maintenance Mode on Multiple Servers -->
#### Maintenance Mode on Multiple Servers

<!-- By default, Laravel determines if your application is in maintenance mode using a file-based system. This means to activate maintenance mode, the `php artisan down` command has to be executed on each server hosting your application. -->
Laravel은 기본적으로 파일 기반 방식으로 유지보수 모드 진입 여부를 판단합니다. 즉, 애플리케이션이 여러 서버에 배포되어 있다면 각 서버에서 `php artisan down` 명령을 각각 실행해야 유지보수 모드가 적용됩니다.

<!-- Alternatively, Laravel offers a cache-based method for handling maintenance mode. This method requires running the `php artisan down` command on just one server. To use this approach, modify the maintenance mode variables in your application's `.env` file. You should select a cache `store` that is accessible by all of your servers. This ensures the maintenance mode status is consistently maintained across every server: -->
대신 Laravel은 캐시 기반 유지보수 모드 방식도 제공합니다. 이 방법을 사용하면 한 서버에서만 `php artisan down` 명령을 실행해도 전체 서버에 유지보수 상태가 공유됩니다. 이를 위해서는 `.env` 파일의 유지보수 모드 관련 변수를 아래처럼 설정하고, 모든 서버에서 접근 가능한 캐시 `store`를 지정해야 합니다.

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering the Maintenance Mode View -->
#### Pre-Rendering the Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
배포 과정에서 `php artisan down` 명령을 활용하는 경우, Composer 의존성이나 기타 인프라 요소가 업데이트되는 동안에도 사용자가 접속한다면 종종 에러가 발생할 수 있습니다. 이는 Laravel 프레임워크의 많은 부분이 부팅되어야만 유지보수 모드 여부를 판별하고, 템플릿 엔진을 통해 유지보수 화면을 렌더링할 수 있기 때문입니다.

<!-- For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
이 문제를 해결하기 위해, Laravel은 요청 사이클의 맨 초기에 반환될 미리 렌더링된 유지보수 뷰를 제작할 수 있습니다. 이 뷰는 애플리케이션의 어떤 의존성도 로드되기 전에 표시됩니다. 원하는 템플릿을 미리 렌더링하려면 `down` 명령어의 `render` 옵션을 사용하면 됩니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
<!-- #### Redirecting Maintenance Mode Requests -->
#### Redirecting Maintenance Mode Requests

<!-- While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI: -->
유지보수 모드에서 Laravel은 사용자가 접근하는 모든 URL에 대해 유지보수 뷰를 표시합니다. 원한다면 모든 요청을 특정 URL로 리디렉션하도록 설정할 수도 있습니다. 이는 `redirect` 옵션으로 처리할 수 있습니다. 예를 들어, 모든 요청을 `/` URI로 리디렉션하고 싶을 수 있습니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
<!-- #### Disabling Maintenance Mode -->
#### Disabling Maintenance Mode

<!-- To disable maintenance mode, use the `up` command: -->
유지보수 모드를 비활성화하려면 `up` 명령어를 사용합니다.

```shell
php artisan up
```

> [!NOTE]
> 기본 유지보수 모드 템플릿은 `resources/views/errors/503.blade.php`에 직접 정의하여 사용자 지정할 수 있습니다.

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode and Queues -->
#### Maintenance Mode and Queues

<!-- While your application is in maintenance mode, no [queued jobs](/docs/master/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
애플리케이션이 유지보수 모드일 때는 [queued jobs](/docs/master/queues)이 수행되지 않습니다. 유지보수 모드를 해제하면 큐 작업은 다시 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
<!-- #### Alternatives to Maintenance Mode -->
#### Alternatives to Maintenance Mode

<!-- Since maintenance mode requires your application to have several seconds of downtime, consider running your applications on a fully-managed platform like [Laravel Cloud](https://cloud.laravel.com) to accomplish zero-downtime deployment with Laravel. -->
유지보수 모드는 필연적으로 몇 초간 애플리케이션의 다운타임이 발생합니다. 다운타임 없는(Zero-downtime) 배포가 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 플랫폼에서 애플리케이션을 실행하는 것을 고려해 볼 수 있습니다.