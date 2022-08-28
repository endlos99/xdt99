// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99r.psi.Xas99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99r.psi.*;
import com.intellij.psi.PsiReference;

public class Xas99ROpAliasImpl extends ASTWrapperPsiElement implements Xas99ROpAlias {

  public Xas99ROpAliasImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99RVisitor visitor) {
    visitor.visitOpAlias(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99RVisitor) accept((Xas99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  public String getName() {
    return Xas99RPsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(String newName) {
    return Xas99RPsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return Xas99RPsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public PsiReference getReference() {
    return Xas99RPsiImplUtil.getReference(this);
  }

}