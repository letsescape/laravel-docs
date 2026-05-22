# 暗号化 (Encryption)

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [暗号化キーを適切にローテーションする](#gracefully-rotating-encryption-keys)
- [暗号化ツールの使用](#using-the-encrypter)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel の暗号化サービスは、AES-256 および AES-128 暗号化を使用して OpenSSL 経由でテキストを暗号化および復号化するためのシンプルで便利なインターフェイスを提供します。 Laravel の暗号化された値はすべて、メッセージ認証コード (MAC) を使用して署名されるため、一度暗号化されると、基になる値が変更されたり改ざんされたりすることはありません。

<a name="configuration"></a>
## 構成 (Configuration)

Laravel の暗号化機能を使用する前に、`config/app.php` 構成ファイルで `key` 構成オプションを設定する必要があります。この構成値は、`APP_KEY` 環境変数によって駆動されます。 `key:generate` コマンドは PHP の安全なランダム バイト ジェネレーターを使用してアプリケーションの暗号的に安全なキーを構築するため、この変数の値を生成するには `php artisan key:generate` コマンドを使用する必要があります。通常、`APP_KEY` 環境変数の値は、[Laravelのインストール](/docs/{{version}}/installation) 中に生成されます。

<a name="gracefully-rotating-encryption-keys"></a>
### 暗号化キーを適切にローテーションする

アプリケーションの暗号化キーを変更すると、認証されたすべてのユーザー セッションがアプリケーションからログアウトされます。これは、セッション Cookie を含むすべての Cookie が Laravel によって暗号化されるためです。さらに、以前の暗号化キーで暗号化されたデータを復号化することはできなくなります。

この問題を軽減するために、Laravel では、アプリケーションの `APP_PREVIOUS_KEYS` 環境変数に以前の暗号化キーをリストすることができます。この変数には、以前のすべての暗号化キーのカンマ区切りのリストが含まれる場合があります。

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

この環境変数を設定すると、Laravel は値を暗号化するときに常に「現在の」暗号化キーを使用します。ただし、値を復号化するとき、Laravel は最初に現在のキーを試し、現在のキーを使用した復号化が失敗した場合、Laravel はキーの 1 つが値を復号化できるまで、以前のすべてのキーを試します。

この正常な復号化のアプローチにより、暗号化キーがローテーションされた場合でも、ユーザーはアプリケーションを中断することなく使用し続けることができます。

<a name="using-the-encrypter"></a>
## 暗号化ツールの使用 (Using the Encrypter)

<a name="encrypting-a-value"></a>
#### 値の暗号化

`Crypt` ファサードによって提供される `encryptString` メソッドを使用して値を暗号化できます。すべての暗号化された値は、OpenSSL と AES-256-CBC 暗号を使用して暗号化されます。さらに、暗号化されたすべての値はメッセージ認証コード (MAC) で署名されます。統合されたメッセージ認証コードは、悪意のあるユーザーによって改ざんされた値の復号化を防ぎます。

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

<a name="decrypting-a-value"></a>
#### 値の復号化

`Crypt` ファサードによって提供される `decryptString` メソッドを使用して値を復号化できます。メッセージ認証コードが無効な場合など、値を適切に復号化できない場合は、`Illuminate\Contracts\Encryption\DecryptException` がスローされます。

    use Illuminate\Contracts\Encryption\DecryptException;
    use Illuminate\Support\Facades\Crypt;

    try {
        $decrypted = Crypt::decryptString($encryptedValue);
    } catch (DecryptException $e) {
        // ...
    }

