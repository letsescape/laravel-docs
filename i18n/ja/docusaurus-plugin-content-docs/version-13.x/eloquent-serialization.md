# Eloquent: 連載 (Eloquent: Serialization)

- [Introduction](#introduction)
- [モデルとコレクションのシリアル化](#serializing-models-and-collections)
    - [配列へのシリアル化](#serializing-to-arrays)
    - [JSON へのシリアル化](#serializing-to-json)
- [JSON からの属性の非表示](#hiding-attributes-from-json)
- [JSON への値の追加](#appending-values-to-json)
- [日付のシリアル化](#date-serialization)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel を使用して API を構築する場合、多くの場合、モデルと関係を配列または JSON に変換する必要があります。 Eloquent には、これらの変換を行うだけでなく、モデルのシリアル化された表現にどの属性を含めるかを制御するための便利なメソッドが含まれています。

> [!NOTE]
> Eloquent モデルとコレクションの JSON シリアル化を処理するさらに堅牢な方法については、[Eloquent  API リソース](/docs/{{version}}/eloquent-resources) のドキュメントを確認してください。

<a name="serializing-models-and-collections"></a>
## モデルとコレクションのシリアル化 (Serializing Models and Collections)

<a name="serializing-to-arrays"></a>
### 配列へのシリアル化

モデルとそのロードされた [relationships](/docs/{{version}}/eloquent-relationships) を配列に変換するには、`toArray` メソッドを使用する必要があります。このメソッドは再帰的であるため、すべての属性とすべての関係 (関係の関係を含む) が配列に変換されます。

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` メソッドは、モデルの属性を配列に変換するために使用できますが、その関係は変換できません。

```php
$user = User::first();

return $user->attributesToArray();
```

コレクション インスタンスで `toArray` メソッドを呼び出して、モデルの [collections](/docs/{{version}}/eloquent-collections) 全体を配列に変換することもできます。

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON へのシリアル化

モデルを JSON に変換するには、`toJson` メソッドを使用する必要があります。 `toArray` と同様、`toJson` メソッドは再帰的であるため、すべての属性とリレーションが JSON に変換されます。 [PHPでサポートされています](https://secure.php.net/manual/en/function.json-encode.php) の JSON エンコード オプションを指定することもできます。

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

あるいは、モデルまたはコレクションを文字列にキャストすることもできます。これにより、モデルまたはコレクションに対して `toJson` メソッドが自動的に呼び出されます。

```php
return (string) User::find(1);
```

モデルとコレクションは文字列にキャストされるときに JSON に変換されるため、アプリケーションのルートまたはコントローラから直接 Eloquent オブジェクトを返すことができます。 Laravel は、Eloquent モデルとコレクションがルートまたはコントローラから返されると、自動的に JSON にシリアル化します。

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 人間関係

Eloquent モデルが JSON に変換されると、ロードされたリレーションシップが JSON オブジェクトの属性として自動的に組み込まれます。また、Eloquent リレーションシップ メソッドは「キャメル ケース」メソッド名を使用して定義されますが、リレーションシップの JSON 属性は「スネーク ケース」になります。

<a name="hiding-attributes-from-json"></a>
## JSON からの属性の非表示 (Hiding Attributes From JSON)

場合によっては、モデルの配列または JSON 表現に含まれるパスワードなどの属性を制限したい場合があります。これを行うには、モデルで `Hidden` 属性を使用できます。 `Hidden` 属性にリストされている属性は、モデルのシリアル化された表現には含まれません。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Model;

#[Hidden(['password'])]
class User extends Model
{
    // ...
}
```


> [!NOTE]
> リレーションシップを非表示にするには、リレーションシップのメソッド名を Eloquent モデルの `Hidden` 属性に追加します。

あるいは、`Visible` 属性を使用して、モデルの配列および JSON 表現に含める必要がある属性の「許可リスト」を定義することもできます。 `Visible` 属性に存在しないすべての属性は、モデルが配列または JSON に変換されるときに非表示になります。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Visible;
use Illuminate\Database\Eloquent\Model;

#[Visible(['first_name', 'last_name'])]
class User extends Model
{
    // ...
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 属性の可視性を一時的に変更する

通常非表示の属性を特定のモデル インスタンスで表示したい場合は、`makeVisible` メソッドまたは `mergeVisible` メソッドを使用できます。 `makeVisible` メソッドはモデル インスタンスを返します。

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

同様に、通常は表示される一部の属性を非表示にしたい場合は、`makeHidden` メソッドまたは `mergeHidden` メソッドを使用できます。

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

すべての表示属性または非表示属性を一時的にオーバーライドしたい場合は、それぞれ `setVisible` メソッドと `setHidden` メソッドを使用できます。

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON への値の追加 (Appending Values to JSON)

場合によっては、モデルを配列または JSON に変換するときに、データベースに対応する列がない属性を追加したい場合があります。これを行うには、まず値の [accessor](/docs/{{version}}/eloquent-mutators) を定義します。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

アクセサーを常にモデルの配列および JSON 表現に追加したい場合は、モデルで `Appends` 属性を使用できます。アクセサーの PHP メソッドが「キャメル ケース」を使用して定義されている場合でも、属性名は通常、「スネーク ケース」のシリアル化表現を使用して参照されることに注意してください。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Appends;
use Illuminate\Database\Eloquent\Model;

#[Appends(['is_admin'])]
class User extends Model
{
    // ...
}
```

属性が `appends` リストに追加されると、モデルの配列と JSON 表現の両方に含まれます。 `appends` 配列の属性は、モデルで構成された `visible` および `hidden` 設定も尊重します。

<a name="appending-at-run-time"></a>
#### 実行時に追加する

実行時に、`append` メソッドまたは `mergeAppends` メソッドを使用して追加の属性を追加するようにモデル インスタンスに指示できます。または、`setAppends` メソッドを使用して、特定のモデル インスタンスに追加されたプロパティの配列全体をオーバーライドすることもできます。

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

同様に、追加されたプロパティをすべてモデルから削除したい場合は、`withoutAppends` メソッドを使用できます。

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
## 日付のシリアル化 (Date Serialization)

<a name="customizing-the-default-date-format"></a>
#### デフォルトの日付形式のカスタマイズ

`serializeDate` メソッドをオーバーライドすることで、デフォルトのシリアル化形式をカスタマイズできます。この方法は、データベースに保存する際の日付の形式には影響しません。

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 属性ごとの日付形式のカスタマイズ

モデルの [キャスト宣言](/docs/{{version}}/eloquent-mutators#attribute-casting) で日付形式を指定することで、個々の Eloquent 日付属性のシリアル化形式をカスタマイズできます。

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```

