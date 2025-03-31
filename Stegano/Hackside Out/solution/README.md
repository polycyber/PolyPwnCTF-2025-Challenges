# Hackside Out 1

## Write-up FR

Nous commençons par lire les données EXIF de l'image.

```bash
exiftool image.jpeg
```

La ligne "Comment" contient un texte en Base64.

```
Comment                         : cG9seWN5YmVye2pPWV9TQUROZSRTX0YzQXJfRElzR3U1dF9hTjkzcn0=
```

Une convertion depuis Base64 révèle le flag.

## Write-up EN

We start by reading the EXIF data of the image.

```bash
exiftool image.jpeg
```

The "Comment" line contains a text in Base64.

```
Comment                         : cG9seWN5YmVye2pPWV9TQUROZSRTX0YzQXJfRElzR3U1dF9hTjkzcn0=
```

A conversion from Base64 reveals the flag.

## Flag

`polycyber{jOY_SADNe$S_F3Ar_DIsGu5t_aN93r}`