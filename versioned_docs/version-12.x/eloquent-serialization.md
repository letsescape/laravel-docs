<!-- # Eloquent: Serialization -->
# Eloquent: Serialization

- [Introduction](#introduction)
- [Serializing Models and Collections](#serializing-models-and-collections)
    - [Serializing to Arrays](#serializing-to-arrays)
    - [Serializing to JSON](#serializing-to-json)
- [Hiding Attributes From JSON](#hiding-attributes-from-json)
- [Appending Values to JSON](#appending-values-to-json)
- [Date Serialization](#date-serialization)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When building APIs using Laravel, you will often need to convert your models and relationships to arrays or JSON. Eloquent includes convenient methods for making these conversions, as well as controlling which attributes are included in the serialized representation of your models. -->
Laravel로 API를 개발할 때, 모델과 연관관계(relationships)를 배열이나 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 쉽게 할 수 있는 편리한 메서드를 제공하며, 모델의 직렬화된 표현에 포함되는 속성을 제어할 수 있는 방법도 제공합니다.

> [!NOTE]
> Eloquent 모델 및 컬렉션의 JSON 직렬화를 더욱 강력하게 처리하려면, [Eloquent API resources](/docs/12.x/eloquent-resources) 문서를 참고하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
<!-- ## Serializing Models and Collections -->
## Serializing Models and Collections

<a name="serializing-to-arrays"></a>
<!-- ### Serializing to Arrays -->
### Serializing to Arrays

<!-- To convert a model and its loaded [relationships](/docs/12.x/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays: -->
모델과 로드된 [relationships](/docs/12.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용합니다. 이 메서드는 재귀적으로 동작하여 모든 속성과 연관관계(연관관계의 연관관계까지 포함)를 배열로 변환합니다:

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

<!-- The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships: -->
`attributesToArray` 메서드는 모델의 속성만 배열로 변환하며, 연관관계는 포함하지 않습니다:

```php
$user = User::first();

return $user->attributesToArray();
```

<!-- You may also convert entire [collections](/docs/12.x/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance: -->
또한, 전체 [collections](/docs/12.x/eloquent-collections)을 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다:

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
<!-- ### Serializing to JSON -->
### Serializing to JSON

<!-- To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php): -->
모델을 JSON으로 변환하려면 `toJson` 메서드를 사용합니다. `toArray`와 마찬가지로, `toJson`도 재귀적으로 모든 속성과 연관관계를 JSON으로 변환합니다. 또한 [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php) 모든 JSON 인코딩 옵션을 지정할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

<!-- Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection: -->
또는 모델이나 컬렉션을 문자열로 casting하면 자동으로 `toJson` 메서드가 호출됩니다:

```php
return (string) User::find(1);
```

<!-- Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers: -->
모델과 컬렉션은 문자열로 casting될 때 자동으로 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 일러퀀트 객체를 바로 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환된 일러퀀트 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- When an Eloquent model is converted to JSON, its loaded relationships will automatically be included as attributes on the JSON object. Also, though Eloquent relationship methods are defined using "camel case" method names, a relationship's JSON attribute will be "snake case". -->
일러퀀트 모델이 JSON으로 변환될 때, 로드된 연관관계도 자동으로 JSON 객체의 속성으로 포함됩니다. 참고로 일러퀀트의 연관관계 메서드는 “카멜 케이스(camel case)”로 정의되어 있지만, JSON 속성명은 “스네이크 케이스(snake case)”로 변환됩니다.

<a name="hiding-attributes-from-json"></a>
<!-- ## Hiding Attributes From JSON -->
## Hiding Attributes From JSON

<!-- Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property to your model. Attributes that are listed in the `$hidden` property's array will not be included in the serialized representation of your model: -->
경우에 따라 비밀번호처럼 모델의 배열 또는 JSON 표현에 포함하지 않고 싶은 속성이 있을 수 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 배열에 나열된 속성들은 직렬화된 표현에서 제외됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be hidden for serialization.
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 연관관계를 숨기려면, 연관관계의 메서드명을 일러퀀트 모델의 `$hidden` 속성에 추가하십시오.

<!-- Alternatively, you may use the `visible` property to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `$visible` array will be hidden when the model is converted to an array or JSON: -->
반대로, `visible` 속성을 사용하여 배열과 JSON 표현에 반드시 포함해야 할 속성의 “허용 목록”을 정의할 수도 있습니다. `$visible` 배열에 포함되지 않은 속성들은 모델이 배열이나 JSON으로 변환될 때 숨겨집니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be visible in arrays.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
<!-- #### Temporarily Modifying Attribute Visibility -->
#### Temporarily Modifying Attribute Visibility

<!-- If you would like to make some typically hidden attributes visible on a given model instance, you may use the `makeVisible` or `mergeVisible` methods. The `makeVisible` method returns the model instance: -->
일반적으로 숨겨지는 속성을 특정 모델 인스턴스에서만 임시로 보이게 하려면, `makeVisible` 또는 `mergeVisible` 메서드를 사용할 수 있습니다. `makeVisible`은 모델 인스턴스를 반환합니다:

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

<!-- Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` or `mergeHidden` methods: -->
반대로, 기본적으로 보이는 속성을 임시로 숨기고 싶다면 `makeHidden` 또는 `mergeHidden` 메서드를 사용할 수 있습니다:

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

<!-- If you wish to temporarily override all of the visible or hidden attributes, you may use the `setVisible` and `setHidden` methods respectively: -->
보이거나 숨겨지는 모든 속성을 일시적으로 오버라이드하려면 `setVisible` 및 `setHidden` 메서드를 각각 사용할 수 있습니다:

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
<!-- ## Appending Values to JSON -->
## Appending Values to JSON

<!-- Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/12.x/eloquent-mutators) for the value: -->
가끔 모델을 배열이나 JSON으로 변환할 때, 데이터베이스 컬럼에 직접 대응되는 속성이 없는 값을 추가하고 싶을 수 있습니다. 이런 경우, 먼저 해당 값에 대한 [accessor](/docs/12.x/eloquent-mutators)를 정의하세요:

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

<!-- If you would like the accessor to always be appended to your model's array and JSON representations, you may add the attribute name to the `appends` property of your model. Note that attribute names are typically referenced using their "snake case" serialized representation, even though the accessor's PHP method is defined using "camel case": -->
accessor를 항상 모델의 배열 및 JSON 표현에 포함하고 싶다면, 모델의 `appends` 속성에 속성명을 추가합니다. 주의할 점은 속성명은 일반적으로 “스네이크 케이스” 형태로 참조된다는 것입니다. (accessor 메서드는 PHP에서 “카멜 케이스”로 정의됩니다.)

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The accessors to append to the model's array form.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

<!-- Once the attribute has been added to the `appends` list, it will be included in both the model's array and JSON representations. Attributes in the `appends` array will also respect the `visible` and `hidden` settings configured on the model. -->
이렇게 `appends` 목록에 속성이 추가되면, 해당 속성은 모델의 배열 및 JSON 표현 모두에 포함됩니다. `appends` 배열의 속성은 모델에서 설정된 `visible` 및 `hidden` 설정도 그대로 따릅니다.

<a name="appending-at-run-time"></a>
<!-- #### Appending at Run Time -->
#### Appending at Run Time

<!-- At runtime, you may instruct a model instance to append additional attributes using the `append` or `mergeAppends` methods. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance: -->
실행 중에 특정 모델 인스턴스에 추가 속성을 붙이고 싶다면, `append` 또는 `mergeAppends` 메서드를 사용할 수 있습니다. 또는 `setAppends` 메서드를 사용해 해당 인스턴스의 추가 속성 전체 배열을 오버라이드할 수도 있습니다:

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<!-- Likewise, if you would like to remove all appended properties from a model, you may use the `withoutAppends` method: -->
반대로, 모델에서 모든 추가 속성을 제거하고 싶다면 `withoutAppends` 메서드를 사용하세요:

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
<!-- ## Date Serialization -->
## Date Serialization

<a name="customizing-the-default-date-format"></a>
<!-- #### Customizing the Default Date Format -->
#### Customizing the Default Date Format

<!-- You may customize the default serialization format by overriding the `serializeDate` method. This method does not affect how your dates are formatted for storage in the database: -->
기본 날짜 직렬화 형식을 사용자 지정하려면 `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 날짜가 저장되는 형식에는 영향을 주지 않습니다:

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
<!-- #### Customizing the Date Format per Attribute -->
#### Customizing the Date Format per Attribute

<!-- You may customize the serialization format of individual Eloquent date attributes by specifying the date format in the model's [cast declarations](/docs/12.x/eloquent-mutators#attribute-casting): -->
특정 일러퀀트 날짜 속성별로 직렬화 포맷을 정의하려면, 모델의 [cast declarations](/docs/12.x/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정하면 됩니다:

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
