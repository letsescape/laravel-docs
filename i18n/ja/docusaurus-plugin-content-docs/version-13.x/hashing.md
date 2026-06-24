<!-- # Hashing -->
# Hashing

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
    - [Hashing Passwords](#hashing-passwords)
    - [Verifying That a Password Matches a Hash](#verifying-that-a-password-matches-a-hash)
    - [Determining if a Password Needs to be Rehashed](#determining-if-a-password-needs-to-be-rehashed)
- [Hash Algorithm Verification](#hash-algorithm-verification)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The Laravel `Hash` [facade](/docs/13.x/facades) provides secure Bcrypt and Argon2 hashing for storing user passwords. If you are using one of the [Laravel application starter kits](/docs/13.x/starter-kits), Bcrypt will be used for registration and authentication by default. -->
Laravel `Hash` [facade](/docs/13.x/facades) は、ユーザーパスワードを保存するための安全な Bcrypt および Argon2 ハッシュを提供します。 [Laravel application starter kits](/docs/13.x/starter-kits) のいずれかを使用している場合、デフォルトで登録と認証に Bcrypt が使用されます。

<!-- Bcrypt is a great choice for hashing passwords because its "work factor" is adjustable, which means that the time it takes to generate a hash can be increased as hardware power increases. When hashing passwords, slow is good. The longer an algorithm takes to hash a password, the longer it takes malicious users to generate "rainbow tables" of all possible string hash values that may be used in brute force attacks against applications. -->
Bcrypt は、「作業係数」を調整できるため、パスワードをハッシュするのに最適な選択肢です。つまり、ハードウェアの能力が向上すると、ハッシュの生成にかかる時間が増加する可能性があります。パスワードをハッシュするときは、遅い方が良いです。アルゴリズムがパスワードをハッシュするのに時間がかかるほど、悪意のあるユーザーがアプリケーションに対するブルート フォース攻撃に使用される可能性のあるすべての文字列ハッシュ値の「レインボー テーブル」を生成するのにかかる時間が長くなります。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- By default, Laravel uses the `bcrypt` hashing driver when hashing data. However, several other hashing drivers are supported, including [argon](https://en.wikipedia.org/wiki/Argon2) and [argon2id](https://en.wikipedia.org/wiki/Argon2). -->
デフォルトでは、Laravel はデータをハッシュするときに `bcrypt` ハッシュドライバを使用します。ただし、[argon](https://en.wikipedia.org/wiki/Argon2) や [argon2id](https://en.wikipedia.org/wiki/Argon2) など、他のいくつかのハッシュ ドライバがサポートされています。

<!-- You may specify your application's hashing driver using the `HASH_DRIVER` environment variable. But, if you want to customize all of Laravel's hashing driver options, you should publish the complete `hashing` configuration file using the `config:publish` Artisan command: -->
`HASH_DRIVER` 環境変数を使用して、アプリケーションのハッシュ ドライバを指定できます。ただし、Laravel のハッシュ ドライバ オプションをすべてカスタマイズしたい場合は、`config:publish` Artisan コマンドを使用して、完全な `hashing` 構成ファイルを公開する必要があります。

```shell
php artisan config:publish hashing
```

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<a name="hashing-passwords"></a>
<!-- ### Hashing Passwords -->
### Hashing Passwords

<!-- You may hash a password by calling the `make` method on the `Hash` facade: -->
`Hash` ファサードで `make` メソッドを呼び出すことで、パスワードをハッシュできます。

```php
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
```

<a name="adjusting-the-bcrypt-work-factor"></a>
<!-- #### Adjusting The Bcrypt Work Factor -->
#### Adjusting The Bcrypt Work Factor

<!-- If you are using the Bcrypt algorithm, the `make` method allows you to manage the work factor of the algorithm using the `rounds` option; however, the default work factor managed by Laravel is acceptable for most applications: -->
Bcrypt アルゴリズムを使用している場合、`make` メソッドでは、`rounds` オプションを使用してアルゴリズムの作業係数を管理できます。ただし、Laravel によって管理されるデフォルトの作業係数は、ほとんどのアプリケーションで受け入れられます。

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
<!-- #### Adjusting The Argon2 Work Factor -->
#### Adjusting The Argon2 Work Factor

<!-- If you are using the Argon2 algorithm, the `make` method allows you to manage the work factor of the algorithm using the `memory`, `time`, and `threads` options; however, the default values managed by Laravel are acceptable for most applications: -->
Argon2 アルゴリズムを使用している場合、`make` メソッドでは、`memory`、`time`、および `threads` オプションを使用してアルゴリズムの作業係数を管理できます。ただし、Laravel によって管理されるデフォルト値は、ほとんどのアプリケーションで受け入れられます。

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> これらのオプションの詳細については、[official PHP documentation regarding Argon hashing](https://secure.php.net/manual/en/function.password-hash.php) を参照してください。

<a name="verifying-that-a-password-matches-a-hash"></a>
<!-- ### Verifying That a Password Matches a Hash -->
### Verifying That a Password Matches a Hash

<!-- The `check` method provided by the `Hash` facade allows you to verify that a given plain-text string corresponds to a given hash: -->
`Hash` ファサードによって提供される `check` メソッドを使用すると、指定されたプレーンテキスト文字列が指定されたハッシュに対応することを検証できます。

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
<!-- ### Determining if a Password Needs to be Rehashed -->
### Determining if a Password Needs to be Rehashed

<!-- The `needsRehash` method provided by the `Hash` facade allows you to determine if the work factor used by the hasher has changed since the password was hashed. Some applications choose to perform this check during the application's authentication process: -->
`Hash` ファサードによって提供される `needsRehash` メソッドを使用すると、パスワードがハッシュされてからハッシャーによって使用される作業係数が変更されたかどうかを判断できます。一部のアプリケーションは、アプリケーションの認証プロセス中にこのチェックを実行することを選択します。

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
<!-- ## Hash Algorithm Verification -->
## Hash Algorithm Verification

<!-- To prevent hash algorithm manipulation, Laravel's `Hash::check` method will first verify the given hash was generated using the application's selected hashing algorithm. If the algorithms are different, a `RuntimeException` exception will be thrown. -->
ハッシュアルゴリズムの操作を防ぐために、Laravelの`Hash::check`メソッドは、指定されたハッシュがアプリケーションの選択されたハッシュアルゴリズムを使用して生成されたことを最初に検証します。アルゴリズムが異なる場合、`RuntimeException` 例外がスローされます。

<!-- This is the expected behavior for most applications, where the hashing algorithm is not expected to change and different algorithms can be an indication of a malicious attack. However, if you need to support multiple hashing algorithms within your application, such as when migrating from one algorithm to another, you can disable hash algorithm verification by setting the `HASH_VERIFY` environment variable to `false`: -->
これはほとんどのアプリケーションで予期される動作であり、ハッシュ アルゴリズムが変更されることは予期されておらず、異なるアルゴリズムは悪意のある攻撃を示す可能性があります。ただし、あるアルゴリズムから別のアルゴリズムに移行する場合など、アプリケーション内で複数のハッシュ アルゴリズムをサポートする必要がある場合は、`HASH_VERIFY` 環境変数を `false` に設定することで、ハッシュ アルゴリズムの検証を無効にすることができます。

```ini
HASH_VERIFY=false
```

