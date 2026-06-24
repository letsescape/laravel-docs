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
Laravel の暗号化サービスは、AES-256 および AES-128 暗号化を使用して OpenSSL 経由でテキストを暗号化および復号化するためのシンプルで便利なインターフェイスを提供します。 Laravel の暗号化された値はすべて、メッセージ認証コード (MAC) を使用して署名されるため、一度暗号化されると、基になる値が変更されたり改ざんされたりすることはありません。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Laravel's encrypter, you must set the `key` configuration option in your `config/app.php` configuration file. This configuration value is driven by the `APP_KEY` environment variable. You should use the `php artisan key:generate` command to generate this variable's value since the `key:generate` command will use PHP's secure random bytes generator to build a cryptographically secure key for your application. Typically, the value of the `APP_KEY` environment variable will be generated for you during [Laravel's installation](/docs/12.x/installation). -->
Laravel の暗号化機能を使用する前に、`config/app.php` 構成ファイルで `key` 構成オプションを設定する必要があります。この構成値は、`APP_KEY` 環境変数によって駆動されます。 `key:generate` コマンドは PHP の安全なランダム バイト ジェネレーターを使用してアプリケーションの暗号的に安全なキーを構築するため、この変数の値を生成するには `php artisan key:generate` コマンドを使用する必要があります。通常、`APP_KEY` 環境変数の値は、[Laravel's installation](/docs/12.x/installation) 中に生成されます。

<a name="gracefully-rotating-encryption-keys"></a>
<!-- ### Gracefully Rotating Encryption Keys -->
### Gracefully Rotating Encryption Keys

<!-- If you change your application's encryption key, all authenticated user sessions will be logged out of your application. This is because every cookie, including session cookies, are encrypted by Laravel. In addition, it will no longer be possible to decrypt any data that was encrypted with your previous encryption key. -->
アプリケーションの暗号化キーを変更すると、認証されたすべてのユーザー セッションがアプリケーションからログアウトされます。これは、セッション Cookie を含むすべての Cookie が Laravel によって暗号化されるためです。さらに、以前の暗号化キーで暗号化されたデータを復号化することはできなくなります。

<!-- To mitigate this issue, Laravel allows you to list your previous encryption keys in your application's `APP_PREVIOUS_KEYS` environment variable. This variable may contain a comma-delimited list of all of your previous encryption keys: -->
この問題を軽減するために、Laravel では、アプリケーションの `APP_PREVIOUS_KEYS` 環境変数に以前の暗号化キーをリストすることができます。この変数には、以前のすべての暗号化キーのカンマ区切りのリストが含まれる場合があります。

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

<!-- When you set this environment variable, Laravel will always use the "current" encryption key when encrypting values. However, when decrypting values, Laravel will first try the current key, and if decryption fails using the current key, Laravel will try all previous keys until one of the keys is able to decrypt the value. -->
この環境変数を設定すると、Laravel は値を暗号化するときに常に「現在の」暗号化キーを使用します。ただし、値を復号化するとき、Laravel は最初に現在のキーを試し、現在のキーを使用した復号化が失敗した場合、Laravel はキーの 1 つが値を復号化できるまで、以前のすべてのキーを試します。

<!-- This approach to graceful decryption allows users to keep using your application uninterrupted even if your encryption key is rotated. -->
この正常な復号化のアプローチにより、暗号化キーがローテーションされた場合でも、ユーザーはアプリケーションを中断することなく使用し続けることができます。

<a name="using-the-encrypter"></a>
<!-- ## Using the Encrypter -->
## Using the Encrypter

<a name="encrypting-a-value"></a>
<!-- #### Encrypting a Value -->
#### Encrypting a Value

<!-- You may encrypt a value using the `encryptString` method provided by the `Crypt` facade. All encrypted values are encrypted using OpenSSL and the AES-256-CBC cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC). The integrated message authentication code will prevent the decryption of any values that have been tampered with by malicious users: -->
`Crypt` ファサードによって提供される `encryptString` メソッドを使用して値を暗号化できます。すべての暗号化された値は、OpenSSL と AES-256-CBC 暗号を使用して暗号化されます。さらに、暗号化されたすべての値はメッセージ認証コード (MAC) で署名されます。統合されたメッセージ認証コードは、悪意のあるユーザーによって改ざんされた値の復号化を防ぎます。

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
`Crypt` ファサードによって提供される `decryptString` メソッドを使用して値を復号化できます。メッセージ認証コードが無効な場合など、値を適切に復号化できない場合は、`Illuminate\Contracts\Encryption\DecryptException` がスローされます。

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```

