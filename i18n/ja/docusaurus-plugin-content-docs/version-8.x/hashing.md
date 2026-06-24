<!-- # Hashing -->
# Hashing

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
    - [Hashing Passwords](#hashing-passwords)
    - [Verifying That A Password Matches A Hash](#verifying-that-a-password-matches-a-hash)
    - [Determining If A Password Needs To Be Rehashed](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The Laravel `Hash` [facade](/docs/8.x/facades) provides secure Bcrypt and Argon2 hashing for storing user passwords. If you are using one of the [Laravel application starter kits](/docs/8.x/starter-kits), Bcrypt will be used for registration and authentication by default. -->
Laravel `Hash` [facade](/docs/8.x/facades) は、ユーザーパスワードを保存するための安全な Bcrypt および Argon2 ハッシュを提供します。 [Laravel application starter kits](/docs/8.x/starter-kits) のいずれかを使用している場合、デフォルトで登録と認証に Bcrypt が使用されます。

<!-- Bcrypt is a great choice for hashing passwords because its "work factor" is adjustable, which means that the time it takes to generate a hash can be increased as hardware power increases. When hashing passwords, slow is good. The longer an algorithm takes to hash a password, the longer it takes malicious users to generate "rainbow tables" of all possible string hash values that may be used in brute force attacks against applications. -->
Bcrypt は、「作業係数」を調整できるため、パスワードをハッシュするのに最適な選択肢です。つまり、ハードウェアの能力が向上すると、ハッシュの生成にかかる時間が増加する可能性があります。パスワードをハッシュするときは、遅い方が良いです。アルゴリズムがパスワードをハッシュするのに時間がかかるほど、悪意のあるユーザーがアプリケーションに対するブルート フォース攻撃に使用される可能性のあるすべての文字列ハッシュ値の「レインボー テーブル」を生成するのにかかる時間が長くなります。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- The default hashing driver for your application is configured in your application's `config/hashing.php` configuration file. There are currently several supported drivers: [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt) and [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i and Argon2id variants). -->
アプリケーションのデフォルトのハッシュ ドライバは、アプリケーションの `config/hashing.php` 構成ファイルで構成されます。現在サポートされているドライバは、[Bcrypt](https://en.wikipedia.org/wiki/Bcrypt) および [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i および Argon2id のバリアント) です。

> [!NOTE]
> Argon2i ドライバには PHP 7.2.0 以降が必要で、Argon2id ドライバには PHP 7.3.0 以降が必要です。

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<a name="hashing-passwords"></a>
<!-- ### Hashing Passwords -->
### Hashing Passwords

<!-- You may hash a password by calling the `make` method on the `Hash` facade: -->
`Hash` ファサードで `make` メソッドを呼び出すことで、パスワードをハッシュできます。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * Update the password for the user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request)
    {
        // Validate the new password length...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
<!-- #### Adjusting The Bcrypt Work Factor -->
#### Adjusting The Bcrypt Work Factor

<!-- If you are using the Bcrypt algorithm, the `make` method allows you to manage the work factor of the algorithm using the `rounds` option; however, the default work factor managed by Laravel is acceptable for most applications: -->
Bcrypt アルゴリズムを使用している場合、`make` メソッドでは、`rounds` オプションを使用してアルゴリズムの作業係数を管理できます。ただし、Laravel によって管理されるデフォルトの作業係数は、ほとんどのアプリケーションで受け入れられます。

```
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
<!-- #### Adjusting The Argon2 Work Factor -->
#### Adjusting The Argon2 Work Factor

<!-- If you are using the Argon2 algorithm, the `make` method allows you to manage the work factor of the algorithm using the `memory`, `time`, and `threads` options; however, the default values managed by Laravel are acceptable for most applications: -->
Argon2 アルゴリズムを使用している場合、`make` メソッドでは、`memory`、`time`、および `threads` オプションを使用してアルゴリズムの作業係数を管理できます。ただし、Laravel によって管理されるデフォルト値は、ほとんどのアプリケーションで受け入れられます。

```
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!TIP]
> これらのオプションの詳細については、[official PHP documentation regarding Argon hashing](https://secure.php.net/manual/en/function.password-hash.php) を参照してください。

<a name="verifying-that-a-password-matches-a-hash"></a>
<!-- ### Verifying That A Password Matches A Hash -->
### Verifying That A Password Matches A Hash

<!-- The `check` method provided by the `Hash` facade allows you to verify that a given plain-text string corresponds to a given hash: -->
`Hash` ファサードによって提供される `check` メソッドを使用すると、指定されたプレーンテキスト文字列が指定されたハッシュに対応することを検証できます。

```
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
<!-- ### Determining If A Password Needs To Be Rehashed -->
### Determining If A Password Needs To Be Rehashed

<!-- The `needsRehash` method provided by the `Hash` facade allows you to determine if the work factor used by the hasher has changed since the password was hashed. Some applications choose to perform this check during the application's authentication process: -->
`Hash` ファサードによって提供される `needsRehash` メソッドを使用すると、パスワードがハッシュされてからハッシャーによって使用される作業係数が変更されたかどうかを判断できます。一部のアプリケーションは、アプリケーションの認証プロセス中にこのチェックを実行することを選択します。

```
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

