<!-- # Image Manipulation -->
# Image Manipulation

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Reading Images](#reading-images)
    - [Uploaded Files](#uploaded-files)
    - [Storage Files](#storage-files)
    - [Other Sources](#other-sources)
- [Manipulating Images](#manipulating-images)
    - [Resizing Images](#resizing-images)
    - [Other Transformations](#other-transformations)
- [Encoding Images](#encoding-images)
- [Storing Images](#storing-images)
- [Inspecting Images](#inspecting-images)
- [Image Drivers](#image-drivers)
    - [Custom Image Drivers](#custom-image-drivers)
    - [Custom Transformations](#custom-transformations)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a fluent image manipulation API that allows you to resize, crop, encode, and store images using the same expressive conventions found throughout the framework. Laravel's image features are powered by [Intervention Image](https://image.intervention.io/) and support the GD and Imagick PHP extensions. -->
Laravelは、フレームワーク全体で採用されている表現力豊かな規約に沿って、画像のリサイズ、クロップ、エンコード、保存を行える、流れるような画像操作APIを提供します。Laravelの画像機能は [Intervention Image](https://image.intervention.io/) を基盤としており、GDおよびImagickのPHP拡張機能をサポートしています。

<!-- The image API is useful when working with uploaded files, files stored on Laravel [filesystem disks](/docs/13.x/filesystem), local files, remote URLs, or raw image bytes: -->
画像 API は、アップロードされたファイル、Laravel の [filesystem disks](/docs/13.x/filesystem) に保存されたファイル、ローカルファイル、リモート URL、または生の画像バイト列を扱う場合に便利です。

```php
use Illuminate\Support\Facades\Image;

$path = Image::fromStorage('avatars/photo.jpg', 'public')
    ->cover(400, 400)
    ->toWebp()
    ->quality(80)
    ->storePublicly('avatars', 'public');
```

> [!WARNING]
> 画像処理は CPU とメモリを大量に消費する可能性があります。大規模な画像処理は、アップロードを受け取る HTTP リクエスト中に実行するのではなく、[queued job](/docs/13.x/queues) で処理することを検討してください。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Before using Laravel's image manipulation features, install the Intervention Image package via Composer: -->
Laravelの画像操作機能を使用する前に、Composerを使ってIntervention Imageパッケージをインストールしてください。

```shell
composer require intervention/image:^4.0
```

<!-- You should also ensure your PHP installation has either the GD or Imagick extension installed, depending on which driver your application will use. -->
アプリケーションで使用するドライバに応じて、PHP に GD または Imagick 拡張機能のいずれかがインストールされていることも確認してください。

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Laravel's image configuration file is located at `config/images.php`. If your application does not have an `images` configuration file, you may publish it using the `config:publish` Artisan command: -->
Laravel の画像設定ファイルは `config/images.php` にあります。アプリケーションに `images` 設定ファイルがない場合は、`config:publish` Artisan コマンドを使用して公開できます。

```shell
php artisan config:publish images
```

<!-- The image configuration file allows you to specify your application's default image driver. You may also specify the default driver using the `IMAGE_DRIVER` environment variable. The supported drivers are `gd` and `imagick`: -->
画像設定ファイルでは、アプリケーションのデフォルト画像ドライバを指定できます。`IMAGE_DRIVER` 環境変数を使ってデフォルトドライバを指定することもできます。対応しているドライバは `gd` と `imagick` です。

```ini
IMAGE_DRIVER=imagick
```

<a name="reading-images"></a>
<!-- ## Reading Images -->
## Reading Images

<!-- The `Image` facade provides several methods for reading images from common sources. Image contents are loaded lazily, so the source is typically not read until the image is processed or its bytes are requested. -->
`Image` ファサードには、一般的なソースから画像を読み込むためのメソッドがいくつか用意されています。画像の内容は遅延読み込みされるため、通常、画像を処理するかバイト列を要求するまでソースは読み込まれません。

<a name="uploaded-files"></a>
<!-- ### Uploaded Files -->
### Uploaded Files

<!-- You may retrieve an uploaded image from an incoming request using the `image` method. This method returns an `Illuminate\Image\Image` instance for the uploaded file, or `null` if the file is not present: -->
受信したリクエストから、アップロードされた画像を `image` メソッドで取得できます。このメソッドは、アップロードされたファイルの `Illuminate\Image\Image` インスタンスを返します。ファイルが存在しない場合は `null` を返します。

```php
use Illuminate\Http\Request;

Route::post('/avatar', function (Request $request) {
    $request->validate(['avatar' => ['required', 'image']]);

    $path = $request->image('avatar')
        ->cover(400, 400)
        ->toWebp()
        ->storePublicly('avatars', 'public');

    // ...
});
```

<!-- Alternatively, you may create an image instance from an `Illuminate\Http\UploadedFile` instance using the `fromUpload` method: -->
または、`fromUpload` メソッドを使用して、`Illuminate\Http\UploadedFile` インスタンスから画像インスタンスを作成することもできます。

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromUpload($request->file('avatar'));
```

<!-- When an image is created from an uploaded file, you may retrieve the underlying uploaded file using the `file` method: -->
画像をアップロードされたファイルから作成した場合は、`file` メソッドを使って元のアップロードファイルを取得できます。

```php
$file = $image->file();
```

<a name="storage-files"></a>
<!-- ### Storage Files -->
### Storage Files

<!-- You may create an image instance from a file stored on one of your application's [filesystem disks](/docs/13.x/filesystem) using the `fromStorage` method. The first argument is the path to the file, while the second argument is the disk name: -->
アプリケーションの [filesystem disks](/docs/13.x/filesystem) に保存されているファイルから、`fromStorage` メソッドを使って画像インスタンスを作成できます。第1引数にはファイルのパスを、第2引数にはディスク名を指定します。

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromStorage('avatars/photo.jpg', disk: 'public');
```

<!-- You may also create image instances directly from a filesystem disk instance using the `image` method: -->
ファイルシステムディスクのインスタンスから `image` メソッドを使って直接イメージのインスタンスを作成することもできます。

```php
use Illuminate\Support\Facades\Storage;

$image = Storage::disk('public')->image('avatars/photo.jpg');
```

<a name="other-sources"></a>
<!-- ### Other Sources -->
### Other Sources

<!-- The `Image` facade also includes methods for creating image instances from raw bytes, local file paths, remote URLs, and Base64 encoded strings: -->
`Image` ファサードには、バイト列、ローカルファイルパス、リモート URL、Base64 エンコードされた文字列から画像インスタンスを作成するメソッドも用意されています。

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromBytes($contents);
$image = Image::fromBase64($base64);
$image = Image::fromPath(storage_path('app/avatars/photo.jpg'));
$image = Image::fromUrl('https://example.com/photo.jpg');
```

<a name="manipulating-images"></a>
<!-- ## Manipulating Images -->
## Manipulating Images

<!-- Image instances are immutable. Each manipulation method returns a new image instance with the transformation appended to its processing pipeline, allowing methods to be chained fluently: -->
画像インスタンスは不変です。各操作メソッドは、変換を処理パイプラインに追加した新しい画像インスタンスを返すため、メソッドを流れるようにチェーンできます。

```php
$image = $request->image('avatar')
    ->orient()
    ->cover(400, 400)
    ->sharpen(10);
```

<!-- Transformations are processed in the order they are added to the image pipeline and the image is only encoded once at the end. -->
変換は画像パイプラインに追加された順序で処理され、画像は最後に一度だけエンコードされます。

<a name="resizing-images"></a>
<!-- ### Resizing Images -->
### Resizing Images

<!-- The `resize` method resizes an image to the given dimensions. You may provide both a width and height, or provide only one dimension using named arguments: -->
`resize` メソッドは、指定したサイズに画像をリサイズします。幅と高さの両方を指定することも、名前付き引数を使って一方のサイズだけを指定することもできます。

```php
$image = $image->resize(800, 600);
$image = $image->resize(width: 800);
$image = $image->resize(height: 600);
```

<!-- The `scale` method proportionally scales an image down so that it fits within the given dimensions. This method will never increase the size of an image: -->
`scale` メソッドは、画像が指定された寸法内に収まるよう、縦横比を維持したまま縮小します。このメソッドで画像が拡大されることはありません。

```php
$image = $image->scale(800, 600);
$image = $image->scale(width: 800);
$image = $image->scale(height: 600);
```

<!-- The `cover` method resizes and crops an image to completely cover the given dimensions: -->
`cover` メソッドは、指定されたサイズ全体を覆うように画像のサイズを変更し、トリミングします。

```php
$image = $image->cover(400, 400);
```

<!-- The `contain` method resizes an image to fit within the given dimensions while preserving the entire image. If necessary, empty space will be filled using the optional background color: -->
`contain` メソッドは、画像全体を維持したまま、指定されたサイズ内に収まるよう画像のサイズを変更します。必要に応じて、空いた領域をオプションの背景色で塗りつぶします。

```php
$image = $image->contain(400, 400);
$image = $image->contain(400, 400, '#ffffff');
$image = $image->contain(400, 400, 'dominant');
```

<!-- You may specify `dominant` as the background color to fill empty space using the image's dominant color. -->
画像の主要な色を使って空白を塗りつぶす背景色として、`dominant` を指定できます。

<!-- You may crop an image using the `crop` method. The first two arguments are the desired width and height, and the optional third and fourth arguments specify the crop's `x` and `y` coordinates: -->
`crop` メソッドを使用して画像をトリミングできます。最初の2つの引数には必要な幅と高さを指定し、3番目と4番目のオプション引数にはトリミング範囲の `x` 座標と `y` 座標を指定します。

```php
$image = $image->crop(300, 200);
$image = $image->crop(300, 200, x: 50, y: 25);
```

<a name="other-transformations"></a>
<!-- ### Other Transformations -->
### Other Transformations

<!-- Laravel also provides a variety of additional image transformation methods: -->
Laravel には、画像を変換する追加のメソッドもさまざまに用意されています。

```php
$image = $image->orient();
$image = $image->rotate(90);
$image = $image->rotate(90, '#ffffff');
$image = $image->rotate(90, 'dominant');
$image = $image->blur(5);
$image = $image->grayscale();
$image = $image->sharpen(10);
$image = $image->flipVertically();
$image = $image->flipHorizontally();
```

<!-- The `orient` method rotates the image according to its EXIF orientation data. The `rotate` method rotates the image clockwise by the given angle and accepts an optional background color. The `blur` and `sharpen` methods accept values between `0` and `100`. -->
`orient` メソッドは、画像の EXIF の向き情報に従って画像を回転させます。`rotate` メソッドは、指定した角度で画像を時計回りに回転させ、オプションで背景色を指定できます。`blur` メソッドと `sharpen` メソッドには、`0` から `100` までの値を指定できます。

<a name="conditional-transformations"></a>
<!-- #### Conditional Transformations -->
#### Conditional Transformations

<!-- Image instances support Laravel's `Conditionable` trait, allowing you to conditionally apply transformations using the `when` and `unless` methods: -->
画像インスタンスは Laravel の `Conditionable` トレイトをサポートしているため、`when` メソッドと `unless` メソッドを使って条件付きで変換を適用できます。

```php
$image = $request->image('avatar')
    ->when($request->boolean('crop'), fn ($image) => $image->cover(400, 400))
    ->unless($request->boolean('preserve_format'), fn ($image) => $image->toWebp());
```

<a name="encoding-images"></a>
<!-- ## Encoding Images -->
## Encoding Images

<!-- By default, processed images are encoded using their original format. However, you may convert the image to another supported format before retrieving or storing it: -->
デフォルトでは、処理済みの画像は元の形式でエンコードされます。ただし、取得または保存する前に、画像をサポートされている別の形式へ変換できます。

```php
$image = $image->toWebp();
$image = $image->toJpg();
$image = $image->toJpeg();
$image = $image->toPng();
$image = $image->toGif();
$image = $image->toAvif();
$image = $image->toBmp();
```

<!-- You may use the `quality` method to set the output quality. The quality will be clamped between `1` and `100`: -->
`quality` メソッドを使用して出力品質を設定できます。品質は `1` から `100` の範囲に収まるよう制限されます。

```php
$image = $image->toWebp()->quality(80);
```

<!-- The `optimize` method is a convenient shortcut for converting the image to a given format and setting its quality. By default, images are optimized as WebP images with a quality of `70`: -->
`optimize` メソッドは、画像を指定した形式に変換し、品質を設定する便利なショートカットです。デフォルトでは、画像は品質 `70` の WebP 画像として最適化されます。

```php
$image = $image->optimize();

$image = $image->optimize(format: 'jpg', quality: 85);
```

<!-- You may retrieve the processed image contents as a string of bytes, base64 encoded string, or data URI: -->
処理済みの画像コンテンツは、バイト列、Base64エンコード文字列、またはデータ URI として取得できます。

```php
$bytes = $image->toBytes();
$base64 = $image->toBase64();
$dataUri = $image->toDataUri();
```

<!-- An image instance may also be cast to a string to retrieve a data URI: -->
画像インスタンスを文字列に cast して、データ URI を取得することもできます。

```php
$dataUri = (string) $image;
```

<a name="storing-images"></a>
<!-- ## Storing Images -->
## Storing Images

<!-- The `store` method stores the processed image on one of your application's filesystem disks. Like uploaded files, Laravel will generate a unique filename and return the stored path. The second argument may be used to specify the disk: -->
`store` メソッドは、処理済みの画像をアプリケーションのファイルシステムディスクのいずれかに保存します。アップロードされたファイルと同様に、Laravel は一意のファイル名を生成し、保存先のパスを返します。第 2 引数を使用してディスクを指定できます。

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars', disk: 's3');
```

<!-- You may use the `storeAs` method to specify the stored filename: -->
`storeAs` メソッドを使用して、保存するファイル名を指定できます。

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storeAs(path: 'avatars', name: 'avatar.jpg', disk: 'public');
```

<!-- The `storePublicly` and `storePubliclyAs` methods store the image with `public` visibility: -->
`storePublicly` および `storePubliclyAs` メソッドは、画像を `public` の可視性で保存します。

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePublicly(path: 'avatars', disk: 'public');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePubliclyAs(path: 'avatars', name: 'avatar.webp', disk: 'public');
```

<!-- If the image could not be stored, the storage methods return `false`. -->
画像を保存できなかった場合、ストレージメソッドは `false` を返します。

<a name="inspecting-images"></a>
<!-- ## Inspecting Images -->
## Inspecting Images

<!-- You may retrieve the image's MIME type, extension, dimensions, width, height, and dominant color using the following methods: -->
次のメソッドを使用すると、画像の MIME タイプ、拡張子、寸法、幅、高さ、主要な色を取得できます。

```php
$mimeType = $image->mimeType();
$extension = $image->extension();

[$width, $height] = $image->dimensions();
$width = $image->width();
$height = $image->height();

$dominantColor = $image->dominantColor();
```

<!-- These methods operate on the processed image. For example, calling `width` after `cover(400, 400)` will return `400`. -->
これらのメソッドは、処理済みの画像に対して動作します。たとえば、`cover(400, 400)` の後に `width` を呼び出すと、`400` が返されます。

<a name="image-drivers"></a>
<!-- ## Image Drivers -->
## Image Drivers

<a name="custom-image-drivers"></a>
<!-- ### Custom Image Drivers -->
### Custom Image Drivers

<!-- Laravel's image manager extends Laravel's base `Illuminate\Support\Manager` class. This means you may register custom image drivers using the `extend` method available on the image manager and `Image` facade. -->
Laravel のイメージマネージャは、Laravel の基底クラスである `Illuminate\Support\Manager` を継承しています。これにより、イメージマネージャと `Image` ファサードで利用できる `extend` メソッドを使って、カスタムイメージドライバを登録できます。

<!-- Custom image drivers should implement the `Illuminate\Contracts\Image\Driver` interface. The `process` method receives the original image contents and the ordered `Illuminate\Image\ImagePipeline` that should be applied to the image, and should return the processed image bytes: -->
カスタム画像ドライバは、`Illuminate\Contracts\Image\Driver` インターフェースを実装する必要があります。`process` メソッドは元の画像コンテンツと、画像に適用する順序付けられた `Illuminate\Image\ImagePipeline` を受け取り、処理済みの画像バイト列を返します。

```php
<?php

namespace App\Images;

use Illuminate\Contracts\Image\Driver;
use Illuminate\Image\ImagePipeline;

class VipsDriver implements Driver
{
    /**
     * Process the given image contents with the specified pipeline.
     */
    public function process(string $contents, ImagePipeline $pipeline): string
    {
        // Apply the pipeline's transformations and output options...

        return $contents;
    }

    /**
     * Register a transformation handler.
     */
    public function transformUsing(string $transformation, callable $callback): static
    {
        // Store the handler so it may be applied while processing the pipeline...

        return $this;
    }
}
```

> [!NOTE]
> カスタム画像ドライバの実装方法をより深く理解するには、フレームワークに組み込まれている `Illuminate\Image\Drivers\InterventionDriver` クラスを確認してください。

<!-- Once you have implemented your custom driver, you may register it using the `Image` facade's `extend` method. Typically, this should be done in the `boot` method of a service provider: -->
カスタムドライバを実装したら、`Image` ファサードの `extend` メソッドを使って登録できます。通常は、サービスプロバイダの `boot` メソッドで登録します。

```php
use App\Images\VipsDriver;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Image;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Image::extend('vips', function (Application $app) {
        return new VipsDriver;
    });
}
```

<!-- After registering the driver, you may use it for a specific image using the `using` method: -->
ドライバを登録したら、`using` メソッドを使って特定の画像で使用できます。

```php
$image = $request->image('avatar')
    ->using('vips')
    ->cover(400, 400);
```

<!-- You may also configure a custom driver as your application's default image driver using the `default` option in your application's `config/images.php` configuration file or the `IMAGE_DRIVER` environment variable: -->
`config/images.php` 設定ファイルの `default` オプションまたは `IMAGE_DRIVER` 環境変数を使用して、カスタムドライバをアプリケーションのデフォルト画像ドライバとして設定することもできます。

```ini
IMAGE_DRIVER=vips
```

<a name="custom-transformations"></a>
<!-- ### Custom Transformations -->
### Custom Transformations

<!-- Applications and packages may define custom transformations by creating a class that implements the `Illuminate\Contracts\Image\Transformation` contract. Custom transformations can then be added to an image pipeline using the `transform` method: -->
アプリケーションやパッケージでは、`Illuminate\Contracts\Image\Transformation` コントラクトを実装するクラスを作成して、カスタム変換を定義できます。定義したカスタム変換は、`transform` メソッドを使って画像パイプラインに追加できます。

```php
<?php

namespace App\Images\Transformations;

use Illuminate\Contracts\Image\Transformation;

class Pixelate implements Transformation
{
    public function __construct(
        public readonly int $size,
    ) {
        //
    }
}
```

<!-- Next, register a handler for the transformation and driver using the `Image` facade's `transformUsing` method. Typically, this should be done in the `boot` method of a service provider: -->
次に、`Image` ファサードの `transformUsing` メソッドを使って、変換とドライバのハンドラを登録します。通常は、サービスプロバイダの `boot` メソッドで登録します。

```php
use App\Images\Transformations\Pixelate;
use Illuminate\Support\Facades\Image;
use Intervention\Image\Interfaces\ImageInterface;

Image::transformUsing('gd', Pixelate::class, function (ImageInterface $image, Pixelate $transformation) {
    return $image->pixelate($transformation->size);
});
```

<!-- Once the transformation handler has been registered, you may apply the transformation to an image: -->
変換ハンドラを登録したら、画像に変換を適用できます。

```php
use App\Images\Transformations\Pixelate;

$image = $request->image('avatar')
    ->transform(new Pixelate(12))
    ->store('avatars');
```
