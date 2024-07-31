import { createClient } from "redis";
import { promisify } from "util";
import express from "express";

const listProducts = [
  { id: 1, name: "Suitcase 250", price: 50, stock: 4 },
  { id: 2, name: "Suitcase 450", price: 100, stock: 10 },
  { id: 3, name: "Suitcase 650", price: 350, stock: 2 },
  { id: 4, name: "Suitcase 1050", price: 550, stock: 5 },
];

function getItemById(id) {
  return listProducts.find((product) => product.id === id);
}

const client = createClient();

client.on("connect", () => {
  console.log("Redis client connected to the server");
});
client.on("error", (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

function reserveStockById(itemId, stock) {
  const key = `item.${itemId}`;
  return setAsync(key, stock);
}
function getCurrentReservedStockById(itemId) {
  const key = `item.${itemId}`;
  return getAsync(key);
}

const app = express();

app.use(express.json());

app.get("/list_products", (req, res) => {
  const newListPorducts = listProducts.map((product) => {
    return {
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
    };
  });
  res.json(newListPorducts);
});

app.get("/list_products/:itemId", async (req, res) => {
  const id = parseInt(req.params.itemId);
  let currentProduct = getItemById(id);
  const currentQuantity = await getCurrentReservedStockById(id);
  if (!currentProduct) {
    res.status(404).json({ status: "Product not found" });
  } else {
    currentProduct = {
      itemId: currentProduct.id,
      itemName: currentProduct.name,
      price: currentProduct.price,
      initialAvailableQuantity: currentProduct.stock,
      currentQuantity: currentQuantity,
    };
    res.json(currentProduct);
  }
});

app.get("/reserve_product/:itemId", async (req, res) => {
  const id = parseInt(req.params.itemId);
  const currentProduct = getItemById(id);
  if (!currentProduct) {
    res.status(404).json({ status: "Product not found" });
  } else {
    const currentQuantity = await getCurrentReservedStockById(id);
    if (parseInt(currentQuantity) === 0) {
      res
        .status(403)
        .json({ status: "Not enough stock available", itemId: id });
    } else {
      const newQuantity = parseInt(currentQuantity) - 1;
      await reserveStockById(id, newQuantity);
      res.json({ status: "Reservation confirmed", itemId: id });
    }
  }
});

app.listen(1245, () => {
  console.log("API available on localhost port 1245");
});
