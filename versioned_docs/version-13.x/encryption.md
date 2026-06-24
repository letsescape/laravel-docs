<!-- # Encryption -->
# Encryption

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Gracefully Rotating Encryption Keys](#gracefully-rotating-encryption-keys)
- [Using the Encrypter](#using-the-encrypter)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's encryption services provide a simple, convenient interface for encrypting and decrypting text via OpenSSL using AES-256 and AES-128 encryption. All of Laravel's encrypted values are signed using a message authentication code (MAC) so that their underlying value cannot be modified or tampered with once encrypted. -->
Laravel의 암호화 서비스는 OpenSSL을 통해 AES-256 및 AES-128 암호화를 사용하여 텍스트를 암호화하고 복호화할 수 있는 간단하고 편리한 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값은 메시지 인증 코드(MAC)로 서명되므로, 암호화된 후에는 내부 값이 수정되거나 변조될 수 없습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Laravel's encrypter, you must set the `key` configuration option in your `config/app.php` configuration file. This configuration value is driven by the `APP_KEY` environment variable. You should use the `php artisan key:generate` command to generate this variable's value since the `key:generate` command will use PHP's secure random bytes generator to build a cryptographically secure key for your application. Typically, the value of the `APP_KEY` environment variable will be generated for you during [Laravel's installation](/docs/13.x/installation). -->
Laravel의 encrypter를 사용하기 전에 `config/app.php` 설정 파일에서 `key` 설정 옵션을 반드시 지정해야 합니다. 이 설정 값은 `APP_KEY` 환경 변수를 통해 관리됩니다. `php artisan key:generate` 명령어로 이 값을 생성하는 것이 좋습니다. `key:generate` 명령어는 PHP의 보안 난수 바이트 생성기를 사용해 애플리케이션에 안전한 암호화 키를 생성하기 때문입니다. 보통 `APP_KEY` 환경 변수는 [Laravel's installation](/docs/13.x/installation)에서 자동으로 생성됩니다.

<a name="gracefully-rotating-encryption-keys"></a>
<!-- ### Gracefully Rotating Encryption Keys -->
### Gracefully Rotating Encryption Keys

<!-- If you change your application's encryption key, all authenticated user sessions will be logged out of your application. This is because every cookie, including session cookies, are encrypted by Laravel. In addition, it will no longer be possible to decrypt any data that was encrypted with your previous encryption key. -->
애플리케이션의 암호화 키를 변경하면, 인증된 모든 사용자 세션이 로그아웃됩니다. 세션 쿠키를 포함한 모든 쿠키가 Laravel에 의해 암호화되기 때문입니다. 또한, 이전 암호화 키로 암호화된 데이터는 더 이상 복호화할 수 없게 됩니다.

<!-- To mitigate this issue, Laravel allows you to list your previous encryption keys in your application's `APP_PREVIOUS_KEYS` environment variable. This variable may contain a comma-delimited list of all of your previous encryption keys: -->
이 문제를 해결하기 위해, Laravel은 이전 암호화 키를 `APP_PREVIOUS_KEYS` 환경 변수에 나열할 수 있도록 지원합니다. 이 변수에는 이전에 사용했던 모든 암호화 키를 쉼표로 구분해 나열할 수 있습니다:

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

<!-- When you set this environment variable, Laravel will always use the "current" encryption key when encrypting values. However, when decrypting values, Laravel will first try the current key, and if decryption fails using the current key, Laravel will try all previous keys until one of the keys is able to decrypt the value. -->
이 환경 변수를 설정하면 Laravel은 암호화 시 항상 "현재" 키를 사용합니다. 복호화 시에는 먼저 현재 키를 시도하고, 실패하면 이전 키들을 순차적으로 시도하여 어느 키로든 성공하면 복호화가 이루어집니다.

<!-- This approach to graceful decryption allows users to keep using your application uninterrupted even if your encryption key is rotated. -->
이런 우아한 복호화 방식 덕분에, 암호화 키를 교체해도 사용자들은 중단 없이 애플리케이션을 계속 사용할 수 있습니다.

<a name="using-the-encrypter"></a>
<!-- ## Using the Encrypter -->
## Using the Encrypter

<a name="encrypting-a-value"></a>
<!-- #### Encrypting a Value -->
#### Encrypting a Value

<!-- You may encrypt a value using the `encryptString` method provided by the `Crypt` facade. All encrypted values are encrypted using OpenSSL and the AES-256-CBC cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC). The integrated message authentication code will prevent the decryption of any values that have been tampered with by malicious users: -->
`Crypt` 파사드에서 제공하는 `encryptString` 메서드를 사용해 값을 암호화할 수 있습니다. 모든 암호화된 값은 OpenSSL과 AES-256-CBC 암호화 방식을 사용하며, 메시지 인증 코드(MAC)로 서명됩니다. 통합된 MAC 덕분에, 악의적인 사용자가 변조한 값은 복호화되지 않습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * Store a DigitalOcean API token for the user.
     */
    public function store(Request $request): RedirectResponse
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();

        return redirect('/secrets');
    }
}
```

<a name="decrypting-a-value"></a>
<!-- #### Decrypting a Value -->
#### Decrypting a Value

<!-- You may decrypt values using the `decryptString` method provided by the `Crypt` facade. If the value cannot be properly decrypted, such as when the message authentication code is invalid, an `Illuminate\Contracts\Encryption\DecryptException` will be thrown: -->
`Crypt` 파사드의 `decryptString` 메서드로 암호화된 값을 복호화할 수 있습니다. 메시지 인증 코드가 유효하지 않거나 올바르게 복호화할 수 없는 경우, `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다:

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```
