<!-- # Encryption -->
# Encryption

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Using The Encrypter](#using-the-encrypter)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's encryption services provide a simple, convenient interface for encrypting and decrypting text via OpenSSL using AES-256 and AES-128 encryption. All of Laravel's encrypted values are signed using a message authentication code (MAC) so that their underlying value can not be modified or tampered with once encrypted. -->
Laravel の暗号化サービスは、AES-256 および AES-128 暗号化を使用して OpenSSL 経由でテキストを暗号化および復号化するためのシンプルで便利なインターフェイスを提供します。 Laravel の暗号化された値はすべて、メッセージ認証コード (MAC) を使用して署名されるため、暗号化されると、基になる値を変更したり改ざんしたりすることはできません。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Laravel's encrypter, you must set the `key` configuration option in your `config/app.php` configuration file. This configuration value is driven by the `APP_KEY` environment variable. You should use the `php artisan key:generate` command to generate this variable's value since the `key:generate` command will use PHP's secure random bytes generator to build a cryptographically secure key for your application. Typically, the value of the `APP_KEY` environment variable will be generated for you during [Laravel's installation](/docs/8.x/installation). -->
Laravel の暗号化機能を使用する前に、`config/app.php` 構成ファイルで `key` 構成オプションを設定する必要があります。この構成値は、`APP_KEY` 環境変数によって駆動されます。 `key:generate` コマンドは PHP の安全なランダム バイト ジェネレーターを使用してアプリケーションの暗号的に安全なキーを構築するため、この変数の値を生成するには `php artisan key:generate` コマンドを使用する必要があります。通常、`APP_KEY` 環境変数の値は、[Laravel's installation](/docs/8.x/installation) 中に生成されます。

<a name="using-the-encrypter"></a>
<!-- ## Using The Encrypter -->
## Using The Encrypter

<a name="encrypting-a-value"></a>
<!-- #### Encrypting A Value -->
#### Encrypting A Value

<!-- You may encrypt a value using the `encryptString` method provided by the `Crypt` facade. All encrypted values are encrypted using OpenSSL and the AES-256-CBC cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC). The integrated message authentication code will prevent the decryption of any values that have been tampered with by malicious users: -->
`Crypt` ファサードによって提供される `encryptString` メソッドを使用して値を暗号化できます。すべての暗号化された値は、OpenSSL と AES-256-CBC 暗号を使用して暗号化されます。さらに、暗号化されたすべての値はメッセージ認証コード (MAC) で署名されます。統合されたメッセージ認証コードは、悪意のあるユーザーによって改ざんされた値の復号化を防ぎます。

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
`Crypt` ファサードによって提供される `decryptString` メソッドを使用して値を復号化できます。メッセージ認証コードが無効な場合など、値を適切に復号化できない場合は、`Illuminate\Contracts\Encryption\DecryptException` がスローされます。

```
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    //
}
```

