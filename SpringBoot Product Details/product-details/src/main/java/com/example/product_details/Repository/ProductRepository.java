package com.example.product_details.Repository;



import com.example.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<Product, Long> {
    // No need to add anything extra, JpaRepository provides all CRUD methods
}
