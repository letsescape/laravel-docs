# ハッシュ化 (Hashing)

- [Introduction](#introduction)
- [Configuration](#configuration)
- [基本的な使い方](#basic-usage)
    - [パスワードのハッシュ化](#hashing-passwords)
    - [パスワードがハッシュと一致することを確認する](#verifying-that-a-password-matches-a-hash)
    - [パスワードを再ハッシュする必要があるかどうかを判断する](#determining-if-a-password-needs-to-be-rehashed)
- [ハッシュアルゴリズムの検証](#hash-algorithm-verification)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel `Hash` [facade](/docs/{{version}}/facades) は、ユーザーパスワードを保存するための安全な Bcrypt および Argon2 ハッシュを提供します。 [Laravelアプリケーションスターターキット](/docs/{{version}}/starter-kits) のいずれかを使用している場合、デフォルトで登録と認証に Bcrypt が使用されます。

Bcrypt は、「作業係数」を調整できるため、パスワードをハッシュするのに最適な選択肢です。つまり、ハードウェアの能力が向上すると、ハッシュの生成にかかる時間が増加する可能性があります。パスワードをハッシュするときは、遅い方が良いです。アルゴリズムがパスワードをハッシュするのに時間がかかるほど、悪意のあるユーザーがアプリケーションに対するブルート フォース攻撃に使用される可能性のあるすべての文字列ハッシュ値の「レインボー テーブル」を生成するのにかかる時間が長くなります。

<a name="configuration"></a>
## 構成 (Configuration)

デフォルトでは、Laravel はデータをハッシュするときに `bcrypt` ハッシュドライバを使用します。ただし、[`argon`](https://en.wikipedia.org/wiki/Argon2) や [`argon2id`](https://en.wikipedia.org/wiki/Argon2) など、他のいくつかのハッシュ ドライバがサポートされています。

`HASH_DRIVER` 環境変数を使用して、アプリケーションのハッシュ ドライバを指定できます。ただし、Laravel のハッシュ ドライバ オプションをすべてカスタマイズしたい場合は、`config:publish` Artisan コマンドを使用して、完全な `hashing` 構成ファイルを公開する必要があります。

```bash
php artisan config:publish hashing
```

<a name="basic-usage"></a>
## 基本的な使い方 (Basic Usage)

<a name="hashing-passwords"></a>
### パスワードのハッシュ化

`Hash` ファサードで `make` メソッドを呼び出すことで、パスワードをハッシュできます。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Hash;

    class PasswordController extends Controller
    {
        /**
         * Update the password for the user.
         */
        public function update(Request $request): RedirectResponse
        {
            // Validate the new password length...

            $request->user()->fill([
                'password' => Hash::make($request->newPassword)
            ])->save();

            return redirect('/profile');
        }
    }

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 作業係数の調整

Bcrypt アルゴリズムを使用している場合、`make` メソッドでは、`rounds` オプションを使用してアルゴリズムの作業係数を管理できます。ただし、Laravel によって管理されるデフォルトの作業係数は、ほとんどのアプリケーションで受け入れられます。

    $hashed = Hash::make('password', [
        'rounds' => 12,
    ]);

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 仕事係数の調整

Argon2 アルゴリズムを使用している場合、`make` メソッドでは、`memory`、`time`、および `threads` オプションを使用してアルゴリズムの作業係数を管理できます。ただし、Laravel によって管理されるデフォルト値は、ほとんどのアプリケーションで受け入れられます。

    $hashed = Hash::make('password', [
        'memory' => 1024,
        'time' => 2,
        'threads' => 2,
    ]);

> [!NOTE]  
> これらのオプションの詳細については、[アルゴンハッシュに関する公式 PHP ドキュメント](https://secure.php.net/manual/en/function.password-hash.php) を参照してください。

<a name="verifying-that-a-password-matches-a-hash"></a>
### パスワードがハッシュと一致することを確認する

`Hash` ファサードによって提供される `check` メソッドを使用すると、指定されたプレーンテキスト文字列が指定されたハッシュに対応することを検証できます。

    if (Hash::check('plain-text', $hashedPassword)) {
        // The passwords match...
    }

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### パスワードを再ハッシュする必要があるかどうかを判断する

`Hash` ファサードによって提供される `needsRehash` メソッドを使用すると、パスワードがハッシュされてからハッシャーによって使用される作業係数が変更されたかどうかを判断できます。一部のアプリケーションは、アプリケーションの認証プロセス中にこのチェックを実行することを選択します。

    if (Hash::needsRehash($hashed)) {
        $hashed = Hash::make('plain-text');
    }

<a name="hash-algorithm-verification"></a>
## ハッシュアルゴリズムの検証 (Hash Algorithm Verification)

ハッシュアルゴリズムの操作を防ぐために、Laravelの`Hash::check`メソッドは、指定されたハッシュがアプリケーションの選択されたハッシュアルゴリズムを使用して生成されたことを最初に検証します。アルゴリズムが異なる場合、`RuntimeException` 例外がスローされます。

これはほとんどのアプリケーションで予期される動作であり、ハッシュ アルゴリズムが変更されることは予期されておらず、異なるアルゴリズムは悪意のある攻撃を示す可能性があります。ただし、あるアルゴリズムから別のアルゴリズムに移行する場合など、アプリケーション内で複数のハッシュ アルゴリズムをサポートする必要がある場合は、`HASH_VERIFY` 環境変数を `false` に設定することで、ハッシュ アルゴリズムの検証を無効にすることができます。

```ini
HASH_VERIFY=false
```

