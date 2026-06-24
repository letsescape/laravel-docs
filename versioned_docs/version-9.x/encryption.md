<!-- # Encryption -->
# Encryption

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Using The Encrypter](#using-the-encrypter)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's encryption services provide a simple, convenient interface for encrypting and decrypting text via OpenSSL using AES-256 and AES-128 encryption. All of Laravel's encrypted values are signed using a message authentication code (MAC) so that their underlying value can not be modified or tampered with once encrypted. -->
Laravel의 암호화 서비스는 OpenSSL을 활용하여 AES-256 및 AES-128 암호화를 통해 텍스트를 손쉽게 암호화·복호화할 수 있는 간편한 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값에는 메시지 인증 코드(MAC)가 함께 서명되어, 암호화 이후에는 데이터의 실질적인 값이 수정되거나 변조될 수 없도록 보호합니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Laravel's encrypter, you must set the `key` configuration option in your `config/app.php` configuration file. This configuration value is driven by the `APP_KEY` environment variable. You should use the `php artisan key:generate` command to generate this variable's value since the `key:generate` command will use PHP's secure random bytes generator to build a cryptographically secure key for your application. Typically, the value of the `APP_KEY` environment variable will be generated for you during [Laravel's installation](/docs/9.x/installation). -->
Laravel의 Encrypter를 사용하기 전에, 반드시 `config/app.php` 설정 파일 내의 `key` 옵션을 설정해야 합니다. 이 설정 값은 `APP_KEY` 환경 변수에 의해 지정됩니다. `php artisan key:generate` 명령어를 사용하여 해당 변수의 값을 생성하는 것이 좋습니다. `key:generate` 명령어는 PHP의 보안 난수 생성기를 활용해 애플리케이션에 암호학적으로 안전한 키를 만들어 줍니다. 일반적으로 [Laravel's installation](/docs/9.x/installation) 중에 `APP_KEY` 환경 변수의 값이 자동으로 생성됩니다.

<a name="using-the-encrypter"></a>
<!-- ## Using The Encrypter -->
## Using The Encrypter

<a name="encrypting-a-value"></a>
<!-- #### Encrypting A Value -->
#### Encrypting A Value

<!-- You may encrypt a value using the `encryptString` method provided by the `Crypt` facade. All encrypted values are encrypted using OpenSSL and the AES-256-CBC cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC). The integrated message authentication code will prevent the decryption of any values that have been tampered with by malicious users: -->
`Crypt` 파사드에서 제공하는 `encryptString` 메서드를 이용해 값을 암호화할 수 있습니다. 암호화된 값은 모두 OpenSSL과 AES-256-CBC 암호화 알고리즘을 사용하며, 메시지 인증 코드(MAC)로 서명됩니다. 이 메시지 인증 코드 덕분에 악의적인 사용자가 변조한 값에 대해서는 복호화가 차단됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * Store a DigitalOcean API token for the user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function storeSecret(Request $request)
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();
    }
}
```

<a name="decrypting-a-value"></a>
<!-- #### Decrypting A Value -->
#### Decrypting A Value

<!-- You may decrypt values using the `decryptString` method provided by the `Crypt` facade. If the value can not be properly decrypted, such as when the message authentication code is invalid, an `Illuminate\Contracts\Encryption\DecryptException` will be thrown: -->
암호화된 값은 `Crypt` 파사드의 `decryptString` 메서드로 복호화할 수 있습니다. 만약 메시지 인증 코드가 올바르지 않거나 복호화에 실패할 경우, `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다.

```
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    //
}
```
