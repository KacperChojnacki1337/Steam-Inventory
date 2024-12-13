CREATE TABLE public.currency_table (
	id serial4 NOT NULL,
	"date" date NULL,
	rate numeric NULL,
	CONSTRAINT currency_table_pkey PRIMARY KEY (id)
);

CREATE TABLE public.inventory (
	item_number serial4 NOT NULL,
	buy_date date NOT NULL,
	item_name text NOT NULL,
	cost_per_item float4 NOT NULL,
	number_of_items int4 NOT NULL,
	current_price float4 NOT NULL,
	total_cost float4 NOT NULL,
	total_value float4 NOT NULL,
	total_return_percent float4 NOT NULL,
	total_return_dollar float4 NULL,
	item_link varchar(255) NOT NULL,
	purchase_info int4 NULL,
	real_cost_per_item float8 NULL,
	real_total_cost float8 NULL,
	CONSTRAINT inventory_pkey PRIMARY KEY (item_number)
);

CREATE TABLE public.inventory_data (
	id serial4 NULL,
	update_date date NULL,
	item_number int4 NULL,
	item_name text NULL,
	cost_per_item float4 NULL,
	number_of_items int4 NULL,
	current_price float4 NULL,
	total_cost float4 NULL,
	total_value float4 NULL,
	item_link varchar(255) NULL,
	exchange_rate numeric(10, 4) NULL,
	buy_date date NULL,
	real_cost_per_item_pln numeric(10, 2) NULL,
	real_total_cost_pln float8 NULL,
	real_total_value_pln numeric(10, 2) NULL,
	exchange_rate_update numeric NULL,
	cost_per_item_pln numeric(10, 2) NULL,
	total_cost_pln numeric(10, 2) NULL,
	total_value_pln numeric(10, 2) NULL,
	current_price_pln numeric(10, 2) NULL,
	type_of_purchase_channel text NULL,
	purchase_id int4 NULL,
	CONSTRAINT fk_inventory_data_purchase_channels FOREIGN KEY (purchase_id) REFERENCES public.purchase_channels(id)
);
CREATE INDEX idx_inventory_data_purchase_id ON public.inventory_data USING btree (purchase_id);

CREATE TABLE public.purchase_channels (
	id serial4 NOT NULL,
	channel varchar(50) NULL,
	type_of_channel varchar(50) NULL,
	CONSTRAINT purchase_channels_pkey PRIMARY KEY (id)
);

CREATE TABLE public.sales_channels (
	id serial4 NOT NULL,
	channel text NULL,
	CONSTRAINT sales_channels_pkey PRIMARY KEY (id)
);


CREATE TABLE public.sales_data (
	id int4 DEFAULT nextval('my_sequence'::regclass) NOT NULL,
	sales_date date NOT NULL,
	item_number int4 NULL,
	channel_id int4 NULL,
	selling_price_real_pln numeric NULL,
	selling_price_steam_pln numeric NULL,
	CONSTRAINT sales_data_pkey PRIMARY KEY (id)
);







