# Shopify / Google Feeds Combiner

Shopify updated Liquid pages to add a pagination to product lists, this broke an implementation in place for providing products to Google Feeds.

This Repo acts a temporary fix to that problem.

## Development
One note - ensure you pull the most recent from main as this will update daily.

## Scripts

## combine_feeds.py

The `combine_feeds.py` script will loop through up to ten paginated pages on: 
`https://shop.cancerresearchuk.org/pages/xml-product-feed` 

It then restructures this as an RSS feed and saves the files in the `docs/combined_product_feed.xml`

This page is then built and deployed to Github Pages so that it can be publicly fetched by google.

You are able to run this locally:

```
python3 scripts/combine_feeds.py

✅ Combined XML product feed saved to 'docs/combined_product_feed.xml'
```

## check_totals.py

The `check_totals.py` is for sanity checking and comparing the number of products to see that the right number are found
As of 17 July 2025 this is whats returned.
```
python3 scripts/check_totals.py

✅ Total number of <item> elements: 1743
```

## Github actions
This is designed to automatically run nightly on a cron at 3am. If there are changes found in the XML a new `combined_product_feed.xml` file is committed and the github pages build and deploy should be triggered automatically.

If needed this can also be run manually from the github actions workflows page using the Update Shopify Feed action.
