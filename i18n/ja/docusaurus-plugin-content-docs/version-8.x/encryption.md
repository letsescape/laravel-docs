# 暗号化 (Encryption)

- [Introduction](#introduction)
- [Configuration](#configuration)
- [暗号化ツールの使用](#using-the-encrypter)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel の暗号化サービスは、AES-256 および AES-128 暗号化を使用して OpenSSL 経由でテキストを暗号化および復号化するためのシンプルで便利なインターフェイスを提供します。 Laravel の暗号化された値はすべて、メッセージ認証コード (MAC) を使用して署名されるため、暗号化されると、基になる値を変更したり改ざんしたりすることはできません。

<a name="configuration"></a>
## 構成 (Configuration)

Laravel の暗号化機能を使用する前に、`config/app.php` 構成ファイルで `key` 構成オプションを設定する必要があります。この構成値は、`APP_KEY` 環境変数によって駆動されます。 `key:generate` コマンドは PHP の安全なランダム バイト ジェネレーターを使用してアプリケーションの暗号的に安全なキーを構築するため、この変数の値を生成するには `php artisan key:generate` コマンドを使用する必要があります。通常、`APP_KEY` 環境変数の値は、[Laravelのインストール](/docs/{{version}}/installation) 中に生成されます。

<a name="using-the-encrypter"></a>
## 暗号化ツールの使用 (Using The Encrypter)

<a name="encrypting-a-value"></a>
#### 値の暗号化

`Crypt` ファサードによって提供される `encryptString` メソッドを使用して値を暗号化できます。すべての暗号化された値は、OpenSSL と AES-256-CBC 暗号を使用して暗号化されます。さらに、暗号化されたすべての値はメッセージ認証コード (MAC) で署名されます。統合されたメッセージ認証コードは、悪意のあるユーザーによって改ざんされた値の復号化を防ぎます。

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

<a name="decrypting-a-value"></a>
#### 値の復号化

`Crypt` ファサードによって提供される `decryptString` メソッドを使用して値を復号化できます。メッセージ認証コードが無効な場合など、値を適切に復号化できない場合は、`Illuminate\Contracts\Encryption\DecryptException` がスローされます。

    use Illuminate\Contracts\Encryption\DecryptException;
    use Illuminate\Support\Facades\Crypt;

    try {
        $decrypted = Crypt::decryptString($encryptedValue);
    } catch (DecryptException $e) {
        //
    }

