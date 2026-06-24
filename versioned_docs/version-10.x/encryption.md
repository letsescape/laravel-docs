<!-- # Encryption -->
# Encryption

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Using the Encrypter](#using-the-encrypter)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's encryption services provide a simple, convenient interface for encrypting and decrypting text via OpenSSL using AES-256 and AES-128 encryption. All of Laravel's encrypted values are signed using a message authentication code (MAC) so that their underlying value can not be modified or tampered with once encrypted. -->
Laravel의 암호화 서비스는 OpenSSL을 기반으로 AES-256과 AES-128 암호화를 통해 텍스트를 암호화하고 복호화할 수 있는 쉽고 편리한 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값들은 메시지 인증 코드(MAC, Message Authentication Code)로 서명되어, 한 번 암호화된 이후에는 그 값이 외부에서 임의로 변경되거나 위조될 수 없도록 보호합니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Laravel's encrypter, you must set the `key` configuration option in your `config/app.php` configuration file. This configuration value is driven by the `APP_KEY` environment variable. You should use the `php artisan key:generate` command to generate this variable's value since the `key:generate` command will use PHP's secure random bytes generator to build a cryptographically secure key for your application. Typically, the value of the `APP_KEY` environment variable will be generated for you during [Laravel's installation](/docs/10.x/installation). -->
Laravel의 Encrypter를 사용하기 전에, `config/app.php` 설정 파일에서 `key` 설정 옵션을 반드시 지정해야 합니다. 이 설정 값은 `APP_KEY` 환경 변수에 의해 결정됩니다. 이 변수의 값을 생성할 때는 `php artisan key:generate` 명령어를 사용하는 것이 좋습니다. `key:generate` 명령어는 PHP의 보안 랜덤 바이트 생성기를 활용하여, 애플리케이션에 적합한 암호화 키를 안전하게 생성해줍니다. 일반적으로, `APP_KEY` 환경 변수의 값은 [Laravel's installation](/docs/10.x/installation)에서 자동으로 생성됩니다.

<a name="using-the-encrypter"></a>
<!-- ## Using the Encrypter -->
## Using the Encrypter

<a name="encrypting-a-value"></a>
<!-- #### Encrypting a Value -->
#### Encrypting a Value

<!-- You may encrypt a value using the `encryptString` method provided by the `Crypt` facade. All encrypted values are encrypted using OpenSSL and the AES-256-CBC cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC). The integrated message authentication code will prevent the decryption of any values that have been tampered with by malicious users: -->
`Crypt` 파사드에서 제공하는 `encryptString` 메서드를 사용해 값을 암호화할 수 있습니다. 암호화된 모든 값은 OpenSSL을 사용하고, AES-256-CBC 암호화 방식을 적용합니다. 또한 모든 암호화 값은 메시지 인증 코드(MAC)로 서명됩니다. 내장된 메시지 인증 코드를 통해, 사용자가 악의적으로 값을 변조했다면 해당 값의 복호화가 불가능해지므로 안전하게 보호할 수 있습니다.

```
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

<!-- You may decrypt values using the `decryptString` method provided by the `Crypt` facade. If the value can not be properly decrypted, such as when the message authentication code is invalid, an `Illuminate\Contracts\Encryption\DecryptException` will be thrown: -->
암호화된 값을 복호화하려면 `Crypt` 파사드에서 제공하는 `decryptString` 메서드를 사용하면 됩니다. 만약 메시지 인증 코드(MAC)가 올바르지 않거나, 다른 이유로 값이 정상적으로 복호화되지 않으면 `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다.

```
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```